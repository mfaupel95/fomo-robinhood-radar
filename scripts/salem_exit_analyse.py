"""Exit-Analyse: wie viel von Salems AI-Position ist tatsaechlich verkaufbar?
Read-only. Rechnet Position gegen Pool-Tiefe, Verkaufsdruck und sell-check."""
import sys, json, datetime
sys.path.insert(0, r"O:/Werkstatt/fomo-robinhood-radar")
import httpx
from fomo_agent import db

AI = "0x2e8c31162b855a2ffa90f6f8634643ad6f111e18"
SALEM = "0xb8f305f27ccc406373de0082cc06cb1d065504ea"

conn = db.connect()
conn.text_factory = lambda b: b.decode("utf-8", "replace")

tok = conn.execute("SELECT mint,symbol,liquidity_usd,volume_usd,mcap_usd,sellable,price_usd,checked_at "
                   "FROM tokens WHERE mint=?", (AI,)).fetchone()
print("=== Token ===")
print(dict(tok) if tok else "nicht in tokens")

hold = conn.execute("SELECT amount, ts FROM holdings WHERE address=? AND token=?", (SALEM, AI)).fetchone()
amt = hold["amount"] if hold else 0.0
print(f"\n=== Salem-Position ===\n{amt:,.0f} AI (gelesen "
      f"{datetime.datetime.fromtimestamp(hold['ts'], datetime.UTC):%m-%d %H:%M UTC})" if hold else "keine Holdings-Zeile")

print("\n=== Markt (DexScreener, alle Paare) ===")
r = httpx.get("https://api.dexscreener.com/latest/dex/tokens/" + AI, timeout=25).json()
pairs = r.get("pairs") or []
tot_liq = 0.0
for p in sorted(pairs, key=lambda x: -((x.get("liquidity") or {}).get("usd") or 0))[:4]:
    liq = (p.get("liquidity") or {}).get("usd") or 0
    vol = (p.get("volume") or {}).get("h24") or 0
    tot_liq += liq
    print(f"  {p.get('dexId')}/{p.get('pairAddress','')[:12]}: px {p.get('priceUsd')} | liq ${liq:,.0f} | vol24 ${vol:,.0f} | chg24 {(p.get('priceChange') or {}).get('h24')}%")
print(f"  Summe Liquiditaet: ${tot_liq:,.0f}")

# Verkaufsseite: was wurde in 24h tatsaechlich verkauft?
now = db.now()
sells = conn.execute("SELECT COUNT(*) n, COALESCE(SUM(usd_value),0) usd FROM trades "
                     "WHERE mint=? AND side='sell' AND ts>=?", (AI, now - 86400)).fetchone()
buys = conn.execute("SELECT COUNT(*) n, COALESCE(SUM(usd_value),0) usd FROM trades "
                    "WHERE mint=? AND side='buy' AND ts>=?", (AI, now - 86400)).fetchone()
print(f"\n=== Tape 24h ===\nKaeufe: {buys['n']} / ${buys['usd']:,.0f}   Verkaeufe: {sells['n']} / ${sells['usd']:,.0f}")

# sell-check-Historie
try:
    sc = conn.execute("SELECT sellable, sell_note, sell_checked_at FROM tokens WHERE mint=?", (AI,)).fetchone()
    print(f"\n=== sell-check ===\nsellable={sc['sellable']} | note={sc['sell_note']} | "
          f"{datetime.datetime.fromtimestamp(sc['sell_checked_at'], datetime.UTC):%m-%d %H:%M}" if sc and sc['sell_checked_at'] else "kein sell-check")
except Exception as e:
    print("sell-check:", e)

if hold and tot_liq:
    px = float((pairs[0].get("priceUsd") if pairs else 0) or 0)
    print(f"\n=== Exit-Rechnung (px {px}) ===")
    print(f"  Positionswert: ${amt*px:,.0f}")
    for share in (0.01, 0.05, 0.10, 0.25, 0.50, 1.00):
        print(f"  {share*100:5.1f}% der Position = ${amt*px*share:,.0f} = {share*amt*px/tot_liq*100:5.1f}% der Pool-Tiefe")
