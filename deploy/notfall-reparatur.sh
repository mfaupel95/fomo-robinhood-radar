#!/usr/bin/env bash
# notfall-reparatur.sh — fomoradar.app ist von aussen nicht erreichbar (80/443 zu),
# SSH (22) aber offen: der Host lebt, Caddy/Webschicht steht nicht.
#
# Aufruf (auf dem Server, als root):
#   ssh -i ~/.ssh/fomoradar root@193.233.209.98 'bash -s' < deploy/notfall-reparatur.sh
# oder direkt auf der Maschine:  bash /opt/fomoradar/app/deploy/notfall-reparatur.sh
#
# SICHER: liest zuerst, startet nur, was nachweislich aus ist; startet nichts neu,
# was laeuft. Aendert keine Konfiguration. Keine Secrets in der Ausgabe.
set -uo pipefail

echo "=== 1. Host ==="
hostname; uptime || true
echo
echo "=== 2. Platz (voll = haeufigste Ursache fuer toten Caddy) ==="
df -h / /opt 2>/dev/null || df -h /
echo
echo "=== 3. Dienst-Zustand ==="
for u in caddy radar-api radar-site radar-bot radar-watch radar-collect.timer \
         radar-health.timer radar-digest.timer radar-heartbeat.timer; do
  st=$(systemctl is-active "$u" 2>/dev/null || true)
  en=$(systemctl is-enabled "$u" 2>/dev/null || true)
  printf '  %-22s active=%-10s enabled=%s\n' "$u" "${st:-?}" "${en:-?}"
done
echo
echo "=== 4. Was lauscht auf 80/443/8000/4321? ==="
(ss -ltnp 2>/dev/null || netstat -ltnp 2>/dev/null) | grep -E ':(80|443|8000|4321)\b' || echo "  (nichts)"
echo
echo "=== 5. Firewall ==="
ufw status verbose 2>/dev/null | head -20 || echo "  ufw nicht verfuegbar"
echo
echo "=== 6. Letzte Fehler (Caddy / Site / API) ==="
for u in caddy radar-site radar-api; do
  echo "--- $u"
  journalctl -u "$u" -n 15 --no-pager 2>/dev/null | grep -iE 'error|fail|panic|denied|full|refus' | tail -6 || true
done
echo
echo "=== 7. Reparatur (nur Aus-Start, keine Konfig-Aenderung) ==="
geaendert=0
for u in caddy radar-api radar-site; do
  if ! systemctl is-active --quiet "$u" 2>/dev/null; then
    echo "  starte $u ..."
    systemctl start "$u" && geaendert=1 || echo "  FEHLER beim Start von $u"
  fi
done
# Ein gescheiterter Unit (z. B. nach Reboot) wird einmal zurueckgesetzt.
systemctl reset-failed 2>/dev/null || true
[ "$geaendert" -eq 0 ] && echo "  alles, was laufen soll, lief bereits."
echo
echo "=== 8. Nachpruefung ==="
sleep 3
for u in caddy radar-api radar-site; do
  printf '  %-12s %s\n' "$u" "$(systemctl is-active "$u" 2>/dev/null || echo '?')"
done
(ss -ltn 2>/dev/null || netstat -ltn 2>/dev/null) | grep -E ':(80|443)\b' || echo "  80/443 lauscht NICHT"
echo
echo "=== 9. Von aussen pruefen (auf dem Server selbst) ==="
curl -sS -o /dev/null -w '  https://fomoradar.app -> %{http_code} (%{time_total}s)\n' \
     --max-time 15 https://fomoradar.app/ 2>&1 || echo "  https fehlgeschlagen"
echo
echo "=== fertig. Wenn 80/443 noch zu sind: Abschnitt 6 zeigt den Grund. ==="
