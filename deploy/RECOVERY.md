# Ausfall und Wiederanlauf — FOMO Robinhood Radar

Stand: 2026-11-02.

## Was am 2026-11-02 gemessen wurde

`fomoradar.app` ist vollständig tot: Ports 22, 80 und 443 antworten nicht, ICMP 100 % Verlust,
auch von einem fremden Netz (Firecrawl) Timeout. DNS ist in Ordnung (A 193.233.209.98, auch über
8.8.8.8); `tracert` endet in den Hops vor dem Ziel. Das ist kein Caddy- oder App-Fehler, sondern
die Maschine selbst ist weg.

**Ursache ist bekannt und gewollt:** das Upstream-Repository
(`github.com/cvxv666/fomo-robinhood-radar`) trägt seit dem 6. Oktober 2026 den Commit
„Archived: two months of it, kept where the machine cannot take it“ — *„The server, the site and
the bot are switched off on 6 October 2026.“* Die IP gehört **Aeza** (NL), nicht Contabo; Domain
und Maschine sind cvxv666's, nicht Max'. Es gibt von hier keinen SSH-Key, kein Provider-Konto und
damit keinen Weg, diese Maschine zu booten.

Konsequenz: **`fomoradar.app` lässt sich von diesem Rechner aus nicht „reparieren“.** Entweder
schaltet der Betreiber wieder ein, oder es wird eine eigene Instanz betrieben. Beides ist eine
Entscheidung über Geld/Domain, keine Codeänderung.

## Lokal betreiben (auf diesem Windows-Rechner)

Voraussetzungen: `.venv`, `site/node_modules`, `fomo_agent.db` (alles vorhanden).

```
deploy\windows\start-local.cmd        REM API + Site + Bot, idempotent
deploy\windows\stop-local.cmd         REM beendet alle drei
```

- Site: http://127.0.0.1:4321 — API: http://127.0.0.1:8000/docs (User-Agent nötig, sonst 401/429)
- Logs: `logs\api.log`, `logs\site.log`, `logs\bot.log`
- Der Bot ist `@Maximilian420_5_bot` (`TELEGRAM_BOT_NAME=fomoradarRH_bot` in `.env`, Token geprüft).
  Ein zweiter Long-Poller beendet sich selbst mit 409 — Doppelstart ist ungefährlich.
- `PUBLIC_SITE_URL` zeigt in `.env` noch auf `https://fomoradar.app` (tot). Solange keine eigene
  Domain gesetzt ist, führen Links aus Bot/Pushes ins Leere — bewusst offen gelassen.

Wächter: `deploy\health_local.py` prüft API + Site und meldet **nur Zustandswechsel**
(leere Ausgabe = alles gut). Er läuft als Hermes-Cronjob `fomo-local-watch` (alle 15 Minuten) und
schreibt seinen Zustand nach `~\.fomo-radar-health.json`.

## Eigene öffentliche Instanz (der eigentliche Weg zurück)

1. VPS mieten (Ubuntu 24.04/26.04, 2–4 GB RAM, ~5 €/Monat; Anbieter egal).
2. Domain oder Subdomain auf die IP zeigen lassen (A-Record). Ohne eigene Domain geht auch
   `http://<ip>` für den Anfang — Caddy braucht für TLS einen Namen.
3. Auf der Kiste als root:

```
REPO=https://github.com/mfaupel95/fomo-robinhood-radar.git \
DOMAIN=radar.example.com bash deploy/provision.sh
```

Das Skript installiert Pakete, User `radar`, venv, Site-Build, systemd-Units und Caddy. Beim
ersten Lauf stoppt es nach dem Anlegen von `.env` (Kopie von `.env.example`) und nennt die
Pflichtfelder — `TELEGRAM_BOT_TOKEN`, `RPC_URLS`, `FOMOAPI_KEY`, `PUBLIC_SITE_URL`. Danach:

```
systemctl enable --now radar-api radar-site radar-bot radar-collect.timer radar-watch \
    radar-health.timer radar-digest.timer radar-daily.timer radar-backup.timer
curl -A provision/1.0 http://127.0.0.1:8000/api/health
```

4. Danach ist `deploy/update.sh` mit `RADAR_HOST=root@<ip>` und `RADAR_KEY` der normale Deploy-Weg.

Grenzen: das Skript ist idempotent, aber **nicht auf echter Hardware getestet** (kein Host
verfügbar). Erster Lauf auf einer frischen Kiste mit `bash -x` beobachten.

## Diagnose-Kommandos (von außen, ohne Serverzugang)

```
nslookup fomoradar.app 8.8.8.8
for p in 22 80 443; do timeout 8 bash -c "cat </dev/null >/dev/tcp/<host>/$p" && echo "$p open" || echo "$p down"; done
curl -sS -m 20 -A "fomo-radar/1.0" https://<host>/api/health
```

Auf der Kiste selbst (wenn SSH wieder geht):

```
systemctl status radar-api radar-site radar-bot caddy
systemctl list-timers 'radar-*'
journalctl -u radar-api -n 80 --no-pager
df -h; free -m; uptime
```
