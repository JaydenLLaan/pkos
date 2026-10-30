#!/bin/bash
set -euo pipefail
apt-get install -y --no-install-recommends qml6-module-org-kde-ksvg python3
python3 - <<'PY'
import sys
from pathlib import Path
sys.path.insert(0,'scripts')
from design import frame,svg
Path('/tmp/pkos-frame.svg').write_text(svg(frame('decoration')))
PY
cat > /tmp/pkos-theme/Main.qml <<'QML'
import QtQuick
import org.kde.ksvg as KSvg
Rectangle {
    width: 1280; height: 800; color: "#10151b"
    KSvg.FrameSvgItem {
        x: 320; y: 120; width: 640; height: 480
        imagePath: "/tmp/pkos-frame.svg"
        prefix: "decoration"
        Text { anchors.centerIn: parent; text: "pkOS · frame rendering"; color: "#edf2f7"; font.family: "Inter"; font.pixelSize: 24 }
    }
}
QML
xvfb-run -a -s '-screen 0 1280x800x24' bash -c '
  sddm-greeter-qt6 --test-mode --theme /tmp/pkos-theme >test-results/frames-preview.log 2>&1 &
  greeter_pid=$!
  sleep 5
  import -window root test-results/frames-preview.png
  kill "$greeter_pid" 2>/dev/null || true
  wait "$greeter_pid" 2>/dev/null || true
'
cat test-results/frames-preview.log
! grep -Ei 'Unexpected token|theme cannot be loaded|Failed to load.*theme|Main.qml:[0-9]+:[0-9]+:' test-results/frames-preview.log
