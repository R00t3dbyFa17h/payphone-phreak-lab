#!/usr/bin/env python3
"""payphone-phreak-lab :: flag_check.py  (Asterisk AGI)

Called from the Flag Terminal (extension 700):

    AGI(flag_check.py,${TEAM},${FLAG})

Validates a dialed FLAG against flags.json, posts a solve to the scoreboard,
and sets channel variables the dialplan reads back:

    FLAGRESULT = OK | DUP | BAD
    FLAGPOINTS = <points awarded>   (0 on BAD/DUP)

No third-party dependencies (stdlib only).
"""
import json
import os
import sys
import urllib.request
import urllib.error

import agilib

HERE = os.path.dirname(os.path.abspath(__file__))
FLAGS_PATH = os.path.join(HERE, "flags.json")
SCOREBOARD_URL = os.environ.get("SCOREBOARD_URL", "http://127.0.0.1:8080").rstrip("/")
SCOREBOARD_TOKEN = os.environ.get("SCOREBOARD_TOKEN", "change-me-phreaklab")


def load_flags():
    try:
        with open(FLAGS_PATH) as f:
            return json.load(f)
    except Exception:
        return {}


def post_solve(team, challenge, points):
    """Record the solve. Returns 'OK', 'DUP', or 'ERR'."""
    body = json.dumps({
        "token": SCOREBOARD_TOKEN,
        "team": team,
        "challenge": challenge,
        "points": points,
    }).encode()
    req = urllib.request.Request(
        SCOREBOARD_URL + "/api/score",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode() or "{}")
            return data.get("result", "OK")
    except urllib.error.HTTPError as e:
        if e.code == 409:
            return "DUP"
        return "ERR"
    except Exception:
        return "ERR"


def main():
    agilib.read_env()
    team = sys.argv[1] if len(sys.argv) > 1 else ""
    flag = sys.argv[2] if len(sys.argv) > 2 else ""
    team = "".join(ch for ch in team if ch.isdigit())
    flag = "".join(ch for ch in flag if ch.isdigit())

    flags = load_flags()
    entry = flags.get(flag)

    if not team or entry is None:
        agilib.set_variable("FLAGRESULT", "BAD")
        agilib.set_variable("FLAGPOINTS", 0)
        agilib.verbose("flag_check: BAD team=%s flag=%s" % (team, flag))
        return

    points = int(entry.get("points", 0))
    result = post_solve(team, entry["id"], points)

    if result == "DUP":
        agilib.set_variable("FLAGRESULT", "DUP")
        agilib.set_variable("FLAGPOINTS", 0)
    elif result == "ERR":
        # Scoreboard unreachable: still acknowledge a correct flag so play
        # isn't blocked; organizers can reconcile from the asterisk log.
        agilib.set_variable("FLAGRESULT", "OK")
        agilib.set_variable("FLAGPOINTS", points)
        agilib.verbose("flag_check: scoreboard ERR, awarded locally team=%s %s" % (team, entry["id"]))
    else:
        agilib.set_variable("FLAGRESULT", "OK")
        agilib.set_variable("FLAGPOINTS", points)

    agilib.verbose("flag_check: team=%s flag=%s -> %s (%s, %d pts)"
                   % (team, flag, result, entry["id"], points))


if __name__ == "__main__":
    main()
