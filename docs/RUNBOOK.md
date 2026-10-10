# Day-of runbook

## T-minus 1 week
- [ ] Build the images on the event laptop (`make build`) so you're not
      pulling Docker layers on venue wifi.
- [ ] `make challenge-audio` and rebuild the PBX image.
- [ ] Change SIP passwords (`pjsip.conf`) and `SCOREBOARD_TOKEN`.
- [ ] Provision the payphone's ATA (see HARDWARE.md); test an end-to-end flag.
- [ ] Print **CHALLENGES.md** (players) and **this** + **ORGANIZER_ANSWERS.md**
      (staff only).

## T-minus 1 hour (on site)
- [ ] Switch + PBX host powered; note the host LAN IP.
- [ ] `make up`; confirm scoreboard on the projector (`http://<ip>:8080`).
- [ ] Payphone registered: `docker exec -it phreak-pbx asterisk -rx "pjsip show aors"`.
- [ ] Hang a few softphone tablets/laptops as team stations (team1..team4),
      or let people register their own.
- [ ] Smoke test: dial `100`, `2600`, submit a flag at `700`, see the board move.
- [ ] Reset the board: `docker compose down && docker volume rm payphone-phreak-lab_scoreboard-data && docker compose up -d`.

## Kickoff (5 min talk)
1. Run the **Phreaking 101** mini-talk (docs/PHREAKING_101.md).
2. Explain scoring: dial **700**, team #, flag. Dupes don't double. Dial **200**
   to hear your score. Operator is **0**.
3. Point at the payphone: "that's a real one, wired to our own switch — go."

## During
- Watch the board; if a team is stuck, use the **hint ladder** in the answer key.
- The payphone is the crowd magnet — rotate people through it; put an easy
  challenge (CH2) as the "everyone gets one" on it.
- If the PBX gets wedged: `docker compose restart pbx` (scores persist).

## Common fixes
| Problem | Fix |
| :--- | :--- |
| No dial tone on payphone | ATA lost registration → reboot ATA; check `pjsip show aors`. |
| Flags not scoring | Token mismatch or scoreboard down → `make logs`. |
| Board frozen | It polls every 5s via JS; reload the tab; check scoreboard container. |
| Audio choppy on wifi | Put PBX + phones on **wired** switch; wifi RTP is rough. |

## Teardown
- [ ] Screenshot the final board for the group chat / write-up.
- [ ] `make down`.
- [ ] Reclaim the payphone, ATA, switch, cables.

## Nice-to-haves for next time
- Record custom prompt audio (a gravelly "operator" voice is a hit).
- Add a CH for **wardialing** lore (a bank of extensions that "answer" with
  modem/fax sounds — pure theatre).
- A physical **beige box** demo station (your own line only!) for show-and-tell.
