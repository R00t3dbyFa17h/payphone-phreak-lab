<h1 align="center">☎️ payphone-phreak-lab</h1>

<p align="center">
  <b>A self-hosted PBX + phone-phreaking CTF for your hacker meetup.</b><br>
  Plug in a real payphone, dial into a hacked-up 1980s phone network, and
  teach people how the phone system worked — and why phreaks loved it.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/PBX-Asterisk-orange?style=for-the-badge&logo=asterisk">
  <img src="https://img.shields.io/badge/Deploy-Docker-blue?style=for-the-badge&logo=docker">
  <img src="https://img.shields.io/badge/Scoreboard-Flask-lightgrey?style=for-the-badge&logo=flask">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge">
</p>

> *"He reveals deep and hidden things; he knows what lies in darkness..."* — **Daniel 2:22**

---

## 📞 What is this?

`payphone-phreak-lab` turns an [Asterisk](https://www.asterisk.org/) PBX into a
**capture-the-flag phone network** for a meetup (built for an **HTB meetup**).
Attendees pick up a handset — a softphone, or the **real payphone** you wired
up — and explore a retro phone system full of classic phreaking lore:
directory enumeration, the **2600 Hz** legend, **DISA** misconfigurations,
default voicemail PINs, **DTMF** decoding, IVR mazes, **milliwatt** test lines,
and **ANAC** "who am I?" numbers.

Each challenge yields a 6-digit **flag**. Dial the **Flag Terminal (700)**,
punch in your team number and the flag, and watch your score climb on the
**live scoreboard** projected on the wall.

Everything runs in Docker and against **your own equipment** — it's a safe,
legal, hands-on way to teach the history and mechanics of the phone network.

## 🧰 What's in the box

| Piece | What it does |
| :--- | :--- |
| **Asterisk PBX** (`asterisk/`) | The dialplan *is* the game. SIP for softphones + the payphone's ATA. |
| **Flag Terminal (ext 700)** | Players submit flags by phone; an AGI validates + scores. |
| **Scoreboard** (`scoreboard/`) | Flask + SQLite live board for the projector (`:8080`). |
| **Teaching tools** (`tools/`) | Pure-stdlib DTMF decoder + DTMF/MF/2600 tone generator. |
| **Docs** (`docs/`) | Full setup, **hardware wiring for the payphone**, challenge briefs, an organizer answer key, and a **Phreaking 101** teaching deck. |

## 🚀 Quickstart

```bash
git clone https://github.com/R00t3dbyFa17h/payphone-phreak-lab.git
cd payphone-phreak-lab

# (optional) build the CH5 Touch-Tone challenge clip
make challenge-audio

# bring up the PBX + scoreboard
docker compose up --build
```

- **Scoreboard:** http://&lt;host&gt;:8080
- **SIP:** `udp/5060` — register a softphone (e.g. Zoiper/Linphone) as
  `team1` … `team4` (passwords in `asterisk/etc/pjsip.conf` — **change them**).
- Dial **100** for the main menu, or jump straight to a challenge number.

Point the **payphone's ATA** at the PBX host and you're phreaking on real brass.
See **[docs/HARDWARE.md](docs/HARDWARE.md)**.

## 🗺️ The dial plan (player-facing)

| Dial | Line |
| :--- | :--- |
| `100` | Main menu / operator IVR |
| `411` | Directory Assistance *(CH1)* |
| `2600` | The 2600 line *(CH2)* |
| `767` | DISA port *(CH3)* |
| `5000` | Voicemail *(CH4)* |
| `322` | DTMF decode line *(CH5)* |
| `6000` | The Maze *(CH6)* |
| `600` / `9999` | Milliwatt test / flag *(CH7)* |
| `958` | ANAC — reads your number *(CH8)* |
| `700` | **Flag Terminal** — submit team# + flag |
| `200` | Hear your team's score |
| `0` | Operator |

Full briefs: **[docs/CHALLENGES.md](docs/CHALLENGES.md)** · Answer key (staff):
**[docs/ORGANIZER_ANSWERS.md](docs/ORGANIZER_ANSWERS.md)**.

## 🎓 Teaching

**[docs/PHREAKING_101.md](docs/PHREAKING_101.md)** is a ready-to-present primer:
the history (blue boxes, Cap'n Crunch, 2600 Hz, the Esquire '71 article), how
in-band MF signalling worked and why it was a security disaster, DTMF vs MF,
red boxes and payphones, test lines (milliwatt/ANAC/loop-arounds), and the
**ethics** — then it maps each concept to a challenge in this lab.

## ⚖️ Legal & Ethics

**For education and authorized use on your own lab only.** This project does
**not** attack, defraud, or interact with any real carrier or the public
switched telephone network. The 2600 Hz / blue-box / red-box material is
**historical** — modern networks use out-of-band SS7 signalling, so these
tones do nothing to real systems. Teach the history, teach the defenses, and
keep it on your own gear. See each doc's disclaimer.

---

<p align="center">
  Built with ☎️ and ✝️ by <b>R00t3dbyFa17h / K70n0s510</b> — for the HTB meetup crew.<br>
  <i>Rooted by Authority. Faith by Design. STAY R00t3d In Fa17h!!</i>
</p>
