# Custom sounds

Drop custom prompt recordings here. They are copied into
`/var/lib/asterisk/sounds/custom/` in the PBX image and referenced from the
dialplan as `custom/<name>` (e.g. `Playback(custom/welcome)`).

Record as **8 kHz, mono, 16-bit PCM WAV** (or let Asterisk transcode):

```bash
sox -default -r 8000 -c 1 -b 16 welcome.wav   # record from mic
# or convert an existing file:
ffmpeg -i welcome.mp3 -ar 8000 -ac 1 -acodec pcm_s16le welcome.wav
```

The game runs fine with NO custom sounds (it uses stock Asterisk prompts +
spoken digits). These are optional flavour.

## Required for CH5 (DTMF Decode)
Generate the Touch-Tone challenge clip (encodes flag `314159`):

```bash
../../tools/gen_challenge_audio.sh
```

That writes `dtmf-challenge.wav` here. Rebuild the PBX image afterwards.
