"""Tiny, dependency-free AGI helper for payphone-phreak-lab.

Implements just enough of the Asterisk Gateway Interface (AGI) protocol to
read the initial environment and set channel variables / speak. Pure stdlib
so it runs inside the stock Asterisk image with no pip installs.
"""
import sys


def read_env():
    """Read the AGI environment block (agi_* : value lines) from stdin."""
    env = {}
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        line = line.strip()
        if line == "":
            break
        if ":" in line:
            key, _, val = line.partition(":")
            env[key.strip()] = val.strip()
    return env


def command(cmd):
    """Send one AGI command and return the raw response line."""
    sys.stdout.write(cmd + "\n")
    sys.stdout.flush()
    return sys.stdin.readline().strip()


def set_variable(name, value):
    # Quote the value so spaces/specials survive.
    safe = str(value).replace('"', "'")
    return command('SET VARIABLE %s "%s"' % (name, safe))


def verbose(message, level=1):
    safe = str(message).replace('"', "'")
    return command('VERBOSE "%s" %d' % (safe, level))
