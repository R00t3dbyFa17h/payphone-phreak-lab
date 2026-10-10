# payphone-phreak-lab :: Asterisk PBX image
FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

# Asterisk + English core sounds (gsm & wav) + python3 for the AGI scripts.
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      asterisk \
      asterisk-core-sounds-en-gsm \
      asterisk-core-sounds-en-wav \
      python3 \
      ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Drop in our configuration (the CTF lives in extensions.conf).
COPY etc/ /etc/asterisk/

# AGI flag-checker + scoreboard helpers.
COPY agi/ /var/lib/asterisk/agi-bin/
RUN chmod +x /var/lib/asterisk/agi-bin/*.py || true

# Optional custom prompts / challenge audio (safe if empty).
COPY sounds/ /var/lib/asterisk/sounds/custom/
RUN chown -R root:root /etc/asterisk /var/lib/asterisk || true

# SIP + a small RTP range (see rtp.conf).
EXPOSE 5060/udp
EXPOSE 10000-10099/udp

# Foreground, verbose console.
CMD ["asterisk", "-f", "-vvvc"]
