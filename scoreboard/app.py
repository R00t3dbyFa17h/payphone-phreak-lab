#!/usr/bin/env python3
"""payphone-phreak-lab :: scoreboard

A tiny Flask + SQLite live scoreboard. The Asterisk AGI (flag_check.py) POSTs
solves here; the big screen at the meetup shows /.

Endpoints
    GET  /                 live HTML scoreboard (auto-refresh)
    GET  /healthz          health probe
    GET  /api/board        JSON: ranked teams + recent solves
    GET  /api/team/<id>    JSON: one team's points
    POST /api/team         {token, team, name}     register/rename a team
    POST /api/score        {token, team, challenge, points}  record a solve
                           -> 200 {"result":"OK"} or 409 {"result":"DUP"}

Stdlib + Flask only.
"""
import os
import sqlite3
import time
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

DB_PATH = os.environ.get("DB_PATH", os.path.join(os.path.dirname(__file__), "scoreboard.db"))
TOKEN = os.environ.get("SCOREBOARD_TOKEN", "change-me-phreaklab")
PORT = int(os.environ.get("PORT", "8080"))


def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = db()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS teams (
            id   TEXT PRIMARY KEY,
            name TEXT,
            created REAL
        );
        CREATE TABLE IF NOT EXISTS solves (
            team      TEXT,
            challenge TEXT,
            points    INTEGER,
            ts        REAL,
            UNIQUE(team, challenge)
        );
        """
    )
    conn.commit()
    conn.close()


def ensure_team(conn, team, name=None):
    row = conn.execute("SELECT id, name FROM teams WHERE id=?", (team,)).fetchone()
    if row is None:
        conn.execute("INSERT INTO teams (id, name, created) VALUES (?,?,?)",
                     (team, name or ("Team " + team), time.time()))
    elif name:
        conn.execute("UPDATE teams SET name=? WHERE id=?", (name, team))


@app.route("/healthz")
def healthz():
    return jsonify({"ok": True})


@app.route("/api/team", methods=["POST"])
def api_team():
    data = request.get_json(force=True, silent=True) or {}
    if data.get("token") != TOKEN:
        return jsonify({"error": "unauthorized"}), 401
    team = str(data.get("team", "")).strip()
    if not team:
        return jsonify({"error": "team required"}), 400
    conn = db()
    ensure_team(conn, team, data.get("name"))
    conn.commit()
    conn.close()
    return jsonify({"result": "OK", "team": team})


@app.route("/api/score", methods=["POST"])
def api_score():
    data = request.get_json(force=True, silent=True) or {}
    if data.get("token") != TOKEN:
        return jsonify({"error": "unauthorized"}), 401
    team = str(data.get("team", "")).strip()
    challenge = str(data.get("challenge", "")).strip()
    try:
        points = int(data.get("points", 0))
    except (TypeError, ValueError):
        points = 0
    if not team or not challenge:
        return jsonify({"error": "team and challenge required"}), 400

    conn = db()
    ensure_team(conn, team)
    try:
        conn.execute(
            "INSERT INTO solves (team, challenge, points, ts) VALUES (?,?,?,?)",
            (team, challenge, points, time.time()),
        )
        conn.commit()
        result, code = "OK", 200
    except sqlite3.IntegrityError:
        result, code = "DUP", 409
    conn.close()
    return jsonify({"result": result, "team": team, "challenge": challenge, "points": points}), code


@app.route("/api/team/<team>")
def api_team_score(team):
    conn = db()
    row = conn.execute("SELECT COALESCE(SUM(points),0) AS pts FROM solves WHERE team=?", (team,)).fetchone()
    conn.close()
    return jsonify({"team": team, "points": int(row["pts"])})


def _board():
    conn = db()
    teams = conn.execute(
        """
        SELECT t.id AS id, t.name AS name,
               COALESCE(SUM(s.points),0) AS points,
               COUNT(s.challenge) AS solved,
               COALESCE(MAX(s.ts),0) AS last_ts
        FROM teams t LEFT JOIN solves s ON s.team = t.id
        GROUP BY t.id
        ORDER BY points DESC, last_ts ASC
        """
    ).fetchall()
    recent = conn.execute(
        """
        SELECT s.team AS team, t.name AS name, s.challenge AS challenge,
               s.points AS points, s.ts AS ts
        FROM solves s LEFT JOIN teams t ON t.id = s.team
        ORDER BY s.ts DESC LIMIT 15
        """
    ).fetchall()
    conn.close()
    return teams, recent


@app.route("/api/board")
def api_board():
    teams, recent = _board()
    return jsonify({
        "teams": [dict(r) for r in teams],
        "recent": [dict(r) for r in recent],
    })


@app.route("/")
def index():
    teams, recent = _board()
    return render_template("index.html", teams=teams, recent=recent, now=time.time())


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
