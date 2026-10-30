# pkOS acceptance checks

## Automated CI evidence

- [ ] Shell/YAML/Python/SVG syntax validation passed.
- [ ] A clean amd64 Trixie live-build completed; SHA256 emitted.
- [ ] xorriso reports UEFI El Torito boot and a hybrid system area.
- [ ] NVIDIA DKMS compiled against every shipped kernel; `modinfo` works.
- [ ] The actual ISO booted as a raw USB mass-storage disk with OVMF, without Secure Boot.
- [ ] Live user can log in; Plasma and KWin Wayland are running.
- [ ] NetworkManager and SDDM are active; Bluetooth is enabled (VM has no radio).
- [ ] Desktop has the pkOS panel; screenshot saved as a diagnostic artifact.
- [ ] SDDM theme renders in its test mode, independently of desktop autologin.
- [ ] uv, Node, Go and Neovim run in the booted environment.
- [ ] Calamares completes an erase-disk install on a disposable 48 GiB disk.
- [ ] The installed disk boots with the ISO detached, into Plasma Wayland.
- [ ] Installed user has sudo, swap is active, EFI and root are mounted, and
      the live installer launcher is gone.

CI has no RTX 3050, Wi-Fi radio, trackpad or Acer firmware. A successful build
does not claim those physical checks have passed. Record observations below.

## Acer live session

- [ ] USB boots from F12 as UEFI with Secure Boot disabled.
- [ ] pkOS wordmark, splash, wallpaper, panel and welcome screen appear.
- [ ] Wayland: `echo "$XDG_SESSION_TYPE"` prints `wayland`.
- [ ] Installer launcher opens Calamares; no missing module errors.
- [ ] Keyboard defaults to GB; both laptop keyboard and USB input work.
- [ ] Trackpad tap/click, scroll and palm rejection work.
- [ ] Brightness and volume keys work; screen resolution/refresh are correct.
- [ ] Wi-Fi connects, reconnects and works after suspend; test `nmcli`.
- [ ] Bluetooth pairs with an actual device and reconnects.
- [ ] Speakers, headphones, microphone work through PipeWire.
- [ ] Suspend/resume works on AC and battery; test lid close too.
- [ ] `nvidia-smi` identifies the RTX 3050 Laptop without an error.
- [ ] `pk-gpu glxinfo -B` reports NVIDIA; ordinary apps use Intel.
- [ ] External HDMI/DP display works, if used; test unplug/replug.
- [ ] Intel fallback boot reaches a desktop with NVIDIA disabled.
- [ ] No Windows partition is mounted or changed by merely booting live.

## Installation (destroys selected disk)

- [ ] Backups complete; target NVMe model/size checked twice.
- [ ] Calamares defaults to Erase disk, ext4 and swap file.
- [ ] Full-disk warning and final confirmation are clear.
- [ ] Locale, timezone, keyboard and sudo account can be selected.
- [ ] Offline installation completes without needing repository access.
- [ ] GPT contains only pkOS EFI and root; old Windows/recovery partitions gone.
- [ ] Reboot without USB reaches GRUB and installed Plasma Wayland.
- [ ] Normal user has sudo; no live user's passwordless sudo remains.
- [ ] `/run/live/medium` is absent, and installed initramfs has no live boot.
- [ ] `findmnt /`, `findmnt /boot/efi`, `sudo swapon --show` look correct.
- [ ] NVIDIA works after installed boot and after a kernel update/reboot.
- [ ] Encryption variant: GRUB accepts passphrase, root unlocks and swap lives
      inside the encrypted root. No world-readable keyfiles/initramfs.
- [ ] A fresh additional user receives the same intended visual defaults.

## First-login setup

- [ ] Welcome offers setup once; About pkOS remains available.
- [ ] Offline setup explains network failure and can be rerun.
- [ ] `claude --version`, `codex --version`, `rustup show`, `ollama --version` work.
- [ ] Optional CUDA prompt can be skipped; installation works when selected.
- [ ] Optional model download can be skipped; `ollama run qwen2.5-coder:1.5b`
      works when downloaded (use a small prompt first).
- [ ] Git name/email can be set or skipped without overwriting existing values.
- [ ] Running `pk-setup` twice skips existing tools and preserves configuration.
- [ ] `podman run --rm docker.io/library/alpine echo ready` works without sudo.

## Results

Date / commit / hardware / test / result / notes:

