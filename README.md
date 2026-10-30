# pkOS

A quiet place to build. A minimal amd64 live Linux system with Plasma 6 on
Wayland, built for an Acer Nitro 5 (i7-12650H, RTX 3050 Laptop, UEFI).

## Get the ISO

The **Build pkOS** GitHub Actions workflow builds inside a privileged
`debian:trixie` x86_64 container on `ubuntu-latest`. Nothing is built on macOS.
Download the `pkos-iso` artifact from a successful run. It contains `pkos.iso`
and `pkos.iso.sha256`. The separate diagnostics artifact contains the package
manifest, build log, UEFI layout report and VM boot results/screenshots.

```sh
gh workflow run build.yml
gh run list --workflow build.yml
gh run watch RUN_ID --exit-status
gh run download RUN_ID --name pkos-iso --dir dist
cd dist
shasum -a 256 -c pkos.iso.sha256
```

Artifacts expire after 30 days. Keep your downloaded ISO or trigger a rebuild.
The repository is private; access requires your GitHub login.

## Flash from macOS

Use a USB stick of at least 8 GB. Flashing erases the USB. Disconnect other
external disks if that makes identifying the USB easier. **Run `diskutil list`
first and double-check the disk's capacity and device number.** Use the whole
disk (`diskN`), not a partition such as `diskNs1`.

```sh
cd /Users/jayden/pkos/dist
shasum -a 256 -c pkos.iso.sha256
diskutil list
# Replace N below with the USB disk number you have verified.
diskutil unmountDisk /dev/diskN
sudo dd if=pkos.iso of=/dev/rdiskN bs=4m
sync
diskutil eject /dev/diskN
```

`dd` is quiet while copying; press **Ctrl+T** for progress on macOS. Do not
disconnect the USB until it has been ejected. macOS may say the flashed USB
is unreadable; choose **Ignore**, do not initialize it.

