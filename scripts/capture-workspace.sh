#!/bin/bash
set -euo pipefail
workspace="$HOME/Projects/workspace"
mkdir -p "$workspace"
cd "$workspace"
git init -q -b main
cat > main.py <<'PY'
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Workspace:
    name: str
    root: Path

    def describe(self) -> str:
        return f"{self.name}: ready to build"


def main() -> None:
    workspace = Workspace("pkOS", Path.cwd())
    print(workspace.describe())


if __name__ == "__main__":
    main()
PY
git add main.py
git -c user.name=pkOS -c user.email=preview@localhost commit -qm 'Start workspace'
printf '\n# Next: make something useful.\n' >> main.py
systemd-run --user --collect --unit=pkos-shot-terminal \
    kitty -o linux_display_server=x11 --class pkos-terminal --title Workspace \
    bash -c 'cd "$HOME/Projects/workspace"; clear; python3 main.py; printf "\n"; git status --short; printf "\n"; exec bash'
systemd-run --user --collect --property=ExitType=cgroup --unit=pkos-shot-editor \
    env ELECTRON_ENABLE_LOGGING=1 codium --verbose --enable-logging=stderr \
    --new-window --disable-gpu --ozone-platform=x11 --disable-workspace-trust \
    --skip-welcome --skip-release-notes "$workspace/main.py"
terminal_window=''
editor_window=''
for attempt in $(seq 1 90); do
    terminal_window=$(xdotool search --onlyvisible --class pkos-terminal 2>/dev/null | head -1 || true)
    editor_window=$(xdotool search --onlyvisible --name 'main.py' 2>/dev/null | head -1 || true)
    if [ -n "$terminal_window" ] && [ -n "$editor_window" ]; then break; fi
    sleep 1
done
test -n "$terminal_window"
test -n "$editor_window"
read -r screen_width screen_height < <(xdotool getdisplaygeometry)
editor_width=$((screen_width * 55 / 100 / 8 * 8))
editor_height=$((screen_height - 200))
terminal_width=$((screen_width - editor_width - 80))
terminal_height=$((screen_height - 248))
xdotool windowsize "$editor_window" "$editor_width" "$editor_height"
xdotool windowmove "$editor_window" "$((screen_width - editor_width - 24))" 88
xdotool windowsize "$terminal_window" "$terminal_width" "$terminal_height"
xdotool windowmove "$terminal_window" 24 136
xdotool windowactivate --sync "$terminal_window"
sleep 8
# The wallet wizard is native Wayland. Ask KWin to close that window only,
# without changing the installed wallet service or secure-storage defaults.
cat > /tmp/pkos-capture-wallet.js <<'JS'
for (const window of workspace.windowList()) {
    if (window.caption === "KDE Wallet Service") {
        window.closeWindow();
    }
}
JS
busctl --user call org.kde.KWin /Scripting org.kde.kwin.Scripting loadScript ss /tmp/pkos-capture-wallet.js pkos-capture-wallet
busctl --user call org.kde.KWin /Scripting org.kde.kwin.Scripting start
sleep 3
busctl --user call org.kde.KWin /Scripting org.kde.kwin.Scripting unloadScript s pkos-capture-wallet
xdotool windowactivate --sync "$terminal_window"
sleep 3
printf 'Workspace capture ready: Kitty %s, VSCodium %s\n' "$terminal_window" "$editor_window"
