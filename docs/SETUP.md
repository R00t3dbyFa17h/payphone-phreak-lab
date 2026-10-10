# Setup

`payphone-phreak-lab` runs as two Docker containers: the **Asterisk PBX** and
the **Flask scoreboard**. You need a Linux host (a laptop, NUC, or Pi 4/5 is
plenty) on the same LAN as your phones/ATA.

## 1. Prerequisites

- Docker + Docker Compose plugin (`docker compose version`).
- A flat LAN (one subnet) for the PBX, phones, and the payphone's ATA.
- Softphone apps for testing: **Linphone**, **Zoiper**, or **MicroSIP**.

> **Why host networking?** SIP + RTP are notoriously NAT-unfriendly. The
> provided `docker-compose.yml` uses `network_mode: host` so signalling and
> audio "just work" on a flat meetup LAN. If you must use bridged networking,
> read §6.

## 2. Configure before the event

1. **Change the SIP passwords** in `asterisk/etc/pjsip.conf` (the `password =`
   lines). Defaults are intentionally weak placeholders.
2. **Change the shared token** `SCOREBOARD_TOKEN` in `docker-compose.yml`
   (both services must match). The AGI uses it to post scores.
3. (Optional) **Record custom prompts** into `asterisk/sounds/` — see that
   folder's `README.md`. The game works without them.
4. **Generate the CH5 audio:** `make challenge-audio` (writes
   `asterisk/sounds/dtmf-challenge.wav`).

## 3. Bring it up

```bash
make build      # or: docker compose build
make up         # or: docker compose up -d
make logs       # follow the Asterisk console + scoreboard
```

Find the host's LAN IP (`ip -4 addr`), e.g. `192.168.1.50`.

- Scoreboard → `http://192.168.1.50:8080`
- SIP registrar → `192.168.1.50:5060`

## 4. Register a softphone (test)

In Linphone/Zoiper create an account:

```
Username:  team1
Password:  (whatever you set in pjsip.conf)
Domain:    192.168.1.50
Transport: UDP
```

Dial **100** — you should hear the menu. Dial **2600**, then **700** to submit
the flag it reads you (team `1`). Watch the scoreboard update.

## 5. Seed teams (optional)

Teams auto-create on first flag submit, but you can pre-register names:

```bash
curl -s http://192.168.1.50:8080/api/team -H 'Content-Type: application/json' \
  -d '{"token":"<your token>","team":"7","name":"The Phone Losers"}'
```

## 6. Bridged networking (advanced)

If you can't use host networking:

1. In `docker-compose.yml` remove `network_mode: host` from the `pbx` service
   and uncomment the `ports:` block (5060/udp + 10000-10099/udp).
2. In `asterisk/etc/pjsip.conf` set on `[transport-udp]`:
   ```
   external_media_address = <host-LAN-IP>
   external_signaling_address = <host-LAN-IP>
   local_net = 192.168.0.0/16
   ```
3. Do the same for the scoreboard service (`ports: ["8080:8080"]`) and set
   `SCOREBOARD_URL` on the PBX to the reachable address.

## 7. Reset the scoreboard between rounds

```bash
docker compose down
docker volume rm payphone-phreak-lab_scoreboard-data
docker compose up -d
```

## 8. Troubleshooting

| Symptom | Fix |
| :--- | :--- |
| Phone won't register | Firewall on 5060/udp? Right domain/IP? Password match pjsip.conf? |
| One-way / no audio | RTP blocked — open 10000-10099/udp, or use host networking. |
| Flags never score | Token mismatch (PBX vs scoreboard), or scoreboard URL wrong. Check `make logs`. |
| CH5 line silent | Run `make challenge-audio` then `docker compose build pbx && docker compose up -d`. |
| Asterisk CLI | `docker exec -it phreak-pbx asterisk -rvvv` then `dialplan show from-phones`. |