Alternatively, open [balenaEtcher](https://etcher.balena.io/), choose **Flash
from file**, select `pkos.iso`, choose the verified USB, and flash/validate it.

## Acer firmware and live boot

1. Back up all personal files and any Windows recovery material you want to keep.
2. Connect AC power. Enter firmware with **F2** while powering on.
3. Disable **Secure Boot**. On some Acer firmware a temporary supervisor
   password is needed to unlock that option; record it and remove it afterward.
4. Use UEFI boot. Enable the **F12 Boot Menu** option.
5. If exposed, choose **AHCI** storage mode instead of Intel RST/VMD. On some
   Acer versions **Ctrl+S** on the Main tab exposes storage options. Do not
   change a setting the firmware does not offer. This change may stop the old
   Windows installation booting; pkOS replaces it.
6. Reboot with the USB inserted, press **F12**, and choose its **UEFI** entry.
7. Select **Try pkOS**. The live desktop logs in automatically. The live user
   is `pkos`, password `live`, with passwordless sudo. These credentials and
   live privileges are removed from the installed system.

Intel drives the desktop. Use **Try pkOS — Intel graphics fallback** if the
normal entry cannot reach a usable desktop. This disables NVIDIA modules for
that boot. Do not enable `nomodeset` as a routine workaround: Intel Wayland
needs kernel modesetting. The image has no forced NVIDIA Xorg configuration.

## Install

Open **Install pkOS** on the desktop or welcome screen. The installer works
offline. Choose language, timezone, keyboard, disk and your normal account.
Defaults are `en_GB.UTF-8`, Europe/London and GB keyboard.

**Erase disk is selected by default. It removes every partition on the selected
disk, including Windows, its EFI loader/recovery partitions and your files.**
Review the disk's model and size and the final partition summary. Click the
final confirmation only when it is the intended disk. Disconnect other disks
you do not want to risk selecting. Erasing recreates the partition table and
filesystems; it is not a forensic secure erase of every old SSD block.

The layout is GPT, a 512 MiB FAT32 EFI partition and one ext4 root partition,
plus a swap file. Optional encryption uses LUKS1 so GRUB can unlock an encrypted
root containing `/boot`. GRUB prompts for its passphrase at boot; the initramfs
contains a protected keyfile to avoid a second prompt. Keep a separate backup
of important data and the encryption passphrase. The EFI partition remains
unencrypted. Hibernation is not configured; ordinary suspend is supported.

Create a normal user with a password of at least eight characters; sudo uses
that password and root login is disabled. Desktop autologin is selected by
default and can be unchecked in the installer. For an encrypted installation,
the disk passphrase is still required at boot. GRUB is installed to the EFI
partition, with an additional removable EFI fallback for firmware compatibility.

When installation finishes, reboot and remove the USB when prompted. The
first-login welcome offers **Prepare your workspace**. It runs `pk-setup`,
which checks the network, installs Claude Code and Codex via user-local npm,
installs a minimal Rust toolchain and Ollama, offers CUDA and a small coding
model, and sets Git name/email. It is interactive, idempotent, logs to
`~/.local/state/pkos/setup.log`, and can be rerun after interrupted downloads.
Sign in to the AI tools yourself; no accounts, credentials or model weights
are baked into the ISO. Optional downloads can be large.

## Included tools

Plasma 6, SDDM, Dolphin, Kate, Kitty, Konsole, Firefox ESR, NetworkManager,
Bluetooth, PipeWire, power/brightness management, Inter and JetBrains Mono.
The pkOS slate palette uses `#10151b` backgrounds, `#17212b` surfaces,
`#8babc0` accents and `#edf2f7` text. A 28px top bar holds the wordmark, tray
and clock. A centred, floating dock fits its five pinned applications, stays
visible and marks running apps with a dot. Alt+Space opens application search;
there is no global menu. Window controls are on the left, with restrained
coloured circles, 12px corners and thin borders. Installed desktops are empty;
the live desktop has only the installer launcher.

Qt, GTK, Firefox, VSCodium, Kitty, SDDM, Calamares, Plymouth and GRUB share the
dark palette. Inter is the UI font and JetBrains Mono the code/terminal font.
Papirus-Dark is the icon family, with grey folders and slate-coloured pinned
icons; the terminal uses Papirus' plain terminal glyph. Breeze supplies the cursor.
Kitty is the default terminal, with a compact Git-aware prompt and a muted
dirty-worktree marker. Defaults are staged through `/etc/skel`, `/etc/xdg`,
system configuration and live-build hooks, so they apply to fresh installations.

Git, Neovim, tmux, Podman, Python, pipx, uv, Node/npm, Go, GCC, CMake, ripgrep,
fd (`fdfind`), fzf, bat (`batcat`), jq, curl, htop and btop are installed.
VSCodium is installed from the signed repository recommended by its project
when reachable; Kate is always available as the fallback editor. Neovim has
no network-fetched plugins. User package executables live under `~/.local/bin`.

The image includes Intel firmware/microcode, Wi-Fi/Bluetooth/audio firmware,
the proprietary NVIDIA driver and DKMS module compiled for its shipped kernel,
matching headers, Vulkan/Mesa and PRIME offload:

```sh
nvidia-smi
pk-gpu glxinfo -B
pk-gpu your-gpu-program
podman run --rm docker.io/library/alpine uname -a
```

Normal apps stay on Intel. External display wiring, suspend and GPU power
behaviour must be checked on the physical Nitro. Keep Secure Boot off; this
custom image and its DKMS module do not provide an enrolled Secure Boot chain.

## Build and maintain

The clean-clone build entry point is `scripts/build.sh`, executed by Actions.
It installs live-build, validates source syntax, stages sources under `.build`,
renders SVG assets with librsvg, creates the squashfs with xz, builds the hybrid
ISO and emits a SHA256. The runner then boots the actual ISO under QEMU/OVMF,
checks Plasma Wayland, services, tools and NVIDIA DKMS, and captures a screenshot
before publishing it. Hardware-only checks are in [TESTING.md](TESTING.md).

CI also drives Calamares through an erase-disk installation on a disposable
virtual disk, boots that disk with the ISO detached, and checks the installed
desktop, sudo account, EFI loader and swap. The live boot uses a raw virtual USB
device to exercise the hybrid image's USB boot path.
Design checks require two panels and the installed desktop to be empty. CI
captures the live desktop, packaged login theme, installer, installed desktop
and installed workspace with Kitty and VSCodium open. Screenshot-only sample
files and window positioning are confined to the disposable test machine.

The build targets the named Trixie suite and its security/updates repositories.
It is repeatable from a clean clone, but **not bit-for-bit reproducible**:
packages, container tags and optional vendor repositories receive updates.
Each artifact has the resolved versions in `package-manifest.txt` and
`build-info.json`. No private signing keys or secrets are required. The size
goal is under 2.5 GB; core GPU/development support is retained if it exceeds it.

| Location | Purpose |
| --- | --- |
| `auto/config` | live-build flags, release, boot arguments |
| `config/package-lists/` | explicitly selected packages |
| `config/includes.chroot/` | installed files, commands, user/system defaults |
| `config/hooks/live/` | editor/uv installation, DKMS, branding, cleanup |
| `branding/` | editable SVGs and Plasma/SDDM/GRUB/Plymouth themes |
| `calamares/` | installer flow, partitioning and branding |
| `scripts/` | build, validation, rendering and VM tests |
| `.github/workflows/build.yml` | x86_64 CI and artifact publication |
| `CHANGES.md` | append future changes here |

Change the relevant source, commit, push and inspect Actions. On failure use
`gh run view RUN_ID --log-failed`, fix the actual error, then push/re-run.
Do not run the privileged builder on the Apple Silicon Mac. To run on a
separate Linux amd64 build machine, mount this clone at `/work` in a privileged
`debian:trixie` container and execute `bash scripts/build.sh` there.

For a quick SDDM-only check, run `gh workflow run preview-sddm.yml`. That workflow
renders the source theme with Xvfb and software rendering inside a Trixie
container, rejects QML errors, and uploads `sddm-preview` with a PNG and log.
It builds no ISO and needs no physical GPU. The full ISO workflow separately
verifies the packaged theme in the booted live system.

After installation, update with `sudo apt update && sudo apt upgrade`. Keep
the kernel and NVIDIA module compatible and leave the matching headers
installed. Branding files use local dpkg diversions to preserve pkOS identity
across base-files upgrades. Review upstream release and security notes before
major suite changes.

## Technical references

- [Debian Live Manual](https://live-team.pages.debian.net/live-manual/html/live-manual.en.html)
- [Trixie live-build options](https://manpages.debian.org/trixie/live-build/lb_config.1.en.html)
- [Calamares 3.3.14 source/configuration](https://github.com/calamares/calamares/tree/v3.3.14)
- [NVIDIA on Debian](https://wiki.debian.org/NvidiaGraphicsDrivers)
- [VSCodium repository instructions](https://vscodium.com/#deb)
- [Codex CLI installation](https://developers.openai.com/codex/cli/)
- [Claude Code setup](https://code.claude.com/docs/en/setup)
- [Rustup](https://rustup.rs/), [Ollama Linux](https://docs.ollama.com/linux)

The base distribution's package metadata, repositories, copyright and license
files are preserved. User-facing pkOS artwork and configuration are original.

## Design licenses

- Original pkOS SVG artwork, Aurorae decoration, Plasma style, wordmark widget,
  GTK overrides and configuration: [MIT](LICENSE).
- [Papirus icon theme](https://github.com/PapirusDevelopmentTeam/papirus-icon-theme):
  GPL-3.0; shipped by the distribution package with its copyright notices.
  pkOS modifies pinned application SVG colours to a muted slate palette and
  selects the theme's grey folder variants. Original icon shapes are retained.
- [Breeze](https://invent.kde.org/plasma/breeze) and
  [Breeze GTK](https://invent.kde.org/plasma/breeze-gtk): KDE's open-licensed
  widget engine and GTK base; their installed package copyright files retain
  the component licenses. The pkOS decoration uses KDE's Aurorae engine.
- [KDE Rounded Corners](https://github.com/matinlotfali/KDE-Rounded-Corners),
  Rob and Matin Lotfaliei, GPL-3.0: v0.7.2, downloaded with a pinned SHA256 and
  compiled against Trixie's KWin in CI. Only 12px clipping is enabled; extra
  outlines and animation are disabled. Its license is installed under
  `/usr/share/doc/pkos/third-party/`. Build dependencies stay out of the ISO.
- [Inter](https://github.com/rsms/inter) and
  [JetBrains Mono](https://github.com/JetBrains/JetBrainsMono): SIL OFL-1.1.
  No proprietary platform artwork or fonts are included.

