#!/usr/bin/env python3
"""Local health watch for the FOMO Radar stack (API + site).

Prints NOTHING while both answer. Prints one line per state change when one stops or comes back.
Made for a no_agent cron job: empty stdout means no message is delivered.

State lives in a JSON file so a problem is reported once, not every tick.

    RADAR_API   default http://127.0.0.1:8000/api/health
    RADAR_SITE  default http://127.0.0.1:4321/
"""
import json
import os
import pathlib
import time
import urllib.request
import urllib.error

API = os.environ.get("RADAR_API", "http://127.0.0.1:8000/api/health")
SITE = os.environ.get("RADAR_SITE", "http://127.0.0.1:4321/")
UA = "fomo-radar-watch/1.0 (-)"
STATE = pathlib.Path(os.environ.get("RADAR_WATCH_STATE", pathlib.Path.home() / ".fomo-radar-health.json"))
TIMEOUT = float(os.environ.get("RADAR_WATCH_TIMEOUT", "8"))


def probe(url: str, want_json_ok: bool = False):
    """Return (up: bool, detail: str). Never raises."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            body = r.read(4096)
            if want_json_ok:
                try:
                    data = json.loads(body.decode("utf-8", "replace"))
                except ValueError:
                    return False, "answers, but not JSON"
                if not data.get("ok"):
                    return False, "answers ok:false"
                stale = data.get("stale_seconds")
                extra = ""
                if isinstance(stale, (int, float)) and stale > 8 * 3600:
                    extra = " · last fill %dh ago" % round(stale / 3600)
                return True, extra
            return True, ""
    except urllib.error.HTTPError as e:
        return False, "HTTP %s" % e.code
    except Exception as e:  # noqa: BLE001 - a watch must never crash
        return False, type(e).__name__


def main() -> int:
    now = time.strftime("%H:%M")
    api_up, api_detail = probe(API, want_json_ok=True)
    site_up, _ = probe(SITE)
    before = {}
    try:
        before = json.loads(STATE.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001 - missing or broken state is a first run
        pass
    out = []
    if before.get("api") and not api_up:
        out.append("⚠️ FOMO lokal: API weg (%s)" % api_detail)
    elif before.get("api") is False and api_up:
        out.append("✅ FOMO lokal: API wieder da%s" % (api_detail or ""))
    elif "api" not in before and not api_up:
        out.append("⚠️ FOMO lokal: API antwortet nicht (%s) — start-local.cmd?" % api_detail)
    if before.get("site") and not site_up:
        out.append("⚠️ FOMO lokal: Site weg")
    elif before.get("site") is False and site_up:
        out.append("✅ FOMO lokal: Site wieder da")
    elif "site" not in before and not site_up:
        out.append("⚠️ FOMO lokal: Site antwortet nicht — start-local.cmd?")
    STATE.write_text(json.dumps({"api": api_up, "site": site_up, "ts": int(time.time())}),
                     encoding="utf-8")
    for line in out:
        print("%s %s" % (now, line))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
