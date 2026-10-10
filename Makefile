# payphone-phreak-lab :: convenience targets
.PHONY: help build up down logs ps challenge-audio test clean

help:
	@echo "payphone-phreak-lab"
	@echo "  make build            build PBX + scoreboard images"
	@echo "  make up               start the lab (detached)"
	@echo "  make down             stop the lab"
	@echo "  make logs             follow PBX + scoreboard logs"
	@echo "  make challenge-audio  (re)generate the CH5 DTMF clip"
	@echo "  make test             syntax/lint checks (no containers needed)"
	@echo "  make clean            remove local build cruft"

build:
	docker compose build

up:
	docker compose up -d
	@echo "Scoreboard: http://localhost:8080   SIP: udp/5060"

down:
	docker compose down

logs:
	docker compose logs -f

ps:
	docker compose ps

challenge-audio:
	bash tools/gen_challenge_audio.sh

test:
	@echo "[*] Python syntax..."
	python3 -m py_compile scoreboard/app.py asterisk/agi/*.py tools/*.py
	@echo "[*] JSON (flags.json)..."
	python3 -c "import json; json.load(open('asterisk/agi/flags.json')); print('  flags.json OK')"
	@echo "[*] docker-compose config..."
	@docker compose config >/dev/null 2>&1 && echo "  compose OK" || echo "  (docker not available here; skipped)"
	@echo "[*] self-test: generate + decode DTMF roundtrip..."
	python3 tools/tone_generator.py dtmf 314159 -o /tmp/_pplab_dtmf.wav >/dev/null
	python3 tools/dtmf_decoder.py /tmp/_pplab_dtmf.wav

clean:
	rm -f /tmp/_pplab_dtmf.wav
	find . -name __pycache__ -type d -prune -exec rm -rf {} + 2>/dev/null || true
