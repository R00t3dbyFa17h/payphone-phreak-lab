# Challenge briefs (hand this to players)

Dial in, solve the puzzle, and each challenge reads you a **6-digit flag**.
Submit it at the **Flag Terminal: dial 700**, enter your **team number**, then
the **flag**. Score shows on the big board (or dial **200** to hear it).

**No spoilers here — just the hooks.** 8 challenges, 1,150 points total.

| # | Name | Dial | Pts | Hint |
|:-:|:-----|:----:|:---:|:-----|
| CH1 | Hidden Directory | `411` | 100 | DA won't read you *everything*. Phreak history, October **1971**. Scan. |
| CH2 | The 2600 Line | `2600` | 100 | The most famous number in phreaking. Just call it. |
| CH3 | DISA Misconfig | `767` | 200 | A maintenance port wants a 4-digit PIN. Lazy admins reuse folklore… |
| CH4 | Default Voicemail | `5000` | 150 | Some mailbox still has the factory PIN. What's the laziest possible PIN? |
| CH5 | DTMF Decode | `322` | 200 | It plays Touch-Tones. Record them. `tools/dtmf_decoder.py` is your friend. |
| CH6 | The Maze | `6000` | 150 | A menu with no prompts. Map it. One path wins; wrong turns restart you. |
| CH7 | Milliwatt | `600`→`9999` | 100 | A test tone. Learn what 1004 Hz is *for*, then dial 9999 to claim it. |
| CH8 | ANAC | `958` | 150 | It tells you who you are. Old-school line identification. |

### Submitting a flag
1. Dial **700**.
2. Enter your **team number** (e.g. `7`), press `#` or wait.
3. Enter the **6-digit flag**.
4. Hear "congrats" + your points. Dupes won't double-score.

### Tips
- Use a softphone with a **keypad you can mash** — some challenges reward
  poking at numbers that weren't announced.
- For CH5 you need to **record** the line. A softphone with call recording, or
  `tools/tone_generator.py`/`dtmf_decoder.py` on a captured WAV, both work.
- Stuck? The operator (**0**) and your friendly organizers are there to nudge.

*For the HTB meetup — have fun, stay legal, own the gear you touch.*
