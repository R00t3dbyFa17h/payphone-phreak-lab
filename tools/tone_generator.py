#!/usr/bin/env python3
"""payphone-phreak-lab :: tone_generator.py

Generate telephony tones to a WAV file for the LAB. Pure stdlib (wave + math),
8 kHz / mono / 16-bit -- the format Asterisk likes.

    # DTMF digit string (also used to build the CH5 decode challenge):
    python3 tone_generator.py dtmf 314159 -o dtmf-challenge.wav

    # A single tone (e.g. the historic 2600 Hz supervision tone):
    python3 tone_generator.py tone 2600 --seconds 3 -o 2600.wav

    # The 1004 Hz milliwatt test tone:
    python3 tone_generator.py tone 1004 -o milliwatt.wav

    # A multi-frequency (MF / R1) digit string (historical in-band signalling):
    python3 tone_generator.py mf 1234 -o mf.wav

EDUCATIONAL / LAB USE ONLY. The modern PSTN does NOT use in-band MF or 2600 Hz
supervision -- out-of-band SS7 replaced it decades ago. These tones do nothing
to real carriers; they exist here to drive the CTF on YOUR OWN Asterisk box and
to teach how in-band signalling worked (and why it was a security disaster).
"""
import argparse
import math
import struct
import sys
import wave

RATE = 8000
AMPLITUDE = 0.35  # keep headroom; summed tones must not clip

# Standard DTMF (low, high) frequency pairs.
DTMF = {
    "1": (697, 1209), "2": (697, 1336), "3": (697, 1477), "A": (697, 1633),
    "4": (770, 1209), "5": (770, 1336), "6": (770, 1477), "B": (770, 1633),
    "7": (852, 1209), "8": (852, 1336), "9": (852, 1477), "C": (852, 1633),
    "*": (941, 1209), "0": (941, 1336), "#": (941, 1477), "D": (941, 1633),
}

# MF (R1) pairs -- the in-band inter-office signalling phreaks famously abused.
MF = {
    "1": (700, 900), "2": (700, 1100), "3": (900, 1100), "4": (700, 1300),
    "5": (900, 1300), "6": (1100, 1300), "7": (700, 1500), "8": (900, 1500),
    "9": (1100, 1500), "0": (1300, 1500),
    "KP": (1100, 1700), "ST": (1500, 1700),
}


def _samples_for_freqs(freqs, seconds):
    n = int(RATE * seconds)
    out = []
    for i in range(n):
        t = i / RATE
        val = sum(math.sin(2 * math.pi * f * t) for f in freqs) / max(1, len(freqs))
        out.append(val * AMPLITUDE)
    return out


def _silence(seconds):
    return [0.0] * int(RATE * seconds)


def build_dtmf(digits, tone=0.20, gap=0.08, table=DTMF):
    buf = []
    for ch in digits:
        key = ch.upper()
        if key in table:
            buf += _samples_for_freqs(table[key], tone)
            buf += _silence(gap)
        elif ch in (" ", ","):
            buf += _silence(gap * 2)
        else:
            print("skip unknown symbol: %r" % ch, file=sys.stderr)
    return buf


def build_tone(freq, seconds):
    return _samples_for_freqs([freq], seconds)


def write_wav(path, samples):
    with wave.open(path, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        frames = bytearray()
        for s in samples:
            s = max(-1.0, min(1.0, s))
            frames += struct.pack("<h", int(s * 32767))
        w.writeframes(bytes(frames))
    print("wrote %s (%.2fs, %d Hz)" % (path, len(samples) / RATE, RATE))


def main():
    p = argparse.ArgumentParser(description="Telephony tone generator (lab use only)")
    sub = p.add_subparsers(dest="mode", required=True)

    d = sub.add_parser("dtmf", help="DTMF digit string")
    d.add_argument("digits")
    d.add_argument("--tone", type=float, default=0.20)
    d.add_argument("--gap", type=float, default=0.08)
    d.add_argument("-o", "--out", default="dtmf.wav")

    m = sub.add_parser("mf", help="MF/R1 digit string (historical)")
    m.add_argument("digits")
    m.add_argument("--tone", type=float, default=0.10)
    m.add_argument("--gap", type=float, default=0.06)
    m.add_argument("-o", "--out", default="mf.wav")

    t = sub.add_parser("tone", help="single frequency tone")
    t.add_argument("freq", type=float)
    t.add_argument("--seconds", type=float, default=2.0)
    t.add_argument("-o", "--out", default="tone.wav")

    args = p.parse_args()
    if args.mode == "dtmf":
        write_wav(args.out, build_dtmf(args.digits, args.tone, args.gap, DTMF))
    elif args.mode == "mf":
        write_wav(args.out, build_dtmf(args.digits, args.tone, args.gap, MF))
    elif args.mode == "tone":
        write_wav(args.out, build_tone(args.freq, args.seconds))


if __name__ == "__main__":
    main()
