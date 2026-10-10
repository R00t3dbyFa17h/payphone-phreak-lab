# ATA provisioning notes

Quick reference for registering an **ATA (FXS)** to this lab's Asterisk. The
FXS port powers your analog payphone/handset and speaks SIP to the PBX.

## Credentials to use
From `asterisk/etc/pjsip.conf` (defaults — change before the event):

| Device | SIP user | Password | Caller ID |
|:--|:--|:--|:--|
| Payphone | `payphone` | `phreak-payphone` | 1955 |
| Operator | `operator` | `phreak-operator` | 0 |
| Team 1–4 | `team1`..`team4` | `phreak-team1`.. | 101..104 |

SIP server = the **PBX host LAN IP**, transport **UDP/5060**, codec **PCMU/PCMA**.

## Grandstream HT801 / HT802
Web UI → **FXS PORT**:
- Primary SIP Server: `<PBX IP>`
- SIP User ID / Authenticate ID: `payphone`
- Authenticate Password: `<payphone password>`
- SIP Transport: UDP
- Preferred Vocoder 1/2: PCMU / PCMA
- Dial Plan: `{ x+ | \+x+ | *x+ }` (permissive, so 2600/9999/etc. all dial)
- Enable Pulse Dialing: **Yes** *(only if the phone is rotary)*
- NAT Traversal: No (same LAN)

**BASIC SETTINGS** → set a static IP or DHCP reservation so it's predictable.

Apply → Reboot. Verify on the PBX:
```bash
docker exec -it phreak-pbx asterisk -rx "pjsip show aors"
docker exec -it phreak-pbx asterisk -rx "pjsip show contacts"
```

## Cisco/Linksys SPA112 / Obihai OBi302
Same idea under **Voice → Line 1**:
- Proxy: `<PBX IP>`
- User ID: `payphone`  /  Password: `<payphone password>`
- Preferred Codec: G711u
- Dial Plan: `(x+)` or leave default permissive.

## Dialing quirks
- If short codes (like `0`) don't send, loosen the ATA **Dial Plan** or press
  `#` to force-send.
- Inter-digit timeout too short? Raise it so people have time on the stiff
  payphone keypad.
- Rotary payphone + ATA without pulse support → add a **Dialgizmo** (pulse→DTMF)
  in line, or a **Rotatone** module inside the phone.

## Sanity test (no CTF)
With an HT802, plug a normal handset into FXS **2** as `team1`, the payphone
into FXS **1** as `payphone`, and call `101` ↔ `1955` to confirm two-way audio
and ringing before you rely on the dialplan.
