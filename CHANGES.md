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

## Future changes

Append dated changes, affected files, build run and verification here.

