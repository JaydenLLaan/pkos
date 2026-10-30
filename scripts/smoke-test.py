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
import zlib
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

def screenshot(name='live-desktop'):
    sock = socket.socket(socket.AF_UNIX)
    sock.connect(qmp_path)
    stream = sock.makefile('rwb', buffering=0)
    stream.readline()
    for request in [{'execute':'qmp_capabilities'}, {'execute':'screendump','arguments':{'filename':str(out/(name+'.ppm'))}}]:
        stream.write((json.dumps(request)+'\n').encode())
        while True:
            msg = json.loads(stream.readline())
            if 'return' in msg or 'error' in msg:
                if 'error' in msg:
                    raise RuntimeError(msg)
                break
    sock.close()
    Image.open(out/(name+'.ppm')).save(out/(name+'.png'))

try:
    vm.expect(r'pkos login:')
    vm.sendline('pkos')
    result = vm.expect([r'Password:', r'pkos@pkos'])
    if result == 0:
        vm.sendline('live')
    command('sudo -n true')
    command('test -d /sys/firmware/efi && grep -q \'ID=pkos\' /etc/os-release')
    command('systemctl is-active NetworkManager sddm; systemctl is-enabled bluetooth')
    command('for n in $(seq 1 90); do pgrep -x plasmashell >/dev/null && break; sleep 2; done; pgrep -a plasmashell; pgrep -a kwin_wayland', 240)
    command('loginctl list-sessions; loginctl show-session $(loginctl list-sessions --no-legend | awk \'$3=="pkos" && $4=="seat0" {print $1; exit}\') -p Type | grep Wayland -i')
    command('test -x /usr/local/bin/pk-gpu && test -x /usr/local/bin/pk-setup; uv --version; node --version; go version; nvim --version | head -1')
    command('sudo modinfo nvidia-current | head -10; sudo dkms status; test -e /usr/share/wayland-sessions/plasma.desktop')
    command('grep -q "plugin=org.kde.plasma.icontasks" ~/.config/plasma-org.kde.plasma.desktop-appletsrc')
    screenshot()
    command('systemd-run --user --collect --unit=pkos-installer-test pk-install')
    command('sleep 15; pgrep -a calamares; journalctl --user -u pkos-installer-test --no-pager | tail -60', 60)
    screenshot('live-installer')
    # Run the real installer against the disposable blank virtual disk.
    # Test dependencies are installed only in the live overlay, not in the ISO.
    command('sudo apt-get update >/tmp/pkos-test-apt.log 2>&1 && sudo apt-get install -y --no-install-recommends python3-pyatspi xdotool >>/tmp/pkos-test-apt.log 2>&1', 240)
    command('sudo pkill -x calamares')
    # Keep the command below the serial TTY's canonical input line limit.
    payload = base64.b64encode(zlib.compress(Path('scripts/calamares-test.py').read_bytes())).decode()
    command("printf '%s' '"+payload+"' | base64 -d | python3 -c 'import sys,zlib; sys.stdout.buffer.write(zlib.decompress(sys.stdin.buffer.read()))' >/tmp/pkos-calamares-test.py")
    try:
        command('sudo env $(systemctl --user show-environment | grep -E "^(DISPLAY|XAUTHORITY)=") QT_QPA_PLATFORM=xcb QT_LINUX_ACCESSIBILITY_ALWAYS_ON=1 dbus-run-session -- python3 /tmp/pkos-calamares-test.py', 1500)
    finally:
        screenshot('install-result')
        command('sudo tail -150 /tmp/pkos-install-test.log', 60)
    command('sudo mkdir -p /mnt/pkos-test; sudo mount /dev/vda2 /mnt/pkos-test && sudo mount /dev/vda1 /mnt/pkos-test/boot/efi')
    command('sudo test -f /mnt/pkos-test/boot/efi/EFI/pkOS/grubx64.efi && sudo test -f /mnt/pkos-test/boot/efi/EFI/boot/bootx64.efi')
    command('sudo cat /mnt/pkos-test/etc/fstab; sudo test ! -e /mnt/pkos-test/etc/skel/Desktop/install-pkos.desktop')
    # Enable a serial console in this disposable installed target, never the ISO.
    command("sudo sed -i 's/quiet splash/console=tty0 console=ttyS0,115200/g' /mnt/pkos-test/boot/grub/grub.cfg")
    command('sudo umount /mnt/pkos-test/boot/efi && sudo umount /mnt/pkos-test')
    vm.sendline('sudo systemctl poweroff')
    vm.expect(pexpect.EOF, timeout=120)
    log.close()
    Path(qmp_path).unlink(missing_ok=True)
    installed_args=[]
    i=0
    while i<len(args):
        if args[i] in ['-cdrom','-boot']:
            i+=2
        else:
            installed_args.append(args[i]); i+=1
    log=(out/'installed-serial.log').open('w')
    vm=pexpect.spawn('qemu-system-x86_64',installed_args,encoding='utf-8',codec_errors='replace',timeout=600)
    vm.logfile=log
    vm.expect(r'pkos login:')
    vm.sendline('pkostest')
    vm.expect('Password:')
    vm.sendline('pkos-test-123')
    command('grep -q ID=pkos /etc/os-release && ! grep -qw boot=live /proc/cmdline')
    command('for n in $(seq 1 90); do pgrep -x plasmashell >/dev/null && break; sleep 2; done; pgrep -a plasmashell; pgrep -a kwin_wayland',240)
    command("printf 'pkos-test-123\\n' | sudo -S -p '' true")
    command('findmnt /; findmnt /boot/efi; swapon --show; test ! -d /run/live/medium')
    command('test ! -e /etc/sudoers.d/live; test -f ~/.config/kdeglobals; test ! -e ~/Desktop/install-pkos.desktop; test -x /usr/local/bin/pk-setup')
    screenshot('installed-desktop')
    (out/'boot-result.json').write_text(json.dumps({'uefi':True,'liveDesktop':'Plasma Wayland','serialLogin':True,'nvidiaDKMS':True,'calamaresInstall':True,'installedDesktop':'Plasma Wayland','sudoUser':True},indent=2)+'\n')
    print('PASS: actual ISO live UEFI boot, Calamares erase-disk install, installed UEFI boot and Plasma Wayland verified.',flush=True)
finally:
    if vm.isalive():
        vm.terminate(force=True)
    log.close()
    disk.unlink(missing_ok=True)
