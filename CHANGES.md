# pkOS changes

## 1.0 — 2026-10-30

- Initial Trixie amd64 hybrid live/installer image and privileged GitHub build.
- Minimal Plasma 6 Wayland, slate-blue branding, three wallpapers and complete
  fresh-user, SDDM, Plymouth and GRUB defaults.
- Intel display, NVIDIA DKMS/PRIME and a separate Intel fallback boot option.
- Calamares GPT/EFI/ext4 erase-disk installation, optional LUKS and swap file.
- Coding tools, optional VSCodium, first-login AI/Rust/Ollama setup and docs.
- Automated OVMF live boot verification and diagnostic artifacts.

### Release verification — 2026-10-30

- Clean x86_64 build and full verification passed in [Actions run 41002329323](https://github.com/JaydenLLaan/pkos/actions/runs/41002329323), image source commit `2d99672100e85f9bcba322486592dfee1a10d6fe`.
- Verified raw USB UEFI live boot, Plasma Wayland, the packaged SDDM theme
  without fallback, Calamares erase-disk installation, and installed UEFI boot
  with the live USB detached. Checked sudo, active swap, GB keyboard and removal
  of live-only launchers. NVIDIA DKMS compiled for the shipped kernel.
- Versions: Linux 6.12.113, Plasma 6.3.6, NVIDIA 550.163.01, Calamares 3.3.14.
- ISO: `pkos.iso`, 1,947,598,848 bytes. Downloaded using `gh run download` and
  verified on macOS with `shasum -a 256 -c pkos.iso.sha256`.
- SHA256: `e4c4c7543b45c817f3e097bdcc7a7ab3ec93338a5ef0c31af4703e60b9f21e46`.
- Acer hardware checks and the optional encrypted-install variant remain on
  the manual acceptance checklist in `TESTING.md`; no physical Acer testing
  was performed by CI.

## Desktop restyle — 2026-10-30

- Unified dark slate palette, Inter / JetBrains Mono and Papirus-Dark icons.
- 28px top bar with wordmark, tray and clock; centred fit-content dock with
  five pinned applications, running dots and no automatic hiding/global menu.
- Original Aurorae decoration with left circle controls, thin borders and
  12px corners; pinned, source-built GPL rounded-corner effect for client areas.
- Matched Qt, GTK, Firefox, VSCodium, Kitty, SDDM, Calamares, GRUB and Plymouth.
- Removed cropped wallpaper watermark in favour of a quiet top-left wordmark.
- Expanded existing real-ISO boot/install checks with layout assertions and
  an installed Kitty/VSCodium workspace capture. Hardware/software functions
  and installer flow are retained.
- Follow the editor package's canonical desktop ID so its running window
  groups with the pinned dock icon after the upstream desktop-entry rename.

### Restyle release verification — 2026-10-30

- Clean x86_64 build and full tests passed in [Actions run 41070305797](https://github.com/JaydenLLaan/pkos/actions/runs/41070305797),
  image source `d2b360634423df973693467d25d02db1f1b2436c`.
- The identical ISO passed the complete suite again in [run 41073360494](https://github.com/JaydenLLaan/pkos/actions/runs/41073360494),
  with the final 1920×1080 live, installed workspace, login and installer captures.
- Verified raw USB UEFI boot, Plasma Wayland, NVIDIA DKMS, both panels, Calamares
  erase-disk installation, installed boot with the USB detached, sudo, swap,
  GB keyboard, empty installed desktop and active 12px corner effect.
- Kitty and VSCodium opened together; the editor groups with its pinned icon.
  Screenshot-only sample files and wallet-wizard dismissal remain in the test VM.
- ISO: 1,975,844,864 bytes, downloaded with `gh run download` and verified locally.
- SHA256: `b8739d60c135cc75bb937c6485683be4d9de4ca8c86b04848ff4868085149853`.
- Physical Acer checks and optional encrypted-install acceptance remain manual,
  as before. The base system, drivers, tools and installer options are retained.

## Future changes

Append dated changes, affected files, build run and verification here.

