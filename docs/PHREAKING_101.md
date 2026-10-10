# Phreaking 101 — a meetup primer

A ready-to-present walkthrough of phone-phreaking history and mechanics, each
mapped to a challenge in this lab. Talk for ~20 minutes, then turn people
loose on the phones.

> **Framing for the room:** phreaking is the original hacking — curiosity about
> how a giant, mostly-undocumented system *actually* worked. The network has
> changed completely since; almost nothing here works on the real PSTN anymore.
> We study it because the *ideas* — enumeration, default creds, signalling
> trust, test interfaces — are exactly the ideas we use in modern security.

---

## 1. The network as a computer

The 20th-century phone network was a planet-sized state machine controlled by
**tones and timing**. Early switches trusted **in-band signalling**: the same
audio channel that carried your voice also carried the *control* messages that
told switches what to do. If you could make the right sounds, you could talk to
the switch itself. That trust boundary failure is the root of classic phreaking
— and it rhymes with every "control plane over the data plane" bug since.

## 2. 2600 Hz and the blue box  → **CH2 (dial 2600)**

- A **2600 Hz** tone meant "this trunk is idle" (supervision). Play it on an
  in-progress long-distance call and the far switch thought you'd hung up —
  while you still held the line, now in operator/signalling mode.
- **John Draper ("Captain Crunch")** found a toy whistle from Cap'n Crunch
  cereal produced a near-perfect 2600 Hz. Hence the name of a certain magazine
  and a certain hacker ethos.
- A **blue box** generated 2600 Hz **plus MF digits** (see below) to route your
  own free long-distance calls by impersonating the operator/trunk signalling.
- **Why it's dead:** modern networks moved control **out of band** (SS7, and
  now SIP/Diameter on carrier cores). There is no 2600 Hz backdoor on a digital
  trunk. We play the tone here for the history.

## 3. MF vs DTMF — two different tone languages

- **DTMF** ("Touch-Tone", the sounds your keypad makes) is **subscriber**
  signalling: it tells *your* switch which digits you dialed. Each key = a pair
  of a **low** and **high** frequency. Still used everywhere (IVRs, this lab).
  → **CH5 (dial 322)**: decode a Touch-Tone burst.
- **MF (R1)** was **inter-office** signalling between switches — a *different*
  set of tone pairs, wrapped in **KP** (start) and **ST** (stop). Blue boxes
  spoke MF. → `tools/tone_generator.py mf KP1234ST` to hear it.
- Teaching beat: same idea (tones = commands), different layer. DTMF = user↔
  switch; MF = switch↔switch. Phreaks abused the fact that end users could
  inject the *switch↔switch* language.

## 4. Enumeration & the unlisted line  → **CH1 (dial 411)**

Phreaks mapped exchanges by **scanning** — dialing every number in a block to
see what answered (the ancestor of port scanning; "wardialing", later immortal­
ized by the movie *WarGames* and tools like ToneLoc). Operators and directory
assistance leaked structure. In the lab, Directory Assistance lists most lines
but hides one — a nod to the **October 1971 *Esquire*** article *"Secrets of the
Little Blue Box"* that put phreaking on the map. Scan the keypad; find the year.

## 5. DISA & default creds  → **CH3 (767)**, **CH4 (5000)**

- **DISA** (Direct Inward System Access) let employees dial into a company PBX
  from outside and get **dial tone** as if inside — protected by a PIN. Weak or
  default PINs meant strangers could place calls on the company's dime
  ("toll fraud"). This is literally "exposed admin interface + weak password,"
  decades early.
- **Voicemail** systems shipped with **default PINs** (often = the mailbox
  number). Whole scandals (and some famous ones) rode on "the PIN was 1234."
- Lesson for the room: the oldest bug in the book still tops the OWASP charts.

## 6. Test lines: milliwatt, ANAC, loop-arounds  → **CH7 (600/9999)**, **CH8 (958)**

Telcos built **test numbers** for technicians — and phreaks loved them:

- **Milliwatt (1004 Hz)** — a steady reference tone at a known level for
  measuring line quality ("quiet termination"). → dial **600**.
- **ANAC** (Automatic Number Announcement Circuit) — reads back **your own**
  number. Invaluable when you didn't know a line's real digits (e.g. a beige-box
  tap, or an unmarked jack). → dial **958**.
- **Loop-arounds** — two numbers that, when two people called each, connected
  them: a free, anonymous meet-me bridge. The great phreak social network.

## 7. Red boxes & payphones (history, not a how-to)

A **red box** mimicked the **coin-deposit tones** a payphone sent to the
Central Office, fooling it into thinking you'd dropped quarters — stealing calls
from the carrier. **We don't do that here.** In this lab the payphone is *ours*,
wired to *our* ATA, configured to dial freely because we own it — no CO, no
fraud, no victim. The teaching point is the same signalling-trust flaw as 2600
Hz: the CO trusted tones the *endpoint* could forge. Modern payphones and the
PSTN don't accept these tones.

## 8. Ethics — say this out loud

- Everything tonight runs on **our own PBX and our own payphone**. That's the
  line: **your gear, or explicit written authorization — nothing else.**
- The skills transfer straight to **authorized** security work: enumeration,
  credential hygiene, protecting management/test interfaces, and not trusting
  the data plane for control.
- Phreak culture at its best was **curiosity + sharing knowledge responsibly**.
  Keep that; drop the toll fraud (it was a felony then and now).

## 9. Hands-on map

| Concept | Challenge | Dial |
| :--- | :--- | :--- |
| 2600 Hz / blue box history | CH2 | `2600` |
| Enumeration / unlisted lines | CH1 | `411` |
| MF vs DTMF (decode) | CH5 | `322` |
| DISA / exposed admin + weak PIN | CH3 | `767` |
| Default voicemail creds | CH4 | `5000` |
| IVR mapping | CH6 | `6000` |
| Milliwatt test line | CH7 | `600` → `9999` |
| ANAC (know thyself) | CH8 | `958` |
| Submit flags | — | `700` |

## Further reading / listening

- *Exploding the Phone* — Phil Lapsley (the definitive phreaking history).
- *"Secrets of the Little Blue Box"* — Ron Rosenbaum, *Esquire*, Oct 1971.
- *2600: The Hacker Quarterly*.
- The movie *WarGames* (1983) for the wardialing vibe.
