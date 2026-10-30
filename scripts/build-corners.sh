#!/bin/bash
# Build only on the x86_64 Trixie CI builder, against its matching KWin ABI.
set -euo pipefail
target=$(realpath "$1")
apt-get install -y --no-install-recommends cmake g++ gettext extra-cmake-modules \
  kwin-dev qt6-base-private-dev qt6-base-dev-tools libkf6configwidgets-dev \
  libkf6kcmutils-dev libkf6i18n-dev libepoxy-dev libxcb1-dev
source_dir=$(mktemp -d)
trap 'rm -rf "$source_dir"' EXIT
curl --fail --location --retry 3 \
  https://github.com/matinlotfali/KDE-Rounded-Corners/archive/refs/tags/v0.7.2.tar.gz \
  -o "$source_dir/source.tar.gz"
printf '%s  %s\n' 0a58fa41a9bb5e4ac33ddbe50973138d7189cb3393aa718cd83792b047c2e4f0 "$source_dir/source.tar.gz" | sha256sum -c -
tar -xzf "$source_dir/source.tar.gz" -C "$source_dir"
cmake -S "$source_dir/KDE-Rounded-Corners-0.7.2" -B "$source_dir/build" \
  -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr
cmake --build "$source_dir/build" --parallel 2
DESTDIR="$target" cmake --install "$source_dir/build"
install -D -m644 "$source_dir/KDE-Rounded-Corners-0.7.2/LICENSE" \
  "$target/usr/share/doc/pkos/third-party/rounded-corners-LICENSE"
