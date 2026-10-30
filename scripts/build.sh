#!/bin/bash
set -Eeuo pipefail
cd /work
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends \
  live-build debootstrap squashfs-tools xorriso grub-efi-amd64-bin \
  grub-pc-bin grub-common syslinux syslinux-common isolinux mtools dosfstools \
  ca-certificates curl gnupg cpio file rsync python3 python3-yaml \
  librsvg2-bin imagemagick fontconfig fonts-inter fonts-jetbrains-mono \
  shellcheck git
bash scripts/check.sh
mkdir -p .build dist
rsync -a --delete auto/ .build/auto/
rsync -a --delete config/ .build/config/
install -d .build/config/includes.chroot/etc/calamares
cp -a calamares/. .build/config/includes.chroot/etc/calamares/
python3 scripts/assets.py .build/config/includes.chroot
install -D -m644 README.md .build/config/includes.chroot/usr/share/doc/pkos/README.md
install -D -m644 TESTING.md .build/config/includes.chroot/usr/share/doc/pkos/TESTING.md
chmod +x .build/auto/config .build/config/hooks/live/*.hook.chroot
find .build/config/includes.chroot/usr/local/bin .build/config/includes.chroot/usr/local/sbin -type f -exec chmod 755 {} +
chmod 755 .build/config/includes.chroot/etc/skel/Desktop/*.desktop
cd .build
lb config
lb build
ISO=$(find . -maxdepth 1 -name '*.hybrid.iso' -o -maxdepth 1 -name '*.iso' | head -n1)
test -n "$ISO"
cp "$ISO" ../dist/pkos.iso
cd ../dist
sha256sum pkos.iso > pkos.iso.sha256
xorriso -indev pkos.iso -report_el_torito plain -report_system_area plain > iso-layout.txt 2>&1
grep -q 'UEFI' iso-layout.txt
cp ../.build/chroot/usr/share/pkos/package-manifest.txt package-manifest.txt
cp ../.build/chroot/usr/share/pkos/build-info.json build-info.json
stat -c 'ISO size: %s bytes' pkos.iso
if [ "$(stat -c %s pkos.iso)" -gt 2500000000 ]; then
  echo 'Size goal exceeded: required desktop, NVIDIA and dev stack retained.'
fi

