# Hardware: wiring the payphone (and other phones) to the PBX

This lab is pure SIP, so **anything that speaks SIP, or an analog phone behind
an ATA, can join**. Below are the common ways to connect your **payphone**,
easiest first. Pick the one that matches the gear you have.

> ⚠️ **Mains/ringer voltage:** real phone lines ring at ~90 VAC and idle at
> ~48 VDC. ATAs generate this to drive the bell. Don't poke the FXS terminals
> while it's ringing. Keep everything low-voltage/isolated; you're not
> connecting to the real telco line.

---

## Option A — Analog payphone → **ATA (FXS)** → PBX  *(recommended)*

An **ATA** (Analog Telephone Adapter) has one or more **FXS** ports (the kind
that powers a phone) and registers to Asterisk over SIP. This is the standard,
reliable path.

**Known-good ATAs:** Grandstream **HT801** (1 port) / **HT802** (2 port),
Cisco/Linksys **SPA112**, Obihai **OBi302**.

### Wiring
```
[ Payphone ]  --tip/ring (RJ11)-->  [ ATA FXS port ]  --Ethernet-->  [ LAN ]  <-- PBX host
```
- Most single-slot/"COCOT" payphones expose **Tip** and **Ring** on a terminal
  block or an RJ11. Connect those two to the ATA's **Line/Phone (FXS)** port.
- Polarity usually doesn't matter for voice; if the phone behaves oddly, swap
  tip/ring.

### Provision the ATA (Grandstream HT80x example)
Log into the ATA's web UI → **FXS Port** tab:

| Setting | Value |
| :--- | :--- |
| Primary SIP Server | `<PBX-host-IP>` (e.g. 192.168.1.50) |
| SIP User ID / Auth ID | `payphone` |
| Auth Password | *(the `payphone` password from `pjsip.conf`)* |
| SIP Transport | UDP |
| Preferred Vocoder | PCMU (ulaw) then PCMA (alaw) |
| NAT Traversal | No (same LAN) |

Save/Apply/Reboot. The ATA should register; confirm on the PBX:
```bash
docker exec -it phreak-pbx asterisk -rx "pjsip show aors"
docker exec -it phreak-pbx asterisk -rx "pjsip show registrations"
```
Lift the payphone handset → you should hear the lab. More knobs in
[`tools/provision_ata.md`](../tools/provision_ata.md).

### Payphone quirks
- **Coin/charge-a-call logic:** many payphones expect line-side "coin" signals
  from a Central Office to allow a call. For a meetup lab you usually want the
  phone to **dial freely**. Two paths:
  1. Many COCOT/"non-coin" or hotel-style payphones dial normally off an ATA
     already.
  2. For true coin phones, set them to **"free"/"no-coin"/dial-tone-first**
     service mode (varies by make — Protel/Elcotel programming, or a hardware
     strap). Historically, making a payphone give free calls on the *real*
     network was the "red box" trick — **here we just configure our own phone
     on our own ATA; no fraud involved.** See PHREAKING_101 for the history.
- **Rotary-only payphone?** Enable pulse-dial decoding on the ATA (HT80x:
  *FXS → Enable Pulse Dialing*), or add an in-line pulse-to-DTMF converter
  (e.g. "Dialgizmo"), or a Rotatone module inside the phone.

---

## Option B — Analog payphone → **FXS card** in the PBX box

If you'd rather not use an external ATA, put an FXS interface in the host:

- **USB FXS:** an analog ATA in a dongle (still SIP, same as Option A really),
  or a **SIP DECT/Grandstream** base.
- **PCIe FXS:** a Digium/Sangoma analog card with **DAHDI** + `chan_dahdi`.
  This needs DAHDI drivers on the host and passthrough into the container
  (`--device`), plus `chan_dahdi.conf`. Heavier; only worth it if you already
  own the card. The ATA route (A) is far simpler for an event.

---

## Option C — A **SIP payphone** / SIP phone directly

Some modern/retrofit payphones and most desk phones speak SIP natively. Just
register them like a softphone:

```
User:   payphone   (or team1..team4)
Pass:   <from pjsip.conf>
Server: <PBX-host-IP>
```

---

## Option D — Line-powered / "no PBX config" bell test

To just make the payphone **ring and talk to one other handset** without the
CTF, plug two analog phones into a 2-port ATA (HT802) and dial between the two
FXS extensions. Good for a wiring smoke-test before the event.

---

## Shopping list (typical)

- [ ] Payphone (you have this ✔)
- [ ] ATA with FXS: Grandstream **HT802** (2 ports lets you add a handset too)
- [ ] RJ11 cable + a few spade/terminal connectors for tip/ring
- [ ] Small Ethernet switch + cables for the lab LAN
- [ ] Linux mini-PC/Pi to run Docker
- [ ] (Optional) Rotatone / Dialgizmo if the phone is rotary
- [ ] (Optional) A couple of cheap SIP desk phones or softphone tablets for teams

## Verify end-to-end

1. `make up` on the host.
2. ATA registered (`pjsip show aors`).
3. Payphone off-hook → hear menu (dial **100**).
4. Dial **2600**, then **700**, submit team `1` + the flag → scoreboard ticks.

You're phreaking on real brass. 🤙
