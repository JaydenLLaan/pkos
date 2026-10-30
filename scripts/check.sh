#!/bin/bash
set -euo pipefail
while IFS= read -r path; do
  case "$(head -n1 "$path")" in
    '#!/bin/bash'*) bash -n "$path" ;;
    '#!/bin/sh'*) sh -n "$path" ;;
  esac
done < <(find auto scripts config/hooks config/includes.chroot/usr/local -type f)
shellcheck -S error auto/config scripts/*.sh config/hooks/live/*.hook.chroot \
  config/includes.chroot/usr/local/bin/pk-* config/includes.chroot/usr/local/sbin/pk-*
python3 - <<'PY'
from pathlib import Path
import ast, yaml, xml.etree.ElementTree as ET
for p in [*Path('calamares').rglob('*.conf'), *Path('calamares').rglob('*.desc'), Path('.github/workflows/build.yml')]:
    yaml.safe_load(p.read_text())
for p in Path('branding').rglob('*.svg'):
    ET.parse(p)
for p in Path('scripts').glob('*.py'):
    ast.parse(p.read_text())
print('Shell, YAML, Python and SVG validation passed')
PY

