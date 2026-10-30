#!/bin/bash
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends sddm xvfb xauth imagemagick \
  librsvg2-bin fonts-inter qml6-module-qtquick-controls \
  qml6-module-qtquick-layouts qml6-module-qtqml-workerscript \
  qml6-module-qtquick-window qml6-module-qt5compat-graphicaleffects
useradd -m -u 1000 -s /bin/bash pkos
# SessionModel uses this directory's existence to list Wayland sessions;
# software rendering below needs no physical GPU for the preview fixture.
mkdir -p /dev/dri /tmp/pkos-theme /usr/share/wayland-sessions /usr/share/wallpapers/pkos-slate/contents/images
cp branding/sddm/* /tmp/pkos-theme/
rsvg-convert -w 320 branding/wordmark.svg -o /tmp/pkos-theme/wordmark.png
rsvg-convert -w 2560 -h 1440 branding/wallpapers/slate.svg -o /usr/share/wallpapers/pkos-slate/contents/images/2560x1440.png
cat > /usr/share/wayland-sessions/plasma.desktop <<'EOF'
[Desktop Entry]
Name=Plasma (Wayland)
Exec=/bin/true
Type=Application
EOF
export QT_QUICK_BACKEND=software
export QT_QPA_PLATFORM=xcb
xvfb-run -a -s '-screen 0 1280x800x24' bash -c '
  sddm-greeter-qt6 --test-mode --theme /tmp/pkos-theme >test-results/sddm-preview.log 2>&1 &
  greeter_pid=$!
  sleep 5
  import -window root test-results/sddm-preview.png
  kill "$greeter_pid" 2>/dev/null || true
  wait "$greeter_pid" 2>/dev/null || true
'
cat test-results/sddm-preview.log
! grep -Ei 'Unexpected token|theme cannot be loaded|Failed to load.*theme|Main.qml:[0-9]+:[0-9]+:' test-results/sddm-preview.log
