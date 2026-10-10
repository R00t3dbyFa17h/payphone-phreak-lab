#!/usr/bin/env python3
"""payphone-phreak-lab :: dtmf_decoder.py

Decode DTMF digits from a WAV file using the Goertzel algorithm. Pure stdlib
(wave + math) -- no numpy. This is the companion tool for CH5 ("DTMF Decode"):
capture the tones the PBX plays on extension 322, then:

    python3 dtmf_decoder.py capture.wav
    -> decoded: 314159

Works on 8-bit/16-bit mono or stereo PCM WAV at any sample rate.
"""
import math
import sys
import wave

DTMF_LOW = [697, 770, 852, 941]
DTMF_HIGH = [1209, 1336, 1477, 1633]
KEYS = [
    ["1", "2", "3", "A"],
    ["4", "5", "6", "B"],
    ["7", "8", "9", "C"],
    ["*", "0", "#", "D"],
]


def read_wav(path):
    with wave.open(path, "rb") as w:
        rate = w.getframerate()
        n = w.getnframes()
        ch = w.getnchannels()
        width = w.getsampwidth()
        raw = w.readframes(n)
    samples = []
    step = width * ch
    for i in range(0, len(raw) - step + 1, step):
        frame = raw[i:i + width]  # first channel only
        if width == 1:
            samples.append((frame[0] - 128) / 128.0)
        elif width == 2:
            val = int.from_bytes(frame, "little", signed=True)
            samples.append(val / 32768.0)
        else:
            val = int.from_bytes(frame[:2], "little", signed=True)
            samples.append(val / 32768.0)
    return rate, samples


def goertzel(samples, freq, rate):
    n = len(samples)
    k = int(0.5 + (n * freq) / rate)
    w = (2.0 * math.pi / n) * k
    cw = math.cos(w)
    coeff = 2.0 * cw
    s0 = s1 = s2 = 0.0
    for x in samples:
        s0 = x + coeff * s1 - s2
        s2 = s1
        s1 = s0
    power = s1 * s1 + s2 * s2 - coeff * s1 * s2
    return power


def detect_block(block, rate):
    low = [goertzel(block, f, rate) for f in DTMF_LOW]
    high = [goertzel(block, f, rate) for f in DTMF_HIGH]
    li = low.index(max(low))
    hi = high.index(max(high))
    # Simple energy gate to reject silence/noise blocks.
    total = sum(low) + sum(high)
    if total < 1e-3:
        return None
    if max(low) < 0.1 * (total / 8) or max(high) < 0.1 * (total / 8):
        return None
    return KEYS[li][hi]


def decode(path, block_ms=40):
    rate, samples = read_wav(path)
    block = int(rate * block_ms / 1000.0)
    if block < 1:
        return ""
    out = []
    last = None
    silence_run = 0
    for i in range(0, len(samples) - block, block):
        d = detect_block(samples[i:i + block], rate)
        if d is None:
            silence_run += 1
            if silence_run >= 1:
                last = None  # a gap separates repeated digits
            continue
        silence_run = 0
        if d != last:
            out.append(d)
            last = d
    return "".join(out)


def main():
    if len(sys.argv) < 2:
        print("usage: dtmf_decoder.py <file.wav>", file=sys.stderr)
        sys.exit(1)
    digits = decode(sys.argv[1])
    print("decoded: %s" % (digits or "(nothing detected)"))


if __name__ == "__main__":
    main()
