#!/usr/bin/env python3
"""Exercise Calamares through AT-SPI in a disposable VM with one blank disk.

Never run this on a physical machine. smoke-test.py alone deploys it into QEMU.
"""
import os
import subprocess
import time
import pyatspi

if not os.path.exists('/sys/class/dmi/id/product_name') or 'QEMU' not in open('/sys/class/dmi/id/sys_vendor').read():
    raise SystemExit('This destructive integration test requires a QEMU virtual machine.')
process = subprocess.Popen(['calamares', '-d'], stdout=open('/tmp/pkos-install-test.log','w'), stderr=subprocess.STDOUT)

def walk(node, depth=0):
    if depth > 22:
        return
    yield node
    try:
        for child in node:
            yield from walk(child, depth+1)
    except Exception:
        pass

def nodes():
    return list(walk(pyatspi.Registry.getDesktop(0)))

def visible(node):
    return node.getState().contains(pyatspi.STATE_SHOWING)

def dump():
    for node in nodes():
        if visible(node):
            print(node.getRoleName(), repr(node.name), flush=True)

def click(name, timeout=60):
    end=time.time()+timeout
    while time.time()<end:
        for node in nodes():
            if node.getRoleName()=='push button' and node.name.replace('&','').strip().lower()==name.lower() and visible(node) and node.getState().contains(pyatspi.STATE_ENABLED):
                action=node.queryAction()
                action.doAction(0)
                print('Clicked',name,flush=True)
                time.sleep(2)
                return
        time.sleep(1)
    dump()
    raise RuntimeError('No enabled button: '+name)

time.sleep(15)
dump()
for page in ['Welcome','Location','Keyboard','Partitions']:
    print('Leaving',page,flush=True)
    click('Next')
time.sleep(3)
entries=[]
for node in nodes():
    if node.getRoleName() in ['text','password text','entry'] and visible(node):
        try:
            node.queryEditableText()
            bounds=node.queryComponent().getExtents(pyatspi.DESKTOP_COORDS)
            if bounds.width>50:
                entries.append((bounds.y,bounds.x,node))
        except Exception:
            pass
entries.sort(key=lambda item:item[:2])
print('User input count:',len(entries),flush=True)
if len(entries)!=5:
    dump()
    raise RuntimeError('Expected five user fields (name, login, hostname, password, repeat)')
for (_,_,node),value in zip(entries,['PKOS Test','pkostest','pkos','pkos-test-123','pkos-test-123']):
    bounds=node.queryComponent().getExtents(pyatspi.DESKTOP_COORDS)
    subprocess.run(['xdotool','mousemove','--sync',str(bounds.x+bounds.width//2),str(bounds.y+bounds.height//2),'click','1','key','ctrl+a'],check=True)
    subprocess.run(['xdotool','type','--clearmodifiers','--delay','40',value],check=True)
    time.sleep(.5)
click('Next')
click('Install')
click('Install now')
end=time.time()+1200
while time.time()<end:
    texts=[node.name for node in nodes() if visible(node)]
    if any('failed' in text.lower() and 'installation' in text.lower() for text in texts):
        dump()
        raise RuntimeError('Calamares reported installation failure')
    if any('all done' in text.lower() for text in texts):
        print('PKOS_INSTALL_PASS',flush=True)
        process.terminate()
        raise SystemExit(0)
    if process.poll() is not None:
        raise RuntimeError('Calamares closed unexpectedly')
    time.sleep(5)
dump()
raise RuntimeError('Calamares installation did not finish in 20 minutes')
