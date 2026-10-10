#!/usr/bin/env python3
"""payphone-phreak-lab :: scoreboard_status.py  (Asterisk AGI)

Called from extension 200:

    AGI(scoreboard_status.py,${TEAM})

Looks up a team's current score and sets:

    TEAMSCORE = <points>   (0 if unknown / scoreboard unreachable)
"""
import json
import os
import sys
import urllib.request

import agilib

SCOREBOARD_URL = os.environ.get("SCOREBOARD_URL", "http://127.0.0.1:8080").rstrip("/")


def main():
    agilib.read_env()
    team = sys.argv[1] if len(sys.argv) > 1 else ""
    team = "".join(ch for ch in team if ch.isdigit())
    score = 0
    if team:
        try:
            url = "%s/api/team/%s" % (SCOREBOARD_URL, team)
            with urllib.request.urlopen(url, timeout=5) as resp:
                data = json.loads(resp.read().decode() or "{}")
                score = int(data.get("points", 0))
        except Exception:
            score = 0
    agilib.set_variable("TEAMSCORE", score)
    agilib.verbose("scoreboard_status: team=%s score=%d" % (team, score))


if __name__ == "__main__":
    main()
