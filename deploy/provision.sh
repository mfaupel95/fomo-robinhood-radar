#!/usr/bin/env bash
# Provision a fresh Ubuntu host for FOMO Robinhood Radar.
#
# The upstream machine (fomoradar.app, cvxv666's box) was switched off on 2026-10-06, so
# bringing the product back means standing the stack up somewhere, not repairing it there.
# Run as root on a clean Ubuntu 24.04 / 26.04 host:
#
#   REPO=https://github.com/mfaupel95/fomo-robinhood-radar.git \
#   DOMAIN=radar.example.com bash deploy/provision.sh
#
# Idempotent: a second run updates the checkout and reinstalls dependencies; it does not
# touch the database, the backups or an existing .env. Secrets are NOT filled in here -
# the script copies .env.example, refuses to start the services blind, and prints what to set.
set -euo pipefail

REPO="${REPO:-https://github.com/mfaupel95/fomo-robinhood-radar.git}"
BRANCH="${BRANCH:-main}"
DOMAIN="${DOMAIN:-}"
APP=/opt/fomoradar/app
VENV=/opt/fomoradar/venv
DATA=/opt/fomoradar
CORE="radar-api radar-site radar-bot radar-collect.timer radar-watch radar-health.timer radar-digest.timer radar-daily.timer radar-heartbeat.timer radar-backup.timer"

[ "$(id -u)" -eq 0 ] || { echo "run as root" >&2; exit 1; }

echo "==> packages"
apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
    git curl ca-certificates python3 python3-venv python3-pip nodejs npm caddy ufw

echo "==> user"
id -u radar >/dev/null 2>&1 || useradd --system --create-home --shell /usr/sbin/nologin radar

echo "==> tree"
mkdir -p "$DATA" "$DATA/backups"
if [ -d "$APP/.git" ]; then
    git -C "$APP" fetch origin "$BRANCH" --quiet
    git -C "$APP" reset --hard "origin/$BRANCH" --quiet
else
    rm -rf "$APP"
    git clone --branch "$BRANCH" --depth 1 "$REPO" "$APP"
fi

echo "==> python"
python3 -m venv "$VENV"
"$VENV/bin/pip" install -q --upgrade pip
"$VENV/bin/pip" install -q -e "$APP"

echo "==> site"
( cd "$APP/site" && npm install --no-audit --no-fund --loglevel=error && npm run build )

echo "==> secrets"
FRESH_ENV=0
if [ ! -f "$APP/.env" ]; then
    cp "$APP/.env.example" "$APP/.env"
    FRESH_ENV=1
fi
chown radar:radar "$APP/.env"
chmod 600 "$APP/.env"
chown -R radar:radar "$DATA"

echo "==> units"
install -m 644 "$APP"/deploy/systemd/*.service /etc/systemd/system/
install -m 644 "$APP"/deploy/systemd/*.timer /etc/systemd/system/
systemctl daemon-reload

echo "==> caddy"
if [ -n "$DOMAIN" ]; then
    sed "s/fomoradar\.app/$DOMAIN/g" "$APP/deploy/Caddyfile" > /etc/caddy/Caddyfile
    systemctl enable caddy >/dev/null 2>&1 || true
    systemctl reload caddy 2>/dev/null || systemctl restart caddy
else
    echo "   DOMAIN unset - Caddyfile not installed; rerun with DOMAIN=host.tld to do it"
fi

echo "==> firewall"
ufw allow 22/tcp >/dev/null 2>&1 || true
ufw allow 80/tcp >/dev/null 2>&1 || true
ufw allow 443/tcp >/dev/null 2>&1 || true

if [ "$FRESH_ENV" = "1" ]; then
    echo
    echo "  .env is .env.example, not a working config. Fill at least:"
    echo "    TELEGRAM_BOT_TOKEN, RPC_URLS, FOMOAPI_KEY, DB_PATH=$APP/../../fomo_agent.db"
    [ -n "$DOMAIN" ] && echo "    PUBLIC_SITE_URL=https://$DOMAIN, API_CORS_ORIGINS=https://$DOMAIN"
    echo "  then start it:  systemctl enable --now $CORE"
    echo
    exit 0
fi

echo "==> start"
for u in $CORE; do
    systemctl enable --now "$u" >/dev/null 2>&1 || echo "   could not start $u - journalctl -u $u"
done

echo "==> check"
sleep 4
curl -fsS -m 10 -A "provision/1.0" http://127.0.0.1:8000/api/health && echo || \
    echo "   api not answering yet - journalctl -u radar-api -n 40"

echo
echo "done.  tests: cd $APP && $VENV/bin/python -m pytest -q"
