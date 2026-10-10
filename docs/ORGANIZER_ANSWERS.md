# 🔑 Organizer answer key (SPOILERS)

Keep this off the projector. Flags are also in `asterisk/agi/flags.json`
(what the PBX validates) and points in `challenges/challenges.yaml`.

| # | Dial | Solution | Flag | Pts |
|:-:|:----:|:---------|:----:|:---:|
| CH1 | `411` → `1971` | DA hides one line. The hidden extension is **1971** (Esquire article year). Dialing 1971 reads the flag. | `448162` | 100 |
| CH2 | `2600` | Just call 2600; it reads the flag. | `262600` | 100 |
| CH3 | `767` | DISA PIN is **2600** (hinted by the 2600 lore). | `773355` | 200 |
| CH4 | `5000` | Mailbox **1337**, PIN **1337** (default creds). | `909042` | 150 |
| CH5 | `322` | Line plays DTMF for **314159**; decode it. The decoded digits **are** the flag. | `314159` | 200 |
| CH6 | `6000` | Maze path: **3 → 1 → 7**. | `867530` | 150 |
| CH7 | `600` then `9999` | 600 is the milliwatt tone; 9999 announces the flag. | `100461` | 100 |
| CH8 | `958` | ANAC reads caller's number, then the flag. | `580019` | 150 |

**Total: 1,150 points.**

## Changing flags / points
1. Edit `asterisk/agi/flags.json` (the source of truth the PBX checks).
2. Edit the `SayDigits(...)` lines in `asterisk/etc/extensions.conf` to match.
3. Update `challenges/challenges.yaml` + this table.
4. `docker compose build pbx && docker compose up -d`.

## Changing the DISA PIN / voicemail creds / maze path
- DISA PIN: `extensions.conf` context `[phreak-numbers]`, exten `767`, the
  `GotoIf($["${PIN}" = "2600"]...)` line.
- Voicemail: exten `5000`, the `MBOX`/`VPIN` compare.
- Maze: exten `6000`, the three `GotoIf` digit compares (`3`,`1`,`7`).

## Scoreboard admin
- Live board: `http://<host>:8080`
- JSON: `GET /api/board`
- Reset between rounds: `docker compose down && docker volume rm payphone-phreak-lab_scoreboard-data && docker compose up -d`
- Manually award/seed: `POST /api/score` with the shared token (see SETUP §5).

## Hint ladder (for helping stuck teams)
- **CH1:** "Directory didn't read you *every* number. What famous year matters
  to phreaks?" → "Try dialing that year."
- **CH3:** "What's the one number every phreak worships?" → PIN.
- **CH4:** "What's the laziest PIN an admin could pick for mailbox 1337?"
- **CH5:** "Those are Touch-Tones. You can *record* and *decode* them."
- **CH6:** "It's a maze. Keep a map. Only one path doesn't restart you."
