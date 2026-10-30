#!/usr/bin/env python3
"""Deploy source SVGs and configurations. Raster rendering runs on CI only."""
from pathlib import Path
import shutil
import subprocess
import sys
import json
from design import deploy

root = Path(sys.argv[1])
source = Path('branding')

def copy(src, dest):
    target = root / dest.lstrip('/')
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, target)
    return target

def png(src, dest, width, height=None):
    target = root / dest.lstrip('/')
    target.parent.mkdir(parents=True, exist_ok=True)
    cmd = ['rsvg-convert', '-w', str(width)]
    if height:
        cmd += ['-h', str(height)]
    subprocess.run([*cmd, '-o', str(target), str(src)], check=True)
    return target

for size in [16, 24, 32, 48, 64, 128, 256, 512]:
    png(source/'logo.svg', f'usr/share/icons/hicolor/{size}x{size}/apps/pkos.png', size)
copy(source/'logo.svg', 'usr/share/icons/hicolor/scalable/apps/pkos.svg')
copy(source/'logo.svg', 'usr/share/pkos/logo.svg')
copy(source/'wordmark.svg', 'usr/share/pkos/wordmark.svg')
for name in ['slate', 'horizon', 'arc']:
    base = f'usr/share/wallpapers/pkos-{name}'
    png(source/f'wallpapers/{name}.svg', base+'/contents/images/2560x1440.png', 2560, 1440)
    meta = root/base/'metadata.json'
    meta.write_text(json.dumps({'KPlugin': {'Id': f'pkos-{name}', 'Name': f'pkOS {name.title()}', 'License': 'MIT', 'Authors': [{'Name':'pkOS'}]}, 'KPackageStructure':'Wallpaper/Images'}, indent=2))
for name, dest in [('plasma','usr/share/plasma/look-and-feel/org.pkos.desktop'), ('sddm','usr/share/sddm/themes/pkos'), ('plymouth','usr/share/plymouth/themes/pkos'), ('grub','usr/share/grub/themes/pkos')]:
    shutil.copytree(source/name, root/dest, dirs_exist_ok=True)
for dest in ['usr/share/sddm/themes/pkos/wordmark.png', 'usr/share/plymouth/themes/pkos/wordmark.png', 'etc/calamares/branding/pkos/wordmark.png']:
    png(source/'wordmark.svg', dest, 320)
png(source/'logo.svg', 'etc/calamares/branding/pkos/logo.png', 128)
png(source/'welcome.svg', 'etc/calamares/branding/pkos/welcome.png', 900)
# Full scheme, including disabled/inactive groups, derived from one palette.
scheme = '[General]\nName=pkOS\nColorScheme=pkOS\n\n'
palette = {'View': '16,21,27', 'Window':'23,33,43', 'Button':'23,33,43', 'Selection':'139,171,192', 'Tooltip':'23,33,43', 'Complementary':'16,21,27', 'Header':'23,33,43'}
for group, bg in palette.items():
    for suffix in ['', '[Inactive]', '[Disabled]']:
        foreground='16,21,27' if group=='Selection' else '237,242,247'
        scheme += f'[Colors:{group}]{suffix}\nBackgroundNormal={bg}\nBackgroundAlternate=23,33,43\nForegroundNormal={foreground}\nForegroundInactive=139,171,192\nForegroundActive=139,171,192\nForegroundLink=139,171,192\nForegroundVisited=139,171,192\nForegroundNegative=210,123,131\nForegroundNeutral=199,172,118\nForegroundPositive=140,174,152\nDecorationFocus=139,171,192\nDecorationHover=139,171,192\n\n'
scheme += '[WM]\nactiveBackground=23,33,43\nactiveForeground=237,242,247\ninactiveBackground=23,33,43\ninactiveForeground=139,171,192\n'
p=root/'usr/share/color-schemes/pkOS.colors'
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text(scheme)
# KDE's ColorScheme key names a scheme; a finished first login also needs
# its resolved palette in kdeglobals (including for root-run Qt installers).
globals_path=root/'etc/skel/.config/kdeglobals'
with globals_path.open('a') as stream:
    stream.write('\n'+scheme[scheme.index('[Colors:'):])
# Populate system-wide defaults too, while preserving user overrides.
for name in ['kdeglobals', 'kwinrc', 'kcminputrc', 'ksplashrc', 'baloofilerc', 'kxkbrc', 'plasmarc']:
    copy(root/'etc/skel/.config'/name, 'etc/xdg/'+name)
deploy(root)
