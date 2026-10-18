#!/usr/bin/env bash
# Jalankan cross-check test C<->Python (dulu di repo tests/).
# Butuh: repo di ../../asv usluk-usluk (symlink app/core/config/weights di sini),
#        python .venv repo, dan gcc untuk kompilasi C sementara.
set -euo pipefail
cd "$(dirname "$0")"

PY="${PY:-../../asv usluk-usluk/.venv/bin/python3}"
if [ ! -x "$PY" ]; then
  echo "python tak ditemukan: $PY (set PY=... atau setup repo dulu)" >&2
  exit 1
fi

exec "$PY" -m unittest discover -s tests -p 'test_core_*.py' -v
