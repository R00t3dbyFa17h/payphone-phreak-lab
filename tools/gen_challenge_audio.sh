#!/usr/bin/env bash
# payphone-phreak-lab :: build the CH5 DTMF challenge audio.
# Generates asterisk/sounds/dtmf-challenge.wav encoding the flag 314159.
# Asterisk plays it on extension 322; players decode it with dtmf_decoder.py.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="${1:-$HERE/../asterisk/sounds/dtmf-challenge.wav}"
python3 "$HERE/tone_generator.py" dtmf 314159 --tone 0.22 --gap 0.12 -o "$OUT"
echo "[+] CH5 challenge audio written to: $OUT"
echo "    (rebuild the pbx image so Asterisk picks it up: docker compose build pbx)"
