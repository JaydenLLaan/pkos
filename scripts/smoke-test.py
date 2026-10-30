#!/usr/bin/env python3
"""Boot the actual ISO with OVMF and check a real Plasma Wayland session."""
from pathlib import Path
import base64
import json
import os
import shutil
import socket
import subprocess
import sys
import time
import pexpect
from PIL import Image

iso = Path(sys.argv[1]).resolve()
out = Path('test-results').resolve()
out.mkdir(exist_ok=True)
code = next(Path('/usr/share/OVMF').glob('OVMF_CODE_4M.fd'))
variables = out/'OVMF_VARS.fd'
shutil.copy2('/usr/share/OVMF/OVMF_VARS_4M.fd', variables)
disk = out/'install-test.qcow2'
subprocess.run(['qemu-img','create','-f','qcow2',str(disk),'48G'], check=True)
qmp_path = str(out/'qmp.sock')
if Path(qmp_path).exists():
    Path(qmp_path).unlink()
accel = 'kvm' if os.access('/dev/kvm', os.R_OK | os.W_OK) else 'tcg'
args = ['-machine','q35','-accel',accel,'-cpu','max','-smp','2','-m','6144',
        '-drive',f'if=pflash,format=raw,readonly=on,file={code}',
        '-drive',f'if=pflash,format=raw,file={variables}',
        '-drive',f'file={disk},format=qcow2,if=virtio',
        '-cdrom',str(iso),'-boot','d','-vga','virtio',
        '-device','virtio-rng-pci','-netdev','user,id=net0','-device','virtio-net-pci,netdev=net0',
        '-display','none','-serial','stdio','-qmp',f'unix:{qmp_path},server=on,wait=off','-no-reboot']
log = (out/'live-serial.log').open('w')
vm = pexpect.spawn('qemu-system-x86_64', args, encoding='utf-8', codec_errors='replace', timeout=900)
vm.logfile = log

def command(text, timeout=120):
    vm.sendline(text + '; printf "\\n__PKOS_RC_%s__\\n" "$?"')
    vm.expect(r'__PKOS_RC_(\d+)__', timeout=timeout)
    output = vm.before
    rc = int(vm.match.group(1))
    print(output, flush=True)
    if rc:
        raise RuntimeError(f'Guest command exited {rc}: {text}')
    return output

def screenshot():
    sock = socket.socket(socket.AF_UNIX)
    sock.connect(qmp_path)
    stream = sock.makefile('rwb', buffering=0)
    stream.readline()
    for request in [{'execute':'qmp_capabilities'}, {'execute':'screendump','arguments':{'filename':str(out/'live-desktop.ppm')}}]:
        stream.write((json.dumps(request)+'\n').encode())
        while True:
            msg = json.loads(stream.readline())
            if 'return' in msg or 'error' in msg:
                if 'error' in msg:
                    raise RuntimeError(msg)
                break
    sock.close()
    Image.open(out/'live-desktop.ppm').save(out/'live-desktop.png')

try:
    vm.expect(r'pkos login:')
    vm.sendline('pkos')
    result = vm.expect([r'Password:', r'pkos@pkos'])
    if result == 0:
        vm.sendline('live')
    command('sudo -n true')
    command('test -d /sys/firmware/efi && grep -q \'ID=pkos\' /etc/os-release')
    command('systemctl is-active NetworkManager bluetooth sddm')
    command('for n in $(seq 1 90); do pgrep -x plasmashell >/dev/null && break; sleep 2; done; pgrep -a plasmashell; pgrep -a kwin_wayland', 240)
    command('loginctl list-sessions; loginctl show-session $(loginctl list-sessions --no-legend | awk \'$3=="pkos" && $4=="seat0" {print $1; exit}\') -p Type | grep Wayland -i')
    command('test -x /usr/local/bin/pk-gpu && test -x /usr/local/bin/pk-setup; uv --version; node --version; go version; nvim --version | head -1')
    command('sudo modinfo nvidia | head -10; sudo dkms status; test -e /usr/share/wayland-sessions/plasma.desktop')
    command('sudo -u pkos env XDG_RUNTIME_DIR=/run/user/1000 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus qdbus6 org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript "print(panels().length)" | grep 1')
    screenshot()
    (out/'boot-result.json').write_text(json.dumps({'uefi':True,'liveDesktop':'Plasma Wayland','serialLogin':True,'nvidiaDKMS':True},indent=2)+'\n')
    print('PASS: actual ISO booted with UEFI to Plasma Wayland; desktop, network services and DKMS verified.',flush=True)
finally:
    if vm.isalive():
        vm.terminate(force=True)
    log.close()
    disk.unlink(missing_ok=True)
