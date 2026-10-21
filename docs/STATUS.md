# fomo-agent — состояние проекта и фронт работ

Обновлено: 2026-10-21 (сессия 69).

**Session 69 (21. Okt, ~15:35-15:48 UTC): voller `run --once` (runs 2770-2778) - 0 Fehler; collect-loop LEBT (track-Takte 14:21/14:51/15:18, alle 0 errors/24h; run #2764 track war ein manueller Test-Kill, als dead markiert); Watcher LEBT (Worker-PID 32752, Start 04:40, unveraendert seit S68, genau 1 Familie, kein Doppel-Scan) und schrieb Burst #6 live (GARDEN 14:30).** Eigener Lauf statt DB-only: discover_trenches 147 seen / 0 new / 147 updated (lebt), fomo weiter skipped (fomo not configured), new_tokens checked 3 / new 1 ("Claude" 0xc527ce547ab6…, mcap $10,1M liq $10,2M, created 14:12 - noch ungepreist, keine Pool-Adresse, mcap≈liq spricht erstmal fuer Fake-Liq/Honeypot), resolve 0 (keine neuen Trader, letzter first_seen 22. Sep), track 25 Wallets / 0 trades / 0 errors / 426 RPC-Requests (22 Fills vom Watcher/Loop schon auf dem Tape - dedup ueber fill_key), enrich named 27 / priced 24 (sell_check 1 unsellable, fail-soft: 0x043d400d 21 Buys/0 Sells), holdings **1784 pairs (1368 held / 416 empty, +9 seit S68)**, deployers 0, crews 0. RPC-Node gesund, aber stark gedrosselt (53s-Sleeps im eigenen Lauf - geteilt mit Watcher+Loop, normal). **NEUE Signale seit Session 68 (13:07 UTC): (1) picadura (watch 62, UEBER der Trust-Linie) kaufte 13:12-13:14 $20,0k in 3 Buys: $9,991 + $4,995 in ABYSS 0x15f33856… (mcap $3,7M liq $235k) und $4,996 in GH0ST 0x2eb2849c… (mcap $398k liq $58k, created 20.10., ~18h alt) - Zwei-Token-Einstieg einer Trusted-Wallet, Einzel-Wallet, kein Cluster. (2) FartmanSacks (watch 55, UNTER der Trust-Linie) DCA $28,9k in 8 Buys in INU 0x63ee32ac… (13:15-15:19, mcap $2,05M liq $531k) - groesste Buy-Serie seit S68, 0 Sells, weiterhin einzeln, kein Gate. (3) 0xFalcs (watch 50) kaufte 15:15 $29,957 in BONER 0x98096d17e1… (mcap $20,4M liq $1,4M) - GROESSTER Einzel-Buy des Tages, etablierter 51-Tage-Mid-Cap, Einzel-Wallet. (4) **Burst #6 GARDEN** 0xe892480af7… 14:30: RugDalio (65) + iruletrenches (60) + AvgJoesCrypto (60) je $106 in 20 min (14:10-14:30), Token created 14:09, mcap $12k liq $6k, conv 1.14, Alter 20 min - DIESELBE Kohorte wie Burst #5 eHook (03:35, eHook seit Burst-Preis +84%): Muster "Kohorte testet new Launch mit Kleinstbetraegen"; nichts gepusht (0 Subscriber). (5) Exits: MemeKingdom sell $12 (15:44, Dust), unipcs sell NVDA $114 (13:25, Quote-Asset-Kontext). Kontext, nicht neu: TORCH (cosby 13:03 $5,842) ohne weitere Roster-Kaeufe; brezscales-Token 13:06 jetzt benannt: GLOAM 0xdcd885f5…, mcap $1,84M liq $197k px $3,68. **Gewinner unveraendert:** FARMBLOCK (id 4) +2.22x (px 2.369e-05, unveraendert bis 15:27), eHook (id 5) +1.19x (px 2.79e-05, unveraendert seit 14:30), TAPE/TOLL flach ~1.0x (mcap 63k/100k), PRIVACY (id 1) tot (mcap $93, liq $0). Status unveraendert: 147 Trader (2 active / 68 watch / 15 idle / 1 tracking / 61 dropped), 0 neue in 7 Tagen; Top active: game_for_one 72, 0xAvast 70. Score-Queue LEER (pending_scores.json = der Export von 09:23, laengst importiert). Stray: `--unscored` (2,5 kB, Fehl-Export vom 20.10., kein Queue-Item) - Cleanup-Kandidat. **Naechste Aktionen (Entscheidung/Handgriff bei Max): nichts Dringendes - Pipeline, collect-loop und Watcher laufen. GARDEN beobachten: steigt die eHook-Kohorte (65/60/60) mit groesseren Summen nach -> Muster bestaetigt, sonst verpufft. Entscheidung: 0xFalcs (50) nach-scoren? $29,957-Einzel-Buy ist scope-groesser als sein Score. picadura/FartmanSacks: Einzel-Akkumulation, kein Gate. Claude-Token beim naechsten enrich pruefen (Preis/Pool); mcap≈liq erstmal als Fake-Liq werten bis Gegenbeweis.** Keine neuen Keys noetig (FOMO_SESSION/ANTHROPIC/CODEX/HELIUS/FOMOAPI leer wie gehabt - nicht blockierend, Tracking/Bursts auf freiem RPC; TELEGRAM_BOT_TOKEN gesetzt, aber 0 Subscriber -> Pushe feuern nicht; X-Keys leer). Keine Schluessel gedruckt.

**Session 68 (21. Okt, ~12:56-13:07 UTC): voller `run --once` (runs 2749-2758) - 0 Fehler; collect-loop LEBT (track ~30-min-Takt, letzter 12:49, Dauer 9,1 min, 0 errors/24h); Watcher LEBT (genau 1 Familie 40080 Launcher -> 47276 -> 32752 Worker, Start 04:40, kein Doppel-Scan) und schrieb die zwei neuen Fills 13:03/13:06 live (zwischen zwei Loop-Tracks); Score-Queue weiter LEER.** Eigener Lauf statt DB-only (Discovery 6,9 h alt, letzter 06:02, Prezedenz 63/64/66): discover_trenches 147 seen / 0 new / 147 updated (lebt), fomo weiter skipped (fomo not configured), new_tokens checked 3 / new 0, resolve 0 (keine neuen Trader, letzter first_seen 22. Sep), track 25 Wallets / 0 trades / 0 errors / 342 RPC-Requests (inkrementelles Fenster, Loop-Track 12:49 hatte das volle Fenster; dedup ueber fill_key штатно), enrich named 305 / priced 121 (sell_check 1 unsellable, fail-soft), holdings **1775 pairs (1359 held / 416 empty - weiter gewachsen von 1773)**, deployers 0, crews 0. Keine offenen runs nach dem Pass; RPC-Node gesund, trenches lebt. **NEUE Signale seit Session 67 (09:35 UTC): (1) TORCH** `0x000050e18ffa…1111` (RH Chain 4663, mcap $11,5M liq $2,8M, 11 Tage alt) - **cosby (watch 60) kaufte 13:03 +$5,842**, Tagessumme **$25,4k in 5 Buys** (00:37-01:01 vier x ~$4,9k, 13:03 der fünfte) - Einzel-VIP-Akkumulation in einen etablierten Mid-Cap, KEIN Cluster (keine anderen Roster-Käufe in 24h), kein Burst-Gate-Kreuz. **(2) brezscales (watch 45, UNTER der Trust-Linie) kaufte 13:06 $9,951** in neues, noch unbenanntes Token `0xdcd885f5…` (mcap/liq noch nicht indiziert, naechster enrich ~13:19) - groesster Einzel-Buy des Tages, aber kein Trust-Signal (Score 45). (3) Exits: kyle verkaufte PONS $4,995 + AI $2,503 (11:07, Profit-Taking auf etablierten Bags), unipcs Mikro-Sells $47-1,285 (THEO/CA/SPCX/NVDA/gld/WETH, 11:29-11:38, WETH Quote-Asset). Kontext, nicht neu: ORBIO - frankdegods (60) $184k in 7 Buys 23:54-23:56 (20.10.), groesste 24h-Akkumulation, Einzel-Wallet, vor dem letzten Check. **Gewinner unveraendert:** FARMBLOCK (id 4) **+2.22x** (px 2.369e-05), Kohorte DCA-weiter: 19 Buys heute von 16 Wallet-Namen (unipcs, AvgJoesCrypto, ether_monk, 0xAvast u.a.), 0 Sells seit 16:45 gestern; eHook (id 5) +1.19x (px 2.788e-05, noch im Aufbau); TAPE/TOLL flach ~1.0-1.02x (mcap 63k/100k); PRIVACY (id 1) tot (x0.001, liq $0). Kein neuer Burst (letzter id 5 03:35, bursts 24h 1), keine neuen Tokens ueber dem Filter (ANYR 05:49 mcap 118k unter Filter; THEO/CA 11:38 als Sell-Hintergrund, alt), pushes 24h 0. Status unveraendert: 147 Trader (2 active / 68 watch / 15 idle / 1 tracking / 61 dropped), 0 neue in 7 Tagen; Top active: game_for_one 72, 0xAvast 70. Score-Queue LEER (pending_scores.json = der alte 2-Wallet-Export aus Session 65, laengst importiert; frischer run-Export liefert nichts Neues). **Naechste Aktionen (Entscheidung/Handgriff bei Max): nichts Dringendes - Pipeline, collect-loop und Watcher laufen. TORCH beobachten: cosby allein; steigen 2+ Trusted ein -> Report-SIGNAL, 3+ in 30 min -> Burst-Gate. brezscales-Token nach dem naechsten enrich ansehen (Name/Preis).** Keine neuen Keys noetig (FOMO_SESSION/ANTHROPIC/CODEX/HELIUS leer wie gehabt - nicht blockierend, Tracking auf freiem RPC, Scoring manual-Loop, Discovery ueber trenches). Keine Schluessel gedruckt.

Обновлено: 2026-10-21 (сессия 67).

**Session 67 (21. Okt, ~09:30-09:45 UTC): reiner Lese-Check (kein `run --once` - der collect-loop selbst lief sauber) - Pipeline gesund, KEINE neuen Signale seit Session 66.** Runs: #2734 track 08:56 ok, #2736 track 09:26->09:35 ok (25 Wallets / 0 trades / 0 errors / 426 RPC-Requests, volles Fenster), #2737 enrich ok; collect-loop LEBT (track+enrich alle ~20-30 min, alle 0 errors). Watcher LEBT (genau 1 Familie: Launcher 47276 0.02 s CPU + Worker 32752 51.97 s CPU, +8 s seit 08:30, Start 04:40, kein Doppel-Scan). **Keine neuen Signale seit 06:52 UTC:** letzter Trade 06:52 (die 4 Trades aus S66: SCHIFFY $9.7k buy Salem1299534 06:12, STOX $899 buy 31337___ 06:32, eHook $200 buy smol_intern 06:52, CHERRY $171 sell 31337___ 06:07), kein neuer Burst (letzter id 5 eHook 03:35), keine neuen Tokens (discover 06:02 147 seen / 0 new). Gewinner unveraendert: FARMBLOCK (id 4) **+2.22x** (px 1.07e-05 -> 2.37e-05), eHook (id 5) +1.19x (noch im Aufbau), TAPE/TOLL flach ~+1.02x, PRIVACY (id 1) tot (x0.001, Pool geleert). Score: 2 Verdicts heute 07:34 (game_for_one 72 active, 0xAvast 70 active) = Session-65-Import; Queue LEER (pending_scores.json = der 07:23-Export der 2 schon importierten Wallets, kein Backlog). Status unveraendert: 147 Trader (2 active / 68 watch / 15 idle / 1 tracking / 61 dropped), 0 neue in 7 Tagen. Keine neuen Keys noetig (ANTHROPIC/CODEX/HELIUS/FOMOAPI/X/FOMO_SESSION leer wie gehabt - nicht blockierend, Tracking auf freiem RPC, Scoring via manual-Loop). Keine Schluessel gedruckt.

Обновлено: 2026-10-21 (сессия 66).

**Session 66 (21. Okt, ~08:26-08:30 UTC): reiner Lese-Check (kein `run --once`, kein Code) - Pipeline gesund, keine neuen Signale seit dem 08:02-Lauf.** Letzter voller Lauf 08:02 (runs 2714-2723, 0 Fehler): discover_trenches 147 seen / 0 new / 147 updated, new_tokens checked 4 / new 0, track 25 Wallets / 0 trades / 0 errors / 426 RPC-Requests, holdings 1773 pairs (1357 held / 416 empty), crews 0. Seitdem: collect-loop LEBT (track+enrich alle ~20-30 min, letzter track #2732 08:24, alle 0 errors); Watcher LEBT (genau 1 Familie: Launcher 47276 0 CPU + Worker 32752 44 s CPU, Start 04:40, kein Doppel-Scan); Score-Queue LEER (frischer Export 0 / 1 nothing_to_judge `_logjam`). **Neue Aktivitaet seit 08:02: 4 Trades (3 buys / 1 sell) - SCHIFFY $9.7k buy von Salem1299534 (65 watch, mcap 5.2M liq 519k), STOX $899 buy von 31337___ (52, mcap 77k liq 132 - duenn), eHook $200 buy von smol_intern (60), CHERRY $171 sell von 31337___; kein neuer Burst (letzter id 5 eHook 03:35), keine neuen Tokens.** Gewinner unveraendert: FARMBLOCK (id 4) weiter **+2.22x** (px 1.07e-05 -> 2.37e-05), eHook (id 5) +1.19x (noch im Aufbau, Kaeufe 03:18-06:52), TAPE/TOLL flach ~+1.02x, PRIVACY (id 1) tot (x0.001, Pool geleert, mcap $92 liq $0.03). Status unveraendert: 147 Trader (2 active / 68 watch / 15 idle / 1 tracking / 61 dropped), 0 neue in 7 Tagen. Keine neuen Keys noetig (Codex/Helius/Anthropic/FOMO_SESSION leer wie gehabt - nicht blockierend, Tracking auf freiem RPC). Keine Schluessel gedruckt.

Обновлено: 2026-10-21 (сессия 65).

**Session 65 (21. Okt, ~07:34 UTC): Score-Workflow fuer die kleine Welle - 2 faellige Wallets (game_for_one 72, 0xAvast 70) durchgescort und importiert, beide bleiben active; Queue wieder LEER.** Auftrag (Chat, Max): die 2 aktiven Traders, deren 72h-Rescore-Fenster nach dem Session-60-Import gekreuzt hat, durchscoren. `score --export` frisch: **exported 2 / nothing_to_judge 1** (`_logjam`, по дизайну) / 0 bots - der pending_scores.json mit 70 Eintraegen auf der Platte ist der veraltete Session-60-Stand (schon importiert), ignoriert. Inline als Modell gescort (keine Delegation noetig bei 2): Verdicts-Skript im Profile-Scratch, Adressen byte-genau aus der Export-Datei uebernommen (Coverage assertet 2/2 exakt in Export-Reihenfolge), red_flags leer, status active|watch|dropped, style-Enum respektiert, Schema-Validierung 0 invalid. `score --import scoring_session65_results.json --model-label "manual"` -> **2 imported / 0 invalid / 0 unknown**, by_status 2 active / 0 watch / 0 dropped. DB-Verifikation (nicht nur Zaehler): **2 score_history-Zeilen heute (2026-10-21T07:34 UTC, Modell manual)**; Spot-Checks auf aktuellen traders-Zeilen bestaetigt: game_for_one 72 active, 0xAvast 70 active - beide bleiben active wie erhofft. Verteilung danach unveraendert: 147 Trader = 2 active / 68 watch / 15 idle / 1 tracking / 61 dropped. **Queue: LEER** - Nach-Export liefert `exported: 0, nothing_to_judge: 1` (nur `_logjam` ohne Beweise, по дизайну). Beleg: Verdicts-Datei unter profiles/fomo-radar/cache/scratch/scoring_session65_results.json (nicht im Repo; Repo-Arbeitsdateien keine, git status nur die bekannten untracked `--unscored`/`cache/` aus frueheren Sessions). Keine Schluessel gedruckt.

Обновлено: 2026-10-21 (сессия 64).

**Session 64 (21. Okt, ~03:47-04:10 UTC): voller `run --once` (runs 2696-2704) - 0 Fehler; collect-loop LEBT (track+enrich alle ~30 min, letzter 2705 04:00); Watcher LEBT (1 Familie bash 40080 -> python 47276 -> 32752, Start 04:40, kein Doppel-Scan) und schrieb NEUEN Burst id 5; Score-Queue weiter LEER.** Eigener Lauf statt DB-only (Discovery 1 h alt, Prezedenz 63): discover_trenches 147 seen / 0 new / 147 updated (lebt), fomo weiter skipped (fomo not configured), new_tokens checked 4 / new 0, resolve 0 (keine neuen Trader, letzter first_seen 22. Sep), track 25 Wallets / **0 trades** / 0 errors / 426 RPC-Requests (volles Fenster, штатно), holdings **1771 pairs (1356 held / 415 empty - weiter gewachsen von 1765)**, deployers 1 asked / 0 found, crews 0. Keine offenen runs. RPC-Node gesund, `_too_big` griff nicht; trenches lebt. **Watcher-Fund: LEBT und schrieb NEUEN Burst id 5 (03:35 UTC, Token eHook 0x87b7a1fb, mcap 7.6k, liq 7.4k, 3 Wallets AvgJoesCrypto 60/RugDalio 65/unipcs 60, conv 1.14, $399, age 1060 s)** - dieselbe VIP-Kohorte wie FARMBLOCK/TAPE/TOLL; genau 1 Familie (bash 40080 -> python 47276 -> 32752, Start 04:40, kein Doppel-Scan). Status unveraendert: 147 Trader (2 active / 68 watch / 15 idle / 1 tracking / 61 dropped), 0 neue in 7 Tagen. Top active: game_for_one 72, 0xAvast 70; Top watch: soby0x 68, Salem1299534 65, kyle 65, RugDalio 65, ether_monk 62, bluntz_capital 62, picadura 62. trades 24 h: **139** (6 h: 34, letzter 03:49 UTC - im ~72-130-Band), bursts 24h 1 (id 5 eHook), pushes 24h 0. **Gewinner:** FARMBLOCK (id 4) weiter **+2.22x** (px 1.067e-05 -> 2.369e-05), TAPE (id 3) +1.8%, TOLL (id 2) +2.1% (flach). **Naechste Aktionen (Entscheidung/Handgriff bei Max): nichts Dringendes - Pipeline, collect-loop und Watcher laufen; Score-Queue bleibt leer bis die Rescore-Fenster kreuzen (naechste Welle rechnerisch ~21:40 UTC 22. Okt, 72 h nach dem Session-60-Import 05:40), dann durchscoren/importieren.** Keine Schluessel gedruckt.

Обновлено: 2026-10-21 (сессия 63).

**Session 63 (21. Okt, ~02:31-02:43 UTC): voller `run --once` (runs 2682-2691) - 0 Fehler; collect-loop LEBT (track+enrich alle ~20-30 min, letzter 02:39, 0 errors); Watcher war TOT (Session-62-Familie 54036/41316 weg), neu gestartet (genau 1, Bar 1.0, pid 40080, tick 1, head 93940926); Score-Queue weiter LEER (frischer Export 0 / 1 nothing_to_judge).** Eigener Lauf statt DB-only (Discovery 9 h alt, letzter 17:29, Prezedenz 45/49-53/55/57-59/61/62): discover_trenches 147 seen / 0 new / 147 updated (lebt), fomo weiter skipped (fomo not configured), new_tokens checked 5 / new 4 (**MNTD** mcap 24.2M liq 316k, **Kimchi** 10.2M/5.26M, **Pepina** 3.17M/174k, **CREORA** 755k/128k - registriert 02:33, MNTD/Kimchi/Pepina ueber dem Signalfilter), resolve 0 (keine neuen Trader, letzter first_seen 22. Sep), track 25 Wallets / **0 trades** / 0 errors / 426 RPC-Requests (volles Fenster, штатно), holdings **1765 pairs (1350 held / 415 empty - weiter gewachsen von 1756)**, deployers 4 asked / 1 found, crews 0. Keine offenen runs. RPC-Node gesund, `_too_big` griff nicht; trenches lebt. **Watcher-Fund: TOT** - kein `cli watch`-Prozess, die Session-62-Familie (54036/41316, Start 05:29 UTC) ist weg (mit Konsole/Session gestorben); bursts 24h 0 (letzter Eintrag id 4 FARMBLOCK 14:39). Neu gestartet: pid 40080 (`env -u PYTHONPATH PYTHONIOENCODING=utf-8 ./.venv/Scripts/python -m fomo_agent.cli watch`, persist_on_release), Log bestaetigt `watch: every 20s, burst at +1.0 from 3 wallets in 30 min` (Bar 1.0), tickt (tick 1, head 93940926), 0 Fehler; verifiziert: genau 1 Watcher. **Neue Signale seit Session 62 (17:40 UTC 20.10):** kein neuer Burst ueber Bar 1.0; neue Tokens ueber dem Filter: **FABLES** (0xb63d07ce..., created 21:35, mcap 8.1M liq 1.03M, erster Trusted-Einstieg picadura 62 $2,997 um 21:43 - Einzel-VIP, noch kein Cluster), **Kimchi** (0xbca6f3f7..., created 00:45, mcap 10.2M liq 5.26M, noch keine Tracked-Fills), **MNTD** (0x62ed300a..., created 17:39, mcap 24.2M liq 316k, keine Fills); Cluster unter dem Gate: **ROOMS** (0x37b39526..., created 18:02, 3 Trusted smol_intern 60/RugDalio 65/AvgJoesCrypto 60, aber mcap 5.8k liq 4.2k < $10k-Gate). **Gewinner:** FARMBLOCK (Burst id 4, 14:39) jetzt **+2.22x** seit Burst (px 1.067e-05 -> 2.369e-05), Kohorte haelt (letzter Fill 16:45, keine Sells); TAPE (id 3) +1.8%, TOLL (id 2) +2.1% (flach). Status unveraendert: 147 Trader (2 active / 68 watch / 15 idle / 1 tracking / 61 dropped), 0 neue in 7 Tagen. Top active: game_for_one 72, 0xAvast 70; Top watch: soby0x 68, Salem1299534 65, kyle 65, RugDalio 65, ether_monk 62, bluntz_capital 62, picadura 62. trades 24 h: **138** (6 h: 33, letzter 01:35 UTC - im ~72-130-Band), bursts 24h 0, pushes 24h 0. **Naechste Aktionen (Entscheidung/Handgriff bei Max): nichts Dringendes - Pipeline, collect-loop und Watcher laufen; Score-Queue bleibt leer bis die Rescore-Fenster kreuzen (naechste Welle rechnerisch ~21:40 UTC 22. Okt, 72 h nach dem Session-60-Import 05:40), dann durchscoren/importieren.** Keine Schluessel gedruckt.

Обновлено: 2026-10-20 (сессия 62).

**Session 62 (20. Okt, ~17:28-17:40 UTC): voller `run --once` (runs 2628-2638) - 0 Fehler; collect-loop LEBT (track+enrich alle ~20-30 min, letzter 17:27, 0 errors); Watcher LEBT (1 Familie 54036/41316, Start 05:29 UTC) und schrieb einen NEUEN Burst (id 4); Score-Queue weiter LEER.** Eigener Lauf statt DB-only (Discovery 6,4 h alt, letzter 11:02, Prezedenz 45/49-53/55/57-59/61): discover_trenches 147 seen / 0 new / 147 updated (lebt), fomo weiter skipped (fomo not configured), new_tokens checked 1 / new 1 (**GIGATENEV** mcap 10.1M liq 9.78M, created 10-20 13:20, first_seen 17:29 - ueber dem Signalfilter), resolve 0 (keine neuen Trader, letzter first_seen 22. Sep), track 25 Wallets / **0 trades** / 0 errors / 426 RPC-Requests (volles Fenster, штатно), holdings **1756 pairs (1351 held / 405 empty - weiter gewachsen von 1728)**, deployers 6 asked / 4 found, crews 1 (2 Wallets), report 4322 B. Keine offenen runs. RPC-Node gesund, `_too_big` griff nicht; trenches lebt. **Watcher-Fund: LEBT und schrieb NEUEN Burst id 4 (14:39 UTC, Token FARMBLOCK, mcap 23.7k, liq 13.1k, 3 Wallets RugDalio 65/frankdegods 60/unipcs 60, conv 1.14, $369, age 714 s)** - zweiter Eintrag heute nach TAPE (id 3, 08:44); genau 1 Familie (54036/41316, Start 05:29 UTC, kein Doppel-Scan). Status unveraendert: 147 Trader (2 active / 68 watch / 15 idle / 1 tracking / 61 dropped), 0 neue in 7 Tagen. Top active: game_for_one 72, 0xAvast 70; Top watch: soby0x 68, Salem1299534 65, kyle 65, RugDalio 65, ether_monk 62, bluntz_capital 62, picadura 62. trades 24 h: **178** (6 h: 49, letzter 17:37 UTC - weiter ueber dem ~72-130-Band; aktivste 24 h: smol_intern 21, The__Solstice 14, AvgJoesCrypto 13, iruletrenches 11), bursts 24 h 2 (id 3 TAPE + id 4 FARMBLOCK), pushes 24 h 0. **Naechste Aktionen (Entscheidung/Handgriff bei Max): nichts Dringendes - Pipeline, collect-loop und Watcher laufen; Score-Queue bleibt leer bis die Rescore-Fenster kreuzen (naechste Welle rechnerisch ~21:40 UTC 22. Okt, 72 h nach dem Session-60-Import 05:40), dann durchscoren/importieren.** Keine Schluessel gedruckt.

Обновлено: 2026-10-20 (сессия 61).

**Session 61 (20. Okt, ~11:02-11:18 UTC): voller `run --once` (runs 2592-2601) - 0 Fehler; collect-loop LEBT (radar-sammler-Cron, track+enrich alle ~20-30 min, letzter 10:47, 0 errors); Watcher LEBT WIEDER (1 Familie 54036/41316, Start heute 05:29 UTC) und schrieb einen neuen Burst (id 3); Score-Queue weiter LEER (frischer Export 0 / 1 nothing_to_judge).** Eigener Lauf statt DB-only (Discovery 6,1 h alt, letzter 04:48, Prezedenz 45/49-53/55/57-59): discover_trenches 147 seen / 0 new / 147 updated (lebt), fomo weiter skipped (fomo not configured), new_tokens checked 5 / new 1 (**SEASON zweiter Mint** 0x5adfe... mcap 1.12M liq 144k, created 10-20 07:36 - gleiches Symbol, anderer Pool wie Session 59/Paper-Fall, ueber dem Signalfilter), resolve 0 (keine neuen Trader, letzter first_seen 22. Sep), track 25 Wallets / **0 trades** / 0 errors / 426 RPC-Requests (inkrementelles 5,8-h-Fenster, 24 transfers, 0 fills), holdings **1728 pairs (1326 held / 402 empty - weiter gewachsen von 1714)**, deployers 5 asked / 2 found, crews 1 (2 Wallets), score `--export` frisch **exported 0 / nothing_to_judge 1** (`_logjam`, по дизайну) - Queue leer bestaetigt. Keine offenen runs (auch der parallel laufende Loop-Track #2597 schloss regulär 11:17, 0 errors). RPC-Node gesund, `_too_big` griff nicht; trenches lebt. **Watcher-Fund: LEBT WIEDER** - genau 1 Familie (54036 Launcher / 41316 Worker, Start 07:29 lokal = 05:29 UTC, kein Doppel-Scan); der Watcher schrieb burst **id 3 (08:44 UTC, Token TAPE, mcap 63k, liq 12k, 3 Wallets iruletrenches/unipcs/AvgJoesCrypto alle 60, conv 1.08, $922, age 1057 s)** - erster Eintrag seit TOLL (id 2, 19. Okt 12:44); der offene Watcher-Restart aus Session 57 ist damit faktisch erledigt. Status unveraendert: 147 Trader (2 active / 68 watch / 15 idle / 1 tracking / 61 dropped), 0 neue in 7 Tagen. Top active: game_for_one 72, 0xAvast 70; Top watch: soby0x 68, Salem1299534 65, kyle 65, RugDalio 65, ether_monk 62, bluntz_capital 62, picadura 62. trades 24 h: **179** (6 h: 32, letzter 10:35 UTC - weiter ueber dem ~72-130-Band; aktivste 24 h: smol_intern 16, The__Solstice 14, MINHxDYNASTY 13, AvgJoesCrypto 12), bursts 24 h 2 (id 2 TOLL + id 3 TAPE), pushes 24 h 0. **Naechste Aktionen (Entscheidung/Handgriff bei Max): nichts Dringendes - Pipeline, collect-loop und Watcher laufen; Score-Queue bleibt leer bis die Rescore-Fenster kreuzen (naechste Welle rechnerisch ~21:40 UTC 22. Okt, 72 h nach dem Session-60-Import 05:40), dann durchscoren/importieren.** Keine Schluessel gedruckt.

**Session 60 (20. Okt, ~05:40 UTC): Score-Queue geschlossen - 70 Verdicts importiert (2 active / 68 watch / 0 dropped), DB-verifiziert; Queue LEER.** Auftrag (Chat, Max): Queue in pending_scores.json durchscoren (Subagenten-Pfad: export -> Slices a ~14 -> Verdicts -> import manual -> DB-Verifikation). **Stand-Korrektur:** Max nannte 125 Kontexte, tatsaechlich waren es **70** (pending_scores.json mtime 19. Okt 11:49, unveraendert 70 - der 125er-Stand war der Session-46-Export vom 14. Okt, laengst abgearbeitet; STATUS Session 59 sagte ebenfalls 70). `score --export` frisch: **exported 70 / nothing_to_judge 1** (`_logjam`, по дизайну) / 0 bots. Delegation in dieser One-shot-Session aus (oneshot_max_children=0, wie Session 47) -> inline als Modell gescort: Verdicts-Skript im Profile-Scratch, Adressen byte-genau aus der Export-Datei uebernommen (Coverage assertet 70/70 exakt in Export-Reihenfolge), red_flags nur aus dem Enum bot|bundler|insider-like|wash|one-hit (kein distributing), status active|watch|dropped, style-Enum respektiert, Schema-Validierung 0 invalid. `score --import scoring_20261020_results.json --model-label "manual"` -> **70 imported / 0 invalid / 0 unknown**, by_status 2 active / 68 watch / 0 dropped. DB-Verifikation (nicht nur Zaehler): **70 score_history-Zeilen heute (Modell manual)**; Spot-Checks auf aktuellen traders-Zeilen bestaetigt: game_for_one 72 active, 0xAvast 70 active, die 5 Trillionen-Artefakte alle watch (unipcs 60, Salem1299534 65, ogle 55, notanicecat69 55, DumbCrayonEater 50 - Kern der Burst-Kaeufer, wie gefordert nicht gedroppt), kyle 65 watch, bruisedwm 48 watch, techquant 22 dropped (unveraendert, nicht in dieser Welle), `_logjam` tracking/None (nothing_to_judge respektiert). Verteilung danach unveraendert: 147 Trader = 2 active / 68 watch / 15 idle / 1 tracking / 61 dropped. **Queue: LEER** - Nach-Export liefert `exported: 0, nothing_to_judge: 1` (nur `_logjam` ohne Beweise, по дизайну); erster leerer Stand seit 14. Okt. Beleg: Verdicts-Datei unter profiles/fomo-radar/cache/scratch/scoring_20261020_results.json (nicht im Repo; Repo-Arbeitsdateien keine, git status nur untracked cache/ aus Session 57, pending_scores.json gitignored). Keine Schluessel gedruckt.

**Session 59 (20. Okt, ~04:50 UTC): voller `run --once` (runs 2548-2556) - 0 Fehler; collect-loop LEBT (radar-sammler-Cron, track+enrich alle ~20-30 min, letzter 04:31, 0 errors); Watcher weiter TOT; Score-Queue unveraendert 70.** Eigener Lauf statt DB-only (Discovery 6,1 h alt, letzter 22:34, Prezedenz 45/49-53/55/57/58): discover_trenches 147 seen / 0 new / 147 updated (lebt), fomo weiter skipped (fomo not configured), new_tokens checked / new 3 (**W4WORK** mcap 3.85M liq 321k, **FSHIB** 1.24M/307k, **SEASON** 617k/41k - registriert 04:49, W4WORK/FSHIB ueber dem Signalfilter), resolve 0 (keine neuen Trader, letzter first_seen 22. Sep), track 25 Wallets / **1 trade** / 0 errors / 19 RPC-Requests (inkrementelles 5,8-h-Fenster, 45 transfers, 1 fill, 1 priced; `_too_big` teilte das 200k-Fenster sauber am 30k-Cap), holdings **1714 pairs (1314 held / 400 empty - weiter gewachsen von 1709)**, deployers/crews ok, score **70 Kontexte in pending_scores.json** (mtime 09:49, unveraendert 70 - wartet weiter auf Score im Chat), report ok. Keine offenen runs. RPC-Node gesund, `_too_big` griff nicht; trenches lebt. Watcher (`cli watch`) weiter TOT: kein Prozess, bursts 24h 1 (nur der TOLL-Burst 12:44 aus Session 57, kein neuer), pushes 24h 0 - Restart (interaktiv, persist_on_release, genau 1, Bar 1.0) weiter offen bei Max. Status unveraendert: 147 Trader (2 active / 68 watch / 15 idle / 1 tracking / 61 dropped), 0 neue in 7 Tagen. Top active: game_for_one 72, 0xAvast 70; Top watch: soby0x 68, Salem1299534 65, kyle 65, ether_monk 62, bluntz_capital 62, picadura 62. trades 24 h: **196** (6 h: 21, letzter 04:17 UTC - weiter lebhaft ueber dem ~72-130-Band), bursts 24h 1, pushes 24h 0. **Naechste Aktionen (Entscheidung/Handgriff bei Max): (1) Watcher-Restart weiter offen - kein `cli watch`-Prozess lebt, bursts-Gate dunkel seit dem TOLL-Burst 12:44; genau 1 `cli watch` (Bar 1.0) starten. (2) Score-Queue: 70 Kontexte durchscoren/importieren (Subagenten-Pfad oder Chat).** Keine Schluessel gedruckt.

**Session 58 (19. Okt, ~22:34-22:46 UTC): voller `run --once` (runs 2509-2517) - 0 Fehler; collect-loop LEBT (radar-sammler-Cron, track+enrich alle ~20-30 min, letzter 22:25, 0 errors); Watcher weiter TOT; Score-Queue unveraendert 70.** Eigener Lauf statt DB-only (Discovery 6,5 h alt, letzter 15:58, Prezedenz 45/49-53/55/57): discover_trenches 147 seen / 0 new / 147 updated (lebt), fomo weiter skipped (fomo not configured), new_tokens checked 8 / new 1 (**saluteface** mcap 4.8M liq 137k, created 10-19 14:38, first_seen 22:34 - ueber dem Signalfilter), resolve 0 (keine neuen Trader, letzter first_seen 22. Sep), track 25 Wallets / **0 trades** / 0 errors / 426 RPC-Requests (volles Fenster, штатно), holdings **1709 pairs (1309 held / 400 empty - weiter gewachsen von 1636)**, deployers 19 asked / 16 found, crews 0, score **70 Kontexte in pending_scores.json** (mtime 09:49, unveraendert 70 - wartet weiter auf Score im Chat), report ok. Keine offenen runs ausser #2518 (collect-loop-eigener track, Start 22:46, age 0,5 min - normal, kein Crash). RPC-Node gesund, `_too_big` griff nicht; trenches lebt; Gecko 429 auf enrich - fail-soft, штатно. Watcher (`cli watch`) weiter TOT: kein Prozess, bursts 24h 1 (nur der TOLL-Burst 12:44 aus Session 57, kein neuer), pushes 24h 0 - Restart (interaktiv, persist_on_release, genau 1, Bar 1.0) weiter offen bei Max. Status unveraendert: 147 Trader (2 active / 68 watch / 15 idle / 1 tracking / 61 dropped), 0 neue in 7 Tagen. Top active: game_for_one 72, 0xAvast 70; Top watch: soby0x 68, Salem1299534 65, kyle 65, ether_monk 62, bluntz_capital 62, picadura 62. trades 24 h: **178** (6 h: 88, letzter 22:25 UTC - weiter lebhaft ueber dem ~72-130-Band, aktivste 24 h: 0x194db29f 17, 0xaf3a73c1 14, 0xa984149d 12), bursts 24h 1, pushes 24h 0. **Naechste Aktionen (Entscheidung/Handgriff bei Max): (1) Watcher-Restart weiter offen - kein `cli watch`-Prozess lebt, bursts-Gate dunkel seit dem TOLL-Burst 12:44; genau 1 `cli watch` (Bar 1.0) starten. (2) Score-Queue: 70 Kontexte durchscoren/importieren (Subagenten-Pfad oder Chat).** Keine Schluessel gedruckt.

**Session 57 (19. Okt, ~15:58-16:27 UTC): voller `run --once` (runs 2469-2474) - 0 Fehler; collect-loop LEBT (radar-sammler-Cron, track+enrich alle ~20-30 min, letzter 15:45, 0 errors); NEU: bursts-Gate hat wieder gefeuert (burst id 2, 12:44 UTC, TOLL) - erster Eintrag seit dem PRIVACY-Burst 15. Okt; Score-Queue unveraendert 70.** Eigener Lauf statt DB-only (Discovery 6,1 h alt, letzter 09:48, Prezedenz 45/49-53/55): discover_trenches 147 seen / 0 new / 147 updated (lebt), fomo weiter skipped (fomo not configured), new_tokens checked 7 / new 5 (**PONS** mcap 252.6M liq 91.1M, **UHI** 14.0M/187k, **PAPER** 10.2M/638k, **Mimi** 3.2M/84k, **DSKBK** 873k/267k - registriert 15:58, PONS/UHI/PAPER ueber dem Signalfilter), resolve 0 (keine neuen Trader, letzter first_seen 22. Sep), track 25 Wallets / **0 trades** / 0 errors / 426 RPC-Requests (volles Fenster, штатно), holdings **1636 pairs (1240 held / 396 empty - weiter gewachsen von 1600)**, deployers 0, crews 0, score **70 Kontexte in pending_scores.json** (mtime 09:49, unveraendert 70 - wartet weiter auf Score im Chat), report ok. **Toter track-Run #2460 (14:13, finished_at NULL, 1h43m alt bei ~10-min-Norm) als `interrupted (dead process)` markiert** - danach keine offenen runs. RPC-Node gesund, `_too_big` griff nicht; trenches lebt. **Burst-Fund: bursts id 2 am 12:44 UTC (Token TOLL, mcap 100k, liq 16k, 3 Wallets alle Score 60: iruletrenches/unipcs/AvgJoesCrypto, $1,623, conviction 1.08, age 945s, px 9.8e-07) - das Gate hat wieder gefeuert, erster Eintrag seit PRIVACY 15. Okt; ABER kein `cli watch`-Prozess laeuft aktuell (nur meine eigenen Scan-Prozesse) - der Watcher, der den Burst schrieb, ist wieder weg (Restart weiter offen bei Max).** Status unveraendert: 147 Trader (2 active / 68 watch / 15 idle / 1 tracking / 61 dropped), 0 neue in 7 Tagen. Top active: game_for_one 72, 0xAvast 70; Top watch: soby0x 68, Salem1299534 65, kyle 65, ether_monk 62, bluntz_capital 62, picadura 62. trades 24 h: **118** (6 h: 28, letzter 15:43 UTC - deutlich lebhafter als Session 55 (3), wieder im ~72-130-Band), bursts 24h 1, pushes 24h 0. **Naechste Aktionen (Entscheidung/Handgriff bei Max): (1) Watcher-Restart weiter offen - der Burst 12:44 beweist, dass das Gate funktioniert, aber kein Watcher-Prozess lebt; genau 1 `cli watch` (Bar 1.0) starten. (2) Score-Queue: 70 Kontexte durchscoren/importieren (Subagenten-Pfad oder Chat).** Keine Schluessel gedruckt.

**Session 55 (19. Okt, ~05:38-05:42 UTC): voller `run --once` (runs 2404-2408) - 0 Fehler; collect-loop LEBT (radar-sammler-Cron, track alle ~25-30 min, 23 runs heute, 0 errors), Watcher weiter TOT; Score-Queue unveraendert 70.** Eigener Lauf statt DB-only (Prezedenz 45/49-54): discover_trenches 147 seen / 0 new / 147 updated (lebt), fomo weiter skipped (fomo not configured), new_tokens checked / new 2 (**Paper** mcap 10.2M liq 1.18M, **FLFLT** 1.49M/358k - registriert 02:26/02:28, Paper ueber dem Signalfilter), resolve 0 (keine neuen Trader, letzter first_seen 22. Sep), track 25 Wallets / **1 trade** / 0 errors / 19 RPC-Requests (inkrementelles 5,7-h-Fenster, 23 transfers, 1 fill; `_too_big` teilte das 200k-Fenster sauber am 30k-Cap), holdings **1600 pairs (1209 held / 391 empty - weiter gewachsen von 1599)**, deployers 0, crews 0, score **70 Kontexte in pending_scores.json** (generated_at 05:41, unveraendert 70 - wartet weiter auf Score im Chat), report ok. Keine offenen runs (alle heute geschlossen). RPC-Node gesund, `_too_big` griff sauber; trenches lebt. Watcher (`cli watch`) weiter TOT: kein Prozess, bursts 24h 0 (letzter Eintrag PRIVACY 15. Okt 16:42), pushes 24h 0 - Restart (interaktiv, persist_on_release, genau 1, Bar 1.0) weiter offen bei Max. Status unveraendert: 147 Trader (2 active / 68 watch / 15 idle / 1 tracking / 61 dropped), 0 neue in 7 Tagen. Top active: game_for_one 72 (26 trades), 0xAvast 70 (8 trades); Top watch: soby0x 68, Salem1299534 65, kyle 65, ether_monk 62, bluntz_capital 62, picadura 62. trades 24 h: **3** (6 h: 3, letzter 02:56 UTC - weiter sehr ruhig, im Vergleich zu Session 54 (53) deutlich abgeflaut), bursts 24h 0, pushes 24h 0. **Naechste Aktionen (Entscheidung/Handgriff bei Max): (1) Watcher-Restart weiter offen (bursts-Gate dunkel seit 15. Okt). (2) Score-Queue: 70 Kontexte durchscoren/importieren (Subagenten-Pfad oder Chat).** Keine Schluessel gedruckt.

**Session 54 (18. Okt, ~21:34 UTC): voller `run --once` (runs 2369-2379) - 0 Fehler; collect-loop LEBT wieder (radar-sammler-Cron), Watcher weiter TOT; Score-Queue unveraendert 70.** Eigener Lauf statt DB-only (Discovery 6,1 h alt, Prezedenz 45/49-53): discover_trenches 147 seen / 0 new / 147 updated (lebt), fomo weiter skipped (fomo not configured), new_tokens checked 5 / new 1 (**EMRUN** mcap 1.55M - registriert, unter Signalfilter), resolve 0 (keine neuen Trader, letzter first_seen 22. Sep), track 25 Wallets / 1 trade / 0 errors / 19 RPC-Requests (inkrementelles 5,6-h-Fenster; `_too_big` teilte am 30k-Cap sauber), holdings **1599 pairs (1208 held / 391 empty - weiter gewachsen von 1590)**, deployers 1 asked / 1 found, crews 0, score **70 Kontexte** in pending_scores.json (1 nothing_to_judge, `_logjam`) - unveraendert, wartet weiter auf Score im Chat, report 2323 B. **collect-loop-Fund: der `radar-sammler`-Cron im DEFAULT-Profil (7ae21931d484, Intervall 20 min) ist seit Session 53 aktiv und schrieb 12 track + 12 enrich-Runs (cadence ~26 min, alle 0 errors, letzter 21:22 UTC) - der Totraum 16.-18. Okt war die ausgeschaltete Maschine, kein Job-Verlust; Session-53-Meldung "collect-loop nicht geplant" damit korrigiert (der Job existiert, er lag nur brach).** Watcher (`cli watch`) weiter TOT: kein Prozess, bursts 24h 0 (letzter Eintrag PRIVACY 15. Okt 16:42), pushes 0 - Restart (interaktiv, persist_on_release, genau 1, Bar 1.0) weiter offen bei Max. Status unveraendert: 147 Trader (2 active / 68 watch / 15 idle / 1 tracking / 61 dropped), 0 neue in 7 Tagen. Top active: game_for_one 72 (win 100%, 26 trades), 0xAvast 70 (15 trades); Top watch: soby0x 68, Salem1299534 65, kyle 65, ether_monk 62, bluntz_capital 62, picadura 62. trades 24 h: **53** (6 h: 33, letzter 20:55 UTC; aktivste 24 h: The__Solstice 10, loganlim_x 7, RugDalio 7 - im Vergleich zu Session 52/51 (227/232) wieder deutlich ruhiger), bursts 24h 0, pushes 24h 0. **Naechste Aktionen (Entscheidung/Handgriff bei Max): (1) Watcher-Restart weiter offen (bursts-Gate dunkel seit 15. Okt). (2) Score-Queue: 70 Kontexte durchscoren/importieren (Subagenten-Pfad oder Chat).** Keine Schluessel gedruckt.

**Session 53 (18. Okt, ~15:22-15:25 UTC): voller `run --once` (runs 2334-2344) - 0 Fehler; ABER Pipeline war ~2,6 Tage TOT (16. Okt 00:56 -> 18. Okt 15:22): keine runs, keine trades, kein Watcher, kein collect-loop seit 15. Okt 22:54; auch der 6-h-Loop-Cron selbst war verspaetet (catch_up, lateness ~60 h - Maschine/Session war aus).** Eigener Lauf statt DB-only (Discovery 66 h alt): discover_trenches 147 seen / 0 new / 147 updated (lebt), fomo weiter skipped (fomo not configured), new_tokens checked / new 6 (**BOOMER** mcap 21.3M, **hi** 16.6M, **TSI** 12.2M, **ESI** 6.1M, **金钱自由** 5.0M, **SUPERCORE** 3.5M - alle ueber dem Signalfilter, registriert), resolve 0 (keine neuen Trader, letzter first_seen 22. Sep), track 25 Wallets / **5 trades** / 0 errors / 20 RPC-Requests (inkrementelles 5,7-h-Fenster, 41 transfers, 5 fills; `_too_big` teilte das 200k-Fenster sauber am 30k-Cap), holdings **1590 pairs (1202 held / 388 empty - weiter gewachsen von 1587)**, deployers ok, crews 1 (2 Wallets), score **70 Kontexte in pending_scores.json** (mtime 15:24:47; war letzte Session 0/leer - das 72-h/14-Tage-Rescore-Fenster ist gekreuzt, Queue wartet auf Score im Chat), report ok. Gecko 429 auf enrich - fail-soft, штатно. Status unveraendert: 147 Trader (2 active / 68 watch / 15 idle / 1 tracking / 61 dropped), 0 neue in 7 Tagen. Top active: game_for_one 72 (75% win, 19 trades, +$675 realized, aber net -$2.6k durch 3 offene Bags), 0xAvast 70 (net +$224k, 133 offene Bags, Sniper); Top watch: soby0x 68, Salem1299534 65, kyle 65, ether_monk 62, bluntz_capital 62, picadura 62. trades 24 h: 5 (alle im frischen Fenster, letzter 14:46 UTC - die 24-h-Zahl ist durch den Ausfall verzerrt), bursts 24 h 0, pushes 24 h 0. **Naechste Aktionen (Entscheidung/Handgriff bei Max): (1) collect-loop (scripts/collect_loop.sh, 30-min track+enrich) und Watcher (`cli watch`) sind TOT und NICHT geplant - kein Windows-Task, kein Cron-Job; sie kommen nicht von selbst zurueck, nur der 6-h-Loop haelt die Pipeline am Leben. Restart noetig (interaktiv, persist_on_release, genau 1 Watcher, Bar 1.0). (2) Score-Queue: 70 Kontexte durchscoren/importieren (Subagenten-Pfad oder Chat).** Keine Schluessel gedruckt.

**Session 52 (15. Okt, ~20:45-20:58 UTC): voller `run --once` (runs 2314-2325) - 0 Fehler; Discovery war 6,3 h alt (letzter 14:25), jetzt frisch; Queue weiter LEER; Watcher lebt; ERSTER BURST seit 12. Okt aufgezeichnet (PRIVACY, 16:42 UTC) - Gate funktioniert, Signal erwies sich als Verlustfall.** Eigener Lauf statt DB-only (Loop-Takt ~6 h, Prezedenz Session 45/49/50/51): discover_trenches 147 seen / 0 new / 147 updated (lebt), fomo weiter skipped (fomo not configured), new_tokens checked 5 / new 3 (**Dacity** mcap 17.2M liq 409k, **Doge Pepe** 3.5M/183k, **DOPE** 2.1M/84k - registriert 20:47, alle ueber dem Signalfilter), resolve 0 (keine neuen Trader, letzter first_seen 22. Sep), track 25 Wallets / 0 trades / 0 errors / 426 RPC-Requests (volles Fenster; der Loop-Track #2313 20:41-20:51 crawlt parallel, beides dedupliziert ueber fill_key wie Session 49-51), holdings **1587 pairs (1228 held / 359 empty - weiter gewachsen von 1531)**, deployers 7 asked / 3 found, crews 1 (3 Wallets), score **exported 0 / nothing_to_judge 1** (`_logjam`, по дизайну) - Queue leer bestaetigt (pending_scores.json 0 Wallets), report 8126 B. Keine offenen runs (2313 und 2318 beide regulär geschlossen; Loop-enrich 2319/2320 ok). RPC-Node gesund, `_too_big` griff nicht; trenches lebt. Watcher: **genau 1 Familie (98996/101780, Bar 1.0, Start 14. Okt 19:53 UTC)** - unveraendert, lebt, kein Doppel-Scan; der erste bursts-Eintrag seit 12. Okt (id 1) wurde vom Watcher selbst geschrieben: **PRIVACY 16:42 UTC, conv 2.05, 5 Wallets (soby0x 68/kyle 65/picadura 62/Salem1299534 65/unipcs 60), $6.3k, age 425 s** - Pool created 16:33, erste VIP-Kaeufe 16:50-16:52, danach leerlaufender Pool: jetzt liq $0.24, mcap $1.5k, Preis ~53× unter Einstieg (px 8.17e-05 -> 1.55e-06). Gate beweist Funktion, aber dieser Burst waere ein Verlust gewesen; pushes 24 h 0 (keine aktiven Subscriber, wie gehabt). Fills 24 h: **227** (6 h: 137, letzter 20:34 UTC - weiter deutlich ueber dem ~72-130-Band der Vortage, 6-h-Zahl so hoch wie seit Tagen nicht), bursts 24 h 1, pushes 24 h 0. Status unveraendert: 147 Trader (2 active / 68 watch / 15 idle / 1 tracking / 61 dropped), 0 neue in 7 Tagen. Top active: game_for_one 72 (23.5k foll), 0xAvast 70 (277k foll); Top watch: soby0x 68, Salem1299534 65, kyle 65, ether_monk 62, bluntz_capital 62, picadura 62. Naechste Schritte: nichts Dringendes - Queue leer, Score erst wieder wenn die Rescore-Fenster (72 h/14 d) kreuzen (naechste Welle rechnerisch ~21:24 UTC, 72 h nach dem 14.-Okt-Import - moeglicherweise gerade heute Abend faellig); PRIVACY-Burst beobachten: wenn weitere Cluster dieser Art (fruehe VIP-Kaeufe, dann Pool-Drain) haeufiger werden, ist der Bar 1.0 evtl. zu niedrig - Entscheidung bei Max, kein Code-Eingriff jetzt. Keine Schluessel gedruckt.

**Session 51 (15. Okt, ~14:25-14:36 UTC): voller `run --once` (runs 2280-2291) - 0 Fehler; Discovery war 6,2 h alt (letzter 08:15), jetzt frisch; Queue weiter LEER; Watcher lebt.** Eigener Lauf statt DB-only (Loop-Takt ~6 h, Prezedenz Session 45/49/50): discover_trenches 147 seen / 0 new / 147 updated (lebt), fomo weiter skipped (fomo not configured), new_tokens checked 3 / new 1 (**Paper** mcap 10.5M liq 10.1M, created 11:56 UTC - registriert; FTR 219k/109k, create Sep 12, erstmals auf dem Tape), resolve 0 (keine neuen Trader, letzter first_seen 22. Sep), track 25 Wallets / 0 trades / 0 errors / 426 RPC-Requests - Loop-Track #2285 (14:27-14:36) crawlt dasselbe volle Fenster parallel, beide deduplizieren ueber fill_key (wie Session 49/50), enrich named 233 / priced 86, holdings **1531 pairs (1179 held / 352 empty - weiter gewachsen von 1522)**, deployers 3 asked / 1 found, crews 1 (3 Wallets), score **exported 0 / nothing_to_judge 1** (`_logjam`, по дизайну) - Queue leer bestaetigt (pending_scores.json 0 Wallets, mtime 14:35), report 7937 B. Keine offenen runs (Loop-enrich #2292 startete 14:37 und schloss regulaer). RPC-Node gesund, `_too_big` griff nicht; trenches lebt. Watcher: **genau 1 Familie (98996/101780, Bar 1.0, Start 14. Okt 19:53 UTC)** - unveraendert, lebt, kein Doppel-Scan. Fills 24 h: **232** (6 h: 25, letzter 14:24 UTC - weiter deutlich ueber dem ~72-130-Band der Vortage), bursts 24 h 0, pushes 24 h 0. Status unveraendert: 147 Trader (2 active / 68 watch / 15 idle / 1 tracking / 61 dropped), 0 neue in 7 Tagen. Top active: game_for_one 72, 0xAvast 70; Top watch: soby0x 68, Salem1299534 65, kyle 65, ether_monk 62, bluntz_capital 62, picadura 62. Naechste Schritte: nichts Dringendes - Queue leer, Score erst wieder wenn die Rescore-Fenster (72 h/14 d) kreuzen (naechste Welle ~21:24 UTC, 72 h nach dem 14.-Okt-Import); Watcher-Thema erledigt (1 Prozess, Bar 1.0). Keine Schluessel gedruckt.

Обновлено: 2026-10-15 (сессия 50).

**Session 50 (15. Okt, ~08:15-08:20 UTC): voller `run --once` (runs 2246-2257) - 0 Fehler; Discovery war 6,1 h alt (letzter 02:10), jetzt frisch; Queue weiter LEER; Watcher 1x gesund.** Eigener Lauf statt DB-only (Loop-Takt ~6 h, Prezedenz Session 45/49): discover_trenches 147 seen / 0 new / 147 updated (lebt), fomo weiter skipped (fomo not configured), new_tokens checked 7 / new 2 (**WOLFPACK** mcap 5.03M liq 645k, **GMOTH** 1.65M/177k - registriert, beide ueber dem Signalfilter; DARWIN 97k/23k darunter), resolve 0 (keine neuen Trader, letzter first_seen 22. Sep), track 25 Wallets / 0 trades / 0 errors / 207 RPC-Requests inkrementell - der Loop-Track #2245 (08:07-08:16, 0 errors) hatte das Fenster eben selbst gecrawlt, beide Passes liefen parallel und deduplizieren ueber fill_key (wie Session 49 mit #2210), holdings **1522 pairs (1171 held / 351 empty - weiter gewachsen von 1513)**, deployers 2 asked / 1 found, crews 1 (3 Wallets), score **exported 0 / nothing_to_judge 1** (`_logjam`, по дизайну) - Queue leer bestaetigt (pending_scores.json 0 Wallets, regeneriert), report 8030 B. Keine offenen runs (auch der parallel laufende Loop-Track schloss regulär). RPC-Node gesund, `_too_big` griff nicht; trenches lebt. Watcher: **genau 1 Familie (98996/101780, Bar 1.0, Start 14. Okt 19:53 UTC)** - unveraendert seit Session 49, lebt, kein Doppel-Scan (beide pids aktiv). Fills 24 h: **229** (6 h: 30, letzter 08:19 UTC - weiter lebhaft ueber dem ~72-130-Band der Vortage), bursts 24 h 0, pushes 24 h 0 (Watcher lebt, keine Cluster ueber Bar 1.0). Status unveraendert: 147 Trader (2 active / 68 watch / 15 idle / 1 tracking / 61 dropped), 0 neue in 7 Tagen. Top active: game_for_one 72, 0xAvast 70; Top watch: soby0x 68, Salem1299534 65, kyle 65, ether_monk 62, bluntz_capital 62, picadura 62. Naechste Schritte: nichts Dringendes - Queue leer, Score erst wieder wenn die Rescore-Fenster (72 h/14 d) kreuzen; Watcher-Thema aus Session 38/42 erledigt (1 Prozess, Bar 1.0). Keine Schluessel gedruckt.

**Session 49 (15. Okt, ~02:05-02:10 UTC): voller `run --once` (runs 2211-2221) - 0 Fehler; Discovery war 6,6 h alt, jetzt frisch; Score-Queue weiter LEER; verwaister track #2187 als tot markiert.** Eigener Lauf statt DB-only (Prezedenz Session 45): discover_trenches 147 seen / 0 new / 147 updated (lebt), fomo weiter skipped (fomo not configured), new_tokens checked 7 / new 2 (ODDSINU mcap 1.06M - registriert, unter Signalfilter), resolve 0 (keine neuen Trader, letzter first_seen 22. Sep), track 25 Wallets / 0 trades / 0 errors / 19 RPC-Requests inkrementell - der 27-min-Loop hatte das volle Fenster eben selbst gecrawlt (#2210 02:00-02:09, 426 Requests, 0 trades, 0 errors; beide Passes deduplizieren ueber fill_key), enrich 2x ok, holdings 1513 pairs (1169 held / 344 empty - gewachsen von 1095), deployers 4, crews 1 (3 Wallets), score **exported 0 / nothing_to_judge 1** (`_logjam`, по дизайну) - Queue leer bestaetigt; die 125 Wallets in pending_scores.json waren der veraltete Session-46-Export, Lauf 2218 hat die Datei frisch mit 0 ueberschrieben. **Verwaister track #2187 (14. Okt 20:33, finished_at NULL, 5,5 h alt bei ~545 s Norm) als `interrupted (dead process)` markiert** - danach keine offenen Runs mehr (2210 schloss regulaer 02:09:48, auch 2222 enrich fertig). RPC-Node gesund, `_too_big` erkannte das 30k-Bloecke-Cap sauber und teilte das Fenster (kein Fehler); trenches lebt. Watcher: **genau 1 Familie (98996/101780, Start 14. Okt 19:53 UTC, Bar 1.0)** - lebt, kein Doppel-Scan. Fills 24 h: **206** (6 h: 46, letzter 02:03 UTC - deutlich lebhafter als ~72-130 der Vortage; aktivster Trader smol_intern 22 Fills/6 h, watch 60), bursts 24 h 0, pushes 24 h 0 (Watcher lebt, nur keine Cluster ueber Bar 1.0 seit gestern). Status unveraendert: 147 Trader (2 active / 68 watch / 15 idle / 1 tracking / 61 dropped), 0 neue in 7 Tagen. Top active: game_for_one 72, 0xAvast 70; Top watch: soby0x 68, Salem1299534 65, kyle 65, ether_monk 62, bluntz_capital 62, picadura 62. Naechste Schritte: nichts Dringendes - Queue leer, Score erst wieder wenn die Rescore-Fenster (72 h/14 d) kreuzen; Watcher-Rest von Session 38/42 (4 Prozesse) ist durch den einen gesunden Bar-1.0-Prozess faktisch erledigt. Keine Schluessel gedruckt.**

**Session 48 (14. Okt, ~21:42 UTC): Sammel-OK für den 125er-Rescore — Queue bereits LEER, nichts zu scorcen (Session 46+47 hatten die Welle heute komplett geschlossen).** Auftrag (Chat, Max, Sammel-OK): verbleibende Queue per Subagenten-Pfad (export → 5 Slices à 25 → Import `manual`). Geprüft statt blind neu gescort: der Stand "125 Kontexte" aus dem Session-46-Bericht (mtime 21:40) ist bereits Vollzug — heute 125 score_history-Zeilen (51 um 21:06 `manual:deepseek-v4-flash`, 74 um 21:24 `manual:deepseek-v4-flash-0731`), letzter Verdict 21:24:26 UTC. Live-Export eben (`score --export` frisch): **exported: 0, nothing_to_judge: 1** (`_logjam`, по дизайну) — der Nach-Export beweist die leere Queue, kein Re-Score nötig (ein Re-Score hätte heute bereits gefällte Kontexte überschrieben und die Rescore-Fenster 72 h/14 Tage verletzt). DB-Verifikation (nicht nur Zähler): Verteilung heute 2 active / 68 watch / 55 dropped, Trader-Gesamt 147 = 2 active / 68 watch / 15 idle / 1 tracking / 61 dropped; Spot-Checks auf aktuelle Zeilen bestätigt — game_for_one 72 active, 0xAvast 70 active, die 5 Trillionen-Artefakte alle watch (unipcs 60, Salem1299534 65, ogle 55, notanicecat69 55, DumbCrayonEater 50 — Kern der Burst-Käufer, wie gefordert nicht gedroppt). Kein Slicing, kein Import, keine Code-Änderung; Arbeitsdatei `scoring_20261014_late.json` (0 Wallets) liegt im Profile-Scratch, Repo sauber. Nächster Score erst wieder, wenn Kontexte die regulären Fenster kreuzen. Keine Schlüssel gedruckt.

**Session 47 (14. Okt, ~21:35 UTC): Score-Queue leer — 74 Verdicts importiert (30 watch / 44 dropped), DB-verifiziert; Delegation war in dieser Session aus (oneshot_max_children=0), daher inline gescort.** Auftrag (Chat, Max): voller Score-Workflow — export → LLM-Verdicts → import → DB-Verifikation; Empfehlung: die 5 Trillionen-Artefakte (unipcs/Salem1299534/ogle/notanicecat69/DumbCrayonEater) → watch statt dropped (Kern der Burst-Käufer), game_for_one bleibt active. **Stand vorher:** Session 46 importierte um 21:06 bereits 51 der 125 fälligen (2 active — game_for_one 72, 0xAvast 70 — / 38 watch / 11 dropped, `manual:deepseek-v4-flash`), damit waren die 5 Artefakte schon korrekt als watch gesetzt (unipcs 60, Salem1299534 65, ogle 55, notanicecat69 55, DumbCrayonEater 50 — jeder Summary nennt die Trillionen-PnL als unrealisiert/Artefakt). **Meine Welle (Rest):** `score --export` → 74 Wallets / 1 nothing_to_judge (`_logjam`, по дизайну) / 0 bots. Skill-Regel „14er-Slices per Subagent" war nicht einlösbar (delegation.oneshot_max_children=0 in dieser One-shot-Session → delegate_task verweigert; Config selbst ist gesund: deepseek-v4-flash-0731/nous) → inline als Modell gescort: Verdicts-Skript im Profile-Scratch, Adressen byte-genau aus der Export-Datei übernommen (kein Hand-Abschreiben), Abdeckung assertet 74/74 exakt in Export-Reihenfolge, red_flags nur aus dem Enum bot|bundler|insider-like|wash|one-hit (kein `distributing`), status active|watch|dropped, style-Enum respektiert. `score --import scratch_results.json --model-label "manual:deepseek-v4-flash-0731"` → **74 imported / 0 invalid / 0 unknown**, by_status 30 watch / 44 dropped (0 active — die aktiven lagen bereits in der 21:06-Welle). DB-Verifikation (nicht nur Zähler): 125 score_history-Zeilen heute (51 um 21:06 + 74 um 21:24); Spot-Checks auf aktuellen `traders`-Zeilen bestätigt: game_for_one 72 active, unipcs 60 watch, Salem1299534 65 watch, ogle 55 watch, notanicecat69 55 watch, DumbCrayonEater 50 watch, kyle 65 watch (auch er verkauft gegen die Kasse, +$1.37M Buch), bruisedwm 48 watch (+$7k, 13 Trades in 7 d — der frühere tracking-Kandidat), techquant 22 dropped. Verteilung danach: 147 Trader = 2 active / 68 watch / 15 idle / 1 tracking / 61 dropped (tracking 3→1: bruisedwm→watch, techquant→dropped durch diese Welle). **Queue: LEER** — Nach-Export liefert `exported: 0, nothing_to_judge: 1` (nur `_logjam` ohne Beweise, по дизайну); erster leerer Stand seit 11. Okt (der 125er-Stand war der reguläre 72-h/14-Tage-Rescore, nicht Stau). Beleg: Verdicts-Datei unter `profiles/fomo-radar/cache/scratch/scoring_20261014_results.json` (nicht im Repo; Repo-Arbeitsdateien `scratch_*` wieder entfernt, `git status` sauber). Keine Schlüssel gedruckt.

**Session 46 (14. Okt, ~22:30 UTC): Score-Loop geschlossen — 51 Verdicts importiert (2 active / 38 watch / 11 dropped); alle CLI-Aufrufer gegen die PYTHONPATH-Kollision gehärtet.** Auftrag aus dem Chat ("score --export und weiter"): `score --export` (51 Wallets, 25 nothing_to_judge, 0 bots), 4 parallele Subagenten (deleg_1093a30d, 14/14/14/9 Wallets, deepseek-v4-flash, jeder las instructions/schema aus der Export-Datei), Aggregation aus der Batch-Result-Datei (einzige Quelle der Verdicts — Transkript-Logs halten nur den Kickoff), Abdeckung 51/51 geprüft (keine fehlenden/extra Adressen), Schema-Validierung (Status-Enum, red_flags-Enum bot|bundler|insider-like|wash|one-hit, Style-Enum, Score-Bereich, confidence) → `score --import` sauber: **51 imported / 0 invalid / 0 unknown**, by_status 2/38/11, Modell-Label `manual:deepseek-v4-flash`. DB-Verifikation: 51 score_history-Zeilen heute, Spot-Check bestätigt aktive Verdicts (game_for_one 72 active, 0xAvast 70 active — Cryptoaeon zurück auf dropped 30, AvgJoesCrypto watch 60); Trader-Verteilung jetzt 2 active / 39 watch / 15 idle / 3 tracking / 88 dropped (3 watch→dropped durch den Import). **PYTHONPATH-Fix verbreitert (Session-42-Regel war nur Cron-Prompt):** `scripts/collect_loop.sh` (der radar-sammler-Cron, `cli track`+`enrich-tokens` alle ~720 s) rief die CLI ohne `env -u PYTHONPATH` — exakt der Pfad, der track #2064 (`ModuleNotFoundError: fomo_agent.pipeline.provenance`, cp314-PYTHONPATH aus der Hermes-Session gegen cp313-venv) erzeugte; `PY=.venv/Scripts/python` → `PY="env -u PYTHONPATH .venv/Scripts/python"`. Cron-Job `fomo-radar Loop` (0708b8f2725d) Prompt neu gesetzt mit der Regel (der alte Prompt enthielt sie schon laut Session 42, wurde redundant formuliert). Keine weiteren CLI-Aufrufer im Repo gefunden (deploy/* systemd auf dem Server nutzen /opt/fomoradar/venv — dort gilt die Kollision nicht). **Queue nach Import: pending_scores.json 125 Kontexte (mtime 21:40, reguläres Rescore-Fenster — 42 watch kreuzten das 72-h-Fenster, dropped-Alterungen ins 14-Tage-Fenster; die 51 heute importierten sind darin NICHT mehr enthalten, 125 sind die verbleibenden fälligen).** Nächste Schritte: die 125 per gleichem Subagenten-Pfad durchscoren (5 Slices à 25) oder im Chat, danach Watcher-Entscheidung von Session 42/45 (genau 1 `cli watch` pid 62552 läuft, Bar 1.0). Keine Schlüssel gedruckt.

**Session 45 (14. Okt, ~19:30-19:50 UTC): voller `run --once` (runs 2172-2184) - 0 Fehler; Watcher war tot, neu gestartet; Scoring-Queue 53 -> 125 (regulaeres Rescore-Fenster, kein Stau).** Discovery war ~6,5 h alt (letzte volle Discovery 13:02, Loop-Takt 6 h) -> eigener Lauf statt DB-only (Prezedenz Session 44). Full pass: discover_trenches 147 seen / 0 new / 147 updated (lebt), fomo weiter skipped (fomo not configured, fomo_users=0), new_tokens checked 7 / new 2 (kein Signalkandidat), resolve 0 (keine neuen Trader, letzter first_seen nach wie vor 22. Sep), track 25 Wallets / 0 trades / 0 errors / 426 RPC-Requests (volles Fenster, штатно), holdings 1095 pairs (953 held / 142 empty), deployers 3/1, crews 1 (2 Wallets), report ok. Quellen: RPC-Node gesund, `_too_big` griff nicht; trenches lebt; keine Gecko-429 im Pass. **Watcher-Fund: `cli watch` war KOMPLETT tot** - kein einziger fomo_agent.cli-Prozess (Session-44-Familie 47440/114068 weg, vermutlich mit der Konsole/Session gestorben; bursts-Gate dunkel, seit wann unklar, mind. seit der letzten Pruefung ~13:12). Neu gestartet: pid 62552 (`env -u PYTHONPATH PYTHONIOENCODING=utf-8 ./.venv/Scripts/python -m fomo_agent.cli watch`, persist_on_release), Log bestaetigt `watch: every 20s, burst at +1.0 from 3 wallets in 30 min` (Bar 1.0), tickt (tick 1, head 88632456), 0 Fehler; verifiziert: genau 1 Watcher. **Scoring-Queue: 125 Kontexte in pending_scores.json** (mtime 19:40; vorher 53) - Ursache ist Zeit, nicht Code: die 42 watch-Wallets kreuzten heute ~15:31 UTC das 72-h-Rescore-Fenster (letzter Verdict 11. Okt 15:31), dazu dropped-Alterungen ins 14-Tage-Fenster -> 126 faellig (3 tracking + 2 active + 42 watch + 79 dropped), 125 exportiert (1 nothing_to_judge, `_logjam`, по дизайну). Das ist der regulare Rescore-Lauf der Queue, kein Anomalie-Stau; er wartet auf Score im Chat (`score --export` -> Chat -> `score --import`). Fills 24 h: 84 (6 h: 32, letzter 19:00 UTC), bursts 24 h 0, pushes 24 h 0 - ruhige, aber lebende Laufbahn. Status unveraendert: 147 Trader (2 active / 42 watch / 15 idle / 3 tracking / 85 dropped), 0 neue Trader in 7 Tagen. Top active: game_for_one 78 (realized +$4,488, 3/3 closed wins), Cryptoaeon 30; Top watch: DipWheeler 65, RugDalio 65 (net +$319k), AvgJoesCrypto 60 (net +$16.1M), econoar 60. Keine Schluessel gedruckt.

**Session 43

**Session 44 (14. Okt, ~18:45 UTC): fomo-Discovery — Blockade exakt diagnostiziert (reine Konfig, kein Code-Fix); Enthlock wartet auf EINEN Browser-Export von Max.** Auftrag (rein diagnostisch, keine Live-Aenderung): `discover_leaderboard` seit Tagen skipped, fomo_users=0, 0 neue Trader seit 22. Sep. Kette: `.env` `FOMO_SESSION` leer (0 Zeichen) → `FomoClient.__init__` wirft `FomoNotConfigured` → `safe_fomo()`→None → run-Loop skippt sauber (runs 2133/2072/2018 `{"skipped":"fomo not configured"}`; run 2165 18:19 war ein einmaliger `cli discover --leaderboard`-Probe, der Fehler steht in `runs`). Zweite Schicht: selbst mit Session waere der HTTP-Weg tot — Cloudflare 430 am Edge (docs/fomo-endpoints.md, `FomoEdgeBlocked`); FOMO_SESSION ist deshalb voersaetzlich leer, einziger dokumentierter Weg ist der Browser-Export (`scripts/fomo_export.js` → `cli fomo-import`). `fomo_session_from_curl.py` ist hier KEIN Enthlock (1h-Token + 430 → nur Fehler-Spam in runs; bleibt Diagnose-Werkzeug). resolve-Step ist bereit und kostenlos (RobinhoodRPC; runs 2135/2074/2020 `attempted:0` weil fomo_users=0 — kein Input; neue Daten laufen sofort durch, sobald ein Export da ist). Freie Wege erschoepft: trenches lebt, aber statisch (147 seen / 0 new seit Tagen); CODEX-/FOMOAPI-/HELIUS-/ANTHROPIC-Keys alle leer in `.env` (Codex-Weg ohnehin nicht auf eigene Faust). Enthlock = Max-Eingriff einmalig: fomo.family im eigenen Browser eingeloggt → F12-Konsole → Inhalt von `scripts/fomo_export.js` einfuegen → Enter → Leaderboard-Tab anklicken → Autodownload `fomo_export_<ts>.json` → an Session uebergeben → `cli fomo-import <datei>` fuellt fomo_users+fomo_swaps, resolve (frei) macht daraus Trader. Keine Schluessel gedruckt. (14. Okt, ~13:15 UTC): voller `run --once` (runs 2132–2142, 13:02–13:12) — 0 Fehler; Discovery war 12,5 h alt, wieder frisch.** Eigener Lauf statt DB-only, weil die letzte volle Discovery 00:32 war (Discovery-Takt ~12 h); der 30-min-Loop schreibt nur track+enrich. Full pass: discover_trenches 147 seen / 0 new / 147 updated (lebt), fomo weiter skipped (fomo not configured), new_tokens checked 6 / new 5 (**SI** mcap 17.3M liq 205k, **Altai** 9.2M/299k, **Paper** 4.1M/1.3M, **FalconMargin** 2.5M/500k, **DKIT** 940k/133k — registriert, unter Signalfilter), resolve 0 (keine neuen Trader, letzter first_seen 22. Sep), track 25 Wallets / 0 trades / 0 errors / 426 RPC-Requests (volles Fenster, штатно), holdings 1069 pairs (927 held / 142 empty), deployers 3/1, crews 1 (2 Wallets), score 53 exportiert, report 3057 B. Quellen: RPC-Node gesund, `_too_big` griff nicht; trenches lebt; Gecko keine 429 im Pass. tracker 24 h: 49 runs, alle 0 errors; die einzigen 2 Fehler der 48 h sind die bekannten historischen (2064 PYTHONPATH-Importbruch 13. Okt 22:21, 2021 dead process — beide schon markiert); keine offenen runs. Watcher: genau 1 Familie (47440 Worker + 114068 Launcher-Stub, Start 09:40:57, 22 s CPU) — Session-42-Cleanup hält, kein Doppel-Scan. Fills 24 h: 85 (6 h: 20, letzter 12:41 UTC) — ruhige, aber lebende Laufbahn; bursts 24 h 0, pushes 24 h 0. Status unverändert: 147 Trader (2 active / 42 watch / 15 idle / 3 tracking / 85 dropped). Top active: game_for_one 78 (realized +$4,488, 3/3 closed wins), Cryptoaeon 30 (net −$25.1k unrealized, 5 open bags, open cost $49.7k); Top watch: DipWheeler 65 (realized −$2.3k, 3/11 wins, 91k foll), RugDalio 65 (net +$319k, 58 open bags), AvgJoesCrypto 60 (net +$16.1M, 239 open bags), econoar 60 (net +$2.26M). **Scoring-Queue: 53 Kontexte in pending_scores.json** (mtime 13:12, unverändert 53; 1 nothing_to_judge — `_logjam`, по дизайну), letzter Verdict 11. Okt 15:31 — warten auf Score im Chat. Keine Schlüssel gedruckt.

**Session 42 (14. Okt, 09:45 UTC): Watcher-Chaos bereinigt — genau 1 `cli watch` (Bar 1.0) läuft; PYTHONPATH-Kollision dauerhaft entschärft.** *Watcher:* alle 4 `cli watch`-Prozesse (92232/62296/24260/44512) waren noch am Leben (Session 41 hatte 62296/44512 fälschlich als weg gemeldet). Zwei Familien: 92232+62296 (Start 13.10 08:20:48, VOR der HOT_DELTA-Edit 09:36:50 → alter Bar 4.0) und 24260+44512 (Start 09:43:16, NACH der Edit → neuer Bar 1.0); je ein venv-Launcher-Stub (0 CPU) + ein Worker (62296 108 s, 44512 102 s CPU). Der korrekte Watcher ist die 09:43-Familie mit Bar 1.0. Beendet: 92232, 62296, 24260 (taskkill /F; 44512 fiel als Kind von 24260 mit — gleiche Konsole/Job). Danach genau 1 frischer `cli watch` gestartet (pid 102044, `env -u PYTHONPATH PYTHONIOENCODING=utf-8 ./.venv/Scripts/python -m fomo_agent.cli watch`), Log bestätigt `watch: every 20s, burst at +1.0 from 3 wallets in 30 min`, tickt (tick 1, head 88195208), 0 Fehler. Verifiziert: genau 1 python `cli watch` läuft (47440; 23048 ist die eigene Session-Bash, kein Watcher). bursts-Tabelle (0 Zeilen) füllt sich nur, wenn ein echter Cluster den Gate kreuzt (~1/Tag bei Bar 1.0) — der einzige Schreiber ist jetzt der eine gesunde Bar-1.0-Watcher; kein Row in dieser Session erzwingbar. *PYTHONPATH:* die Hermes-Session setzt PYTHONPATH auf eine cp314-pydantic_core-Umgebung, die Imports im cp313-venv bricht (track #2064, `ModuleNotFoundError: fomo_agent.pipeline.provenance`). Dauerhaft: Cron-Job `fomo-radar Loop` (0708b8f2725d) Prompt um die Regel erweitert — jeder CLI-Lauf mit `env -u PYTHONPATH`; Skill `fomo-robinhood-radar` Always-on-Regel ebenso. Kein Code-Fix nötig. Scoring-Queue weiter 53 (unverändert), letzter Verdict 11. Okt — warten auf Score im Chat. Keine Schlüssel gedruckt.

**Session 41 (14. Okt, 06:48 UTC): Loop lebt — kein zweiter `run --once`, DB-Inspektion genügt.** Live-Loop schreibt selbst (track+enrich alle ~29 min, 50 track-runs/24 h, letzter #2106 startete 06:46 — die laufende normale ~545-s-Passage, keine verwaisten offenen runs); letzte volle Discovery 00:32/00:41 (runs 2071–2081): discover_trenches 147 seen / 0 new / 147 updated (lebt), fomo weiter skipped (fomo not configured), new_tokens 2×/24 h; neu first_seen seit Session 40: WOJAK (mcap 3.37M), NET (959k), SI, GAEJUKI, HEY, TRIAN, PIDSER, BALL, SHROUD, FLEDGER plus die 5 aus dem 00:32-Pass (Altai 11.1M, IGNITION 10.9M, Paper 10.5M, NIBBLEMOCHI 1.7M, GMOTH 734k) — registriert, unter Signalfilter; resolve 0 (keine neuen Trader, letzter first_seen nach wie vor 22. Sep). track: 25 Wallets, 0 trades / 0 errors / 426 RPC-Requests (volles Fenster, штатно); die einzigen 2 Fehler der 24 h sind bekannt und historisch (#2021 interrupted, schon Session 38 markiert; #2064 transienter PYTHONPATH-Importbruch 22:21, Doku Session 40). RPC-Node gesund, `_too_big` griff nicht; enrich 47× ohne Fehler. Fills 24 h: 72 (6 h: 19, letzter 05:39 UTC) — ruhige, aber lebende Laufbahn; bursts 24 h: 0, pushes 24 h: 0. Status unverändert: 147 Trader (2 active / 42 watch / 15 idle / 3 tracking / 85 dropped). Top active: game_for_one 78 (realized +$4,488, 3/3 closed wins, 23.5k followers), Cryptoaeon 30 (net −$25.1k, 5 offene Bags, open cost $49.7k); Top watch: DipWheeler 65 (realized −$2.3k, 91k foll), RugDalio 65 (net +$319k), AvgJoesCrypto 60 (net +$16.1M, 105k foll). **Scoring-Queue: 53 Kontexte in pending_scores.json** (mtime 00:41, unverändert 53), letzter Verdict 11. Okt 15:31 — warten auf Score im Chat. **Watcher-Entscheidung (Session 38/39) weiter offen: von den 4 `cli watch` laufen nur noch 2 (92232, 24260 — die als Zombies markierten; 62296, 44512 sind weg).** Nächste Schritte: Watch-Prozesse bereinigen (Max), danach pending_scores.json durchscoren/importieren. Keine Schlüssel gedruckt.

**Session 40 (14. Okt, 00:41 UTC): voller `run --once` (runs 2071–2081) — 0 Fehler; Discovery war 12,5 h alt, jetzt wieder frisch.** Live-Loop schreibt selbst (radar-sammler-Cron, track+enrich alle ~20–30 min, letzter 2082 00:41, keine offenen runs). Voller Durchlauf: discover_trenches 147 seen / 0 new / 147 updated (lebt), fomo weiter skipped (`discover_leaderboard` {}, fomo not configured), new_tokens checked 5 / new 5 (Altai, IGNITION, Paper, NIBBLEMOCHI, GMOTH, alle 00:32), resolve 0 (keine neuen Trader), track 25 Wallets / 0 trades / 0 errors / 426 RPC-Requests (volles Fenster, `_too_big` griff nicht), holdings 1051 pairs (911 held / 140 empty), deployers 2, crews 1 (2 Wallets). RPC-Node gesund; Gecko 429 auf enrich — fail-soft, штатно. Fills 24 h: 72 (6 h: 12, seit UTC-Mitternacht 0) — ruhige, aber lebende Laufbahn. Status: 147 Trader (2 active / 42 watch / 15 idle / 3 tracking / 85 dropped), 0 neue Trader seit 7 Tagen (letzter first_seen 22. Sep). Top active: game_for_one 78 (realized +$10.2k, 138 trades, 4/7 closed wins, best +$6729), Cryptoaeon 30 (positive net flow, 5 open bags); Top watch: DipWheeler 65, RugDalio 65, AvgJoesCrypto 60. **Scoring-Queue: 53 Kontexte in pending_scores.json** (mtime 14. Okt 02:41, +1 seit Session 39; 1 nothing_to_judge — `_logjam`, по дизайну), letzter Verdict 11. Okt 15:31 — warten auf Score im Chat. **Watcher-Entscheidung (aus Session 38/39) weiter offen: alle 4 `cli watch` laufen noch** (92232/62296/24260/44512), bursts weiter 0 Zeilen. **Umgebungs-Hinweis:** die Hermes-Session setzt PYTHONPATH auf eine cp314-pydantic_core-Umgebung — bricht Imports in diesem cp313-venv (erklärt den transienten track-Fehler #2064 22:21, `ModuleNotFoundError: fomo_agent.pipeline.provenance`); CLI-Läufe brauchen `env -u PYTHONPATH`. Nächste Schritte: Watch-Prozesse bereinigen (Max), danach pending_scores.json durchscoren/importieren. Keine Schlüssel gedruckt.

**Сессия 39 (13 окт, 18:17 UTC): живой цикл grün — 44 track-раны / 24 ч, 0 errors; 4 watch-Prozesse laufen immer noch (Entscheidung an Max).** Kein zweiter `run --once` — der lokale Loop schreibt selbst (track+enrich alle ~25–30 min, letzter 2046/2047 18:02–18:03 UTC, keine offenen runs). track: 25 Wallets, 0 trades / 0 errors / 70 RPC-Requests (inkrementell), volle Fenster 426 Requests штатно, `_too_big` hat nicht gegriffen; einziger Fehler der letzten 24 h ist der bekannte track #2021 (11:50, `interrupted (dead process)`, bereits Session 38 markiert). Discovery alle ~12 h (letzter 11:50, nächster ~23:50): trenches 147 seen / 0 new / 147 updated (lebt); fomo weiter skipped (`discover_leaderboard` {}, fomo_users=0); Codex wurde nicht verbraucht; 23 Token first_seen in 24 h (letzter 18:13). Fills 24 h: 91 (6 h: 35, letzter 18:15) — ruhigere, aber lebende Laufbahn. Status: 147 Trader (2 active / 42 watch / 15 idle / 3 tracking / 85 dropped), 0 neue Trader seit 7 Tagen (letzter first_seen 22. Sep). Top active: game_for_one 78 (realized +$4,488, win 3/3, 23.5k foll), Cryptoaeon 30 (net −$25.7k, open $49.7k); Top watch: DipWheeler 65 (realized −$1.5k, 91k foll), RugDalio 65 (net +$270k), AvgJoesCrypto 60 (net +$16.0M, 105k foll), neu dabei econoar/cosby/lordarbiter 60. **Watcher-Entscheidung (aus Session 38) weiter offen: alle 4 `cli watch` laufen noch** — 92232+62296 (Start 08:20:49, alter Bar HOT_DELTA 4.0) und 24260+44512 (Start 09:43:17, neuer Bar 1.0); 92232/24260 0 CPU-Sekunden (Zombies), 62296/44512 ziehen CPU → 2–4× RPC-Scan aktiv, `bursts` unverändert 0 Zeilen. Scoring-Queue: 52 Kontexte in pending_scores.json (mtime 12. Okt 11:42, unverändert), letzter Verdict 11. Okt 15:31 — warten auf Score im Chat. Nächste Schritte: Watch-Prozesse bereinigen (Max), danach pending_scores.json durchscoren/importieren. Keine Schlüssel gedruckt.

**Сессия 38 (13 окт, 11:50 UTC): полный проход до track — 0 ошибок; НАЙДЕНО: 4 параллельных `cli watch` (2 со старым баром 4.0, 2 с новым 1.0), bursts с 11 окт так и 0 строк.** Прогнал `run --once` (runs 2017–2021): discover_trenches 147 seen / 0 new / 147 updated (trenches жив), fomo по-прежнему skipped (fomo_users=0), new_tokens checked 7 / new 3 (**SFFINU** mcap 2.77M liq 570k, **Paper** новый пул 1.99M/246k — тот же символ, другой минт, не вчерашний 10.4M, **LUCKYKEY** 1.07M/93k), resolve 0 (новых трейдеров нет), track #2021 стартовал, но харнесс убил процесс по таймауту — помечен `interrupted (dead process)`; сам трекинг делает 25-мин цикл (следующий ~12:10), потерь нет. Остальной конвейер жив: track+enrich каждые ~25–30 мин, 103 track-рана за 48 ч, 0 ошибок всех видов; RPC-нода здорова (`_too_big` не срабатывал, полные окна 426 запросов штатно). **Финдинг — 4 процесса `cli watch` параллельно:** 92232+62296 (старт 08:20:49, ДО правки .env 09:36:50 → держат старый бар HOT_DELTA 4.0; 62296 — тот, что сессия 37 уже велела убить вручную) и 24260+44512 (старт 09:43:17, после правки → новый бар 1.0); при этом 92232 и 24260 не расходуют CPU с момента старта (0 с — зомби), а «новый watcher» сессии 37 (pid 88992) — bash-обёртка, python-потомка от неё нет. Итог: 2–4× RPC-скан и до 4 оценок burst на тик, при этом `bursts` с 12 окт 18:57 всё ещё 0 строк (при баре 1.0 за ~10 ч ожидание по бэктесту ~0.4 пересечения — 0 совместимо, но пара зомби часть тиков не считает). Решение на Максе: убить 3 из 4 (оставить один, стартованный после 09:36:50), иначе четверной RPC-скан остаётся. Дубль-факт: 2 процесса `cli track` стартовали в одну секунду (11:40:07) — второй следов в runs не оставил (дубль-запуск харнесса). База: 147 трейдеров (2 active / 42 watch / 15 idle / 3 tracking / 85 dropped), новых за 7 дней 0; trades 24h — 130; топ active: game_for_one 78 (realized +$4,488, win 100%, 23.5k foll), Cryptoaeon 30 (net −$21.7k, open $49.7k); топ watch: DipWheeler 65 (realized −$1.2k, 91k foll), RugDalio 65 (net +$220.9k), AvgJoesCrypto 60 (net +$16.0M, 105k foll); bruisedwm tracking score 5, 62.3k foll, open $4.2k. Очередь скоринга: 52 контекста в pending_scores.json без изменений (mtime 12 окт 13:42), последний вердикт 11 окт 15:31. Новые токены 24 ч: 22 first_seen (IMD6900 23.6M, Hound 14.7M, WISP 13.3M из прохода 23:28 + 3 из моего). Ключи не печатались.

Обновлено: 2026-10-13 (сессия 37).

**Сессия 37 (13 окт): Burst-гейт опущен — HOT_DELTA 4.0 → 1.0; реальные кластеры (YIELD/LUCIA) снова проходят; TRUSTED оставлен 60; копи-фид из report-сигналов только помечен.** Решение Макса по анализу сессии 36: бар опущен с 4.0 до 1.0 (config.py default + `.env` + `.env.example` синхронно; старый бар: HOT_DELTA=4.0 за 30 мин от 3 кошельков, TRUSTED=60). Почему 1.0: это вся «линия доверия» с часами — три кошелька на 60 дают 3×(0.6)²=1.08, — и при нём YIELD (3 trusted first-buyers: AvgJoesCrypto 60, econoar 60, RugDalio 65, conv 1.14) и LUCIA (5, conv 1.86, первое пересечение 1.08) — настоящие лаунч-бёрсты одной VIP-когорты — оба проходят; при любом баре ≥2.0 на живой ленте гейт не сработал ни разу (0 пересечений). Промер на локальной ленте (20.5 дней, 4875 филлов, скоры current, `cli hot --backtest`): delta 1.0/30 мин/3 кошелька — 19 пересечений (~0.93/день) на кластерах AvgJoes/econoar/RugDalio/soby0x/cosby/lordarbiter (YIELD ×2, LUCIA, FREELUCIA, OML, SLUICE, AG ×2, FURN ×2, PAPER ×2, GENIE, SS, YAMATA, FRIES, SLATE, LOAN, BEEZIE), 61% дошли до 2× за сутки, медиана лучшей цены 2.88×; при delta 1.5 — 7, при ≥2.0 — 0. Остальные гейты пуша нетронуты (span ≥180 с, sells ≤50%, crews ≥2, liq ≥$10k, cohort 3–90%, namesake ×1.5). TRUSTED оставлен 60 намеренно: это линия доверия всех лент (signals/fresh/exits) и всего провенанса; снижение до 45 зачислило бы в trusted unipcs и других целей сеятеля по всему продукту — решение зафиксировано, развести можно отдельно. Watcher перезапущен с новым баром (pid 88992, `watch: every 20s, burst at +1.0 from 3 wallets in 30 min`; старый watcher сессии 36, pid 62296, держит бар 4.0 и остался висеть — остановить нельзя без /F, нужен ручной kill, иначе двойной RPC-скан). Альтернатива из сессии 36 — брать report-сигналы (≥2 watch-покупателей) как копи-фид — **только помечена**, не реализована: у report-правила 3 ложные тревоги против 2 кластеров (CloudPad 12 окт: 4 покупки за 12 ч, mcap $6k), а burst-гейт с пониженным баром отвечает на ту же потребность, не выключая кластерные проверки. Ключи не печатались.

**Сессия 36 (13 окт, 08:20 UTC): Burst-Gate gestartet — bursts/pushes waren leer, weil `cli watch` in keinem Loop steckt.** Ursache: «watcher» (cron `fomo-radar Loop`, каждые 6 ч `run --once`) + 25-мин track-loop (отдельный процесс) делают track/enrich, но никогда `watch`; единственный писатель `bursts` (record) и `pushes` (только когда ≥1 чат реально оповещён) — это `watch.run`. Запущен `cli watch` как постоянный фоновый процесс против O: (pid 112324, тик 20 с, head 87297958, 0 ошибок) — `bursts` теперь наполняется вживую; `pushes` локально останется 0, пока нет активного подписчика (сейчас 0; это леджер отправленных сообщений, по дизайну). Ручной путь: `cli watch` (петля) / `cli watch --once` (тик); `cli hot --backtest` только меряет, не пишет. **YIELD/LUCIA НЕ проходят burst-гейт** (HOT_DELTA 4.0, TRUSTED 60): YIELD 3 trusted first-buyers (AvgJoesCrypto 60, econoar 60, RugDalio 65), max conv 1.14; LUCIA 5 (soby0x/cosby/AvgJoes/econoar 60, RugDalio 65), max conv 1.86. Остальные покупатели (unipcs 45, PoorGoat_ 50, change 55, 0xAvast 55, frankdegods 50) — <60, в гейте не считаются. Оба пришли только из report-правила (≥2 watch-покупателя), не из гейта. Копи-кандидаты: решение — либо снизить бар (HOT_DELTA/TRUSTED), либо брать report-сигналы как копи-фид. Ключи не печатались.

**Сессия 35 (13 окт, 05:40 UTC): живой цикл пишет базу сам — 0 ошибок за 24 ч; очередь скоринга 52 без изменений; старый зависший track #1802 помечен мёртвым.** Второй `run --once` не гонял: локальный watcher/цикл выполняет track+enrich каждые ~25 мин (последние 1989/1990, 05:07–05:16 UTC, 1991 ещё идёт), за сутки 0 ошибок во всех видах. Зависший track #1802 (10-11 16:52, `finished_at` NULL) — единственный устаревший, помечен `interrupted (dead process)` (проверено: живой #1991 не тронут). Track: 25 кошельков, 0 trades / 0 errors / 426 RPC-запросов (полное окно 5.6 ч, штатно; инкрементальные проходы 19–70 запросов с 1–5 trades). RPC-нода здорова, `_too_big` не срабатывал; trenches на последнем полном проходе (23:28) 147 seen / 0 new / 147 updated; fomo по-прежнему не сконфигурирован (`discover_leaderboard` skipped «fomo not configured», fomo_users=0), Codex не тратился; Gecko-429 на enrich — fail-soft, штатно. Активность 24 ч: 130 филлов (24 с полуночи UTC), топ-токены FREELUCIA 27, PONS 23, YIELD 20 (сигнал сессии 34 торгуется дальше), TORCH 15, BONER 8; самые активные кошельки cosby 38 филлов (16 buys/22 sells), unipcs 12 buys, bruisedwm 9 (tracking, набирает). Новых трейдеров 0 за 7 дней; ночью 1 токен first_seen (SYNCat, mcap 29.8k — под фильтром, не сигнал). Статусы: 2 active, 42 watch, 15 idle, 3 tracking, 85 dropped (всего 147). Топ active: game_for_one score 78, realized +$4,488, win 100%, 23.5k followers; Cryptoaeon 30, net −$21.7k (open cost $49.7k). Топ watch: DipWheeler 65 (realized −$1.2k, 91k foll), RugDalio 65, AvgJoesCrypto 60 (105k foll). **Скоринг-очередь: 52 контекста в `pending_scores.json` без изменений** (mtime 12 окт 13:42, все адреса целы 0x…42 — испорченный черновик сессии 34 не записан), последний записанный вердикт 11 окт 15:31 — ждут `score --import` после оценки в чате.

**Сессия 34 (13 окт, 02:15 UTC): скоринг-прогон 52 НЕ дошёл до БД; разбор трёх сигналов отчёта (YIELD/LUCIA/CloudPad).** Проверка сессии 20261012_183845_28db6e (12 окт 18:39 UTC): вердикты по всем 52 кошелькам из pending_scores.json составлены в сессии (1 active/36 watch/15 dropped; переходы: 11 watch→dropped, 6 dropped→watch, Cryptoaeon active→dropped, techquant tracking→dropped), но файл не записан — write-guard Hermes отказал (репо на O: вне HERMES_WRITE_SAFE_ROOT C:\Users...), затем сессия оборвалась (network stall), `score --import` не выполнялся. Дополнительно: 51/52 адресов черновика испорчены (обрезаны до 10 симв. + padding e0…), у 2 строк red_flags ['distributing'] вне enum (bot|bundler|insider-like|wash|one-hit) — импорт всё равно бы отверг файл. БД нетронута: active=2, watch=42, dropped=85, idle=15, tracking=3; score_history последняя запись 11 окт; pending_scores.json без изменений (mtime 12 окт 13:42). На человеке: пере-скор заново или реконструкция черновика (адреса по префиксу 10 симв. восстанавливаются); 5 «триллионных» артефактов (unipcs/Salem1299534/ogle/notanicecat69/DumbCrayonEater) в черновике dropped по указанию Макса — но dropped снимает их с трекинга, а это ядро покупателей бёрстов (unipcs купил все три токена ниже). Сигналы 12 окт (11:10 UTC): **YIELD** (0xf6a894…, 25 кошельков/5.38 SOL) и **LUCIA** (0xb09b16…, 23/5.43 SOL) — настоящие лаунч-бёрсты одной VIP-когорты: первый вход 77 с / 150 с после создания пула, вся когорта за 22.6 / 18.9 мин, медианный шаг между покупками 8 / 10 с, ни одной покупки в ту же секунду (не сид, почти все kind=trade; 2 dust), продаж когорты ноль; цена входа min/med/max 5.1e-5/1.6e-4/4.0e-4 и 7.1e-5/2.5e-4/6.9e-4, сейчас 2.5x / 3.7x от медианы входа, mcap 405k/935k, liq 36k/59k, пулы торгуются (598/596 и 875/840 за сутки). Покупатели — watch-инфлюенсеры (unipcs 514k foll, PoorGoat_ 499k, change 338k, 0xAvast 277k, frankdegods 244k, AvgJoesCrypto 105k), ни одного active (game_for_one/Cryptoaeon nicht dabei); пересечение YIELD∩LUCIA 18 из 25/23. **CloudPad** (0xf9c0b8…, 4/0.00 SOL) — ложная тревога правила SIGNAL (≥2 watch-покупателей): 4 покупки $70–200 за 12 ч, первый вход 4 ч после запуска, mcap $6k, цена 1.1x, никакого кластера. bursts/pushes пусты (0 строк): локальный watcher работает только с 18:57 UTC 12 окт, события 11 окт им не оценивались — SIGNAL-метка в отчёте это фильтр отчёта, не burst-гейт. Ключи не печатались.

**Сессия 33 (13 окт, 01:30 UTC): локальный цикл встал в 18:57 UTC, прогнал полный `run --once` — 0 ошибок.** Watcher/цикл (track+enrich каждые ~25 мин) молчал с 18:57 (последний #1952), процесса нет — вместо чтения БД прогнал полный проход (runs 1954–1962, 23:28–23:30 UTC): trenches 147 seen / 0 new / 147 updated, fomo по-прежнему не сконфигурирован (skipped), new_tokens checked 10 / new 9 (IMD6900 mcap 23.6M liq 480k, Hound 14.7M/190k, WISP 13.3M/360k, Paper 10.4M/242k, NOCKAI 6.6M/255k, casino 5.6M/233k, TFDCAT 2.9M/278k, CBARA 2.0M/201k, 3RDI 964k/47k), resolve 0, track 25 Wallets / 6 trades / 0 errors / 20 RPC-запросов (окно 18:57–23:28; свежие филлы: bruisedwm набирает VERDEX/SECTORAL/RAIL, bluntz_capital продал PONS $59k), holdings 1034 пар (902 held, 132 empty), deployers 2, crews 0. RPC-нода здорова, `_too_big` не срабатывал; Gecko 429 на enrich (backoff, fail-soft, штатно). Новых трейдеров 0 за 7 дней; статусы: 2 active, 42 watch, 15 idle, 3 tracking (bruisedwm/techquant/_logjam; idle 16→15 — один вернулся в tracking по филлу), 85 dropped (всего 147). Топ active: game_for_one score 78, realized +$4,488, win 100%, 23.5k followers; Cryptoaeon 30, net −$21.7k. Топ watch: DipWheeler 65, RugDalio 65, AvgJoesCrypto 60. **Скоринг-очередь: 52 контекста в `pending_scores.json`** (без изменений; 1 без скора — `_logjam`, по дизайну) — ждут `score --import` после оценки в чате.


**Сессия 32 (12 окт, 17:30 UTC): живой цикл пишет базу сам, второй `run --once` не гонял.** Вместо полного прохода — чтение БД: локальный watcher/цикл выполняет track+enrich каждые ~25 мин (последний 1944/1945, 17:13 UTC), плюс полный проход в 11:00 и 22:00 UTC. За сутки 0 ошибок во всех видах. track: 25 кошельков, 2 trades / 0 errors / 19 RPC-запросов (17:13; проходы с полным окном — 426 запросов, штатно), 30 trades в 16:26. RPC-нода здорова, `_too_big` не срабатывал; fomo по-прежнему не сконфигурирован (`discover_leaderboard` skipped), Codex/Helius без ключей — не блокеры. Новых трейдеров 0 за 7 дней; статусы без изменений: 2 active, 42 watch, 16 idle, 2 tracking, 85 dropped (всего 147). Токены сегодня: 12 first_seen (SLIPPY mcap 1.16M liq 240k, FREELUCIA 830k/82k, YIELD, HOOKSWAP, microclaus, SOVR, SLVN, ZORN, CRVO + 4 из 11:00-прохода CLAUDIA/BTIGR/PDCAP/EQVTA). Топ active: game_for_one score 78, realized +$4,488, win 100%, 23.5k followers; Cryptoaeon 30, net −$18.1k. Топ watch: DipWheeler 65 (+$481 realized, 91k followers), RugDalio 65, AvgJoesCrypto 60. **Скоринг-очередь: 52 контекста в `pending_scores.json`** (без изменений; 1 без скора — `_logjam`, по дизайну) — ждут `score --import` после оценки в чате.

**Сессия 31 (12 окт, 11:00 UTC): чистый дневной проход, 0 ошибок; очередь скоринга выросла до 52.** Полный `run --once` (runs 1907–1917, 11:00–11:10 UTC): trenches discovery 147 seen / 0 new / 147 updated, new_tokens checked=6 new=4 (CLAUDIA mcap 13.2M liq 365k, BTIGR 2.1M / 210k, PDCAP 2.0M / 235k, EQVTA 823k / 126k — все созд. 02:16–08:20 UTC), resolve 0 (новых трейдеров нет), track 25 Wallets / 0 trades / 0 errors / 426 RPC-запросов (rate-limit штатно, окно 5.7h, 50 transfers), holdings 988 пар (858 held, 130 empty), crews 0, deployers 0, pushes 0. RPC-нода здорова; fomo по-прежнему не сконфигурирован (FOMO_SESSION пустая, `discover_leaderboard` skipped, fomo_users=0), Codex/Helius без ключей — не блокеры, все 147 трейдеров из trenches. **Скоринг-очередь: 52 контекста в `pending_scores.json`** (scorer=manual, было 51; 1 nothing_to_judge — `_logjam`, по дизайну) — ждут `score --import` после оценки в чате. Статусы: 2 active, 42 watch, 16 idle, 2 tracking, 85 dropped (всего 147). Топ active: game_for_one score 78, realized +$4,488, win 100%, 23.5k followers; Cryptoaeon 30, net −$18.1k. Топ watch: DipWheeler 65, RugDalio 65, AvgJoesCrypto 60.

**Сессия 30 (12 окт): чистый ночной проход, 0 ошибок; 51 кошелёк ждут скоринга.** Полный `run --once` (runs 1844–1854, 00:44–00:54 UTC): trenches discovery 147 seen / 0 new / 147 updated, track 25 Wallets / 0 trades / 0 errors / 426 RPC-запросов (все через RobinhoodRPC), holdings 984 пар (855 held, 129 empty), crews 0. RPC-нода здорова (rate-limit штатно, отказ «30000 blocks a call» распознан `_too_big`, окно разбито — 0 ошибок). fomo.family по-прежнему стоит (FOMO_SESSION пустая, fomo_users=0), Codex/Helius без ключей — не блокеры, все 147 трейдеров из trenches. Новые токены: FUNPANDA (mcap 5.1M), RBCAT (1.6M), vti, RDDT, AMZN. **Скоринг-очередь: 51 контекст в `pending_scores.json`** (scorer=manual) — ждут `score --import` после оценки в чате. Статусы: 2 active (game_for_one 78, Cryptoaeon 30), 42 watch, 16 idle, 2 tracking, 85 dropped. Новых трейдеров за 24ч нет. 312 тестов зелёные (не гонял, без изменений кода).

**Сессия 29 (11 окт): score-люк закрыт; статус `idle` построен по решению автора.** Сначала (утро) — фильтр: `export_contexts` (score.py:323) судил только по филлам нашей ленты и книге fomo, а trenches-профиль с реальными числами (`followers` 15k–121k, `net_pnl`, open bags) уже ложился в `indexer_stats` и игнорировался. Фильтр открыт на третье свидетельство — `indexer_stats` с ненулевыми числами или followers (пустой `{}` и all-zeros остаются «ничем»); тест и комментарий зафиксировали правило. Прогнал `score --export --unscored` → **24 из 25 экспортированы** (`_logjam` остался: все нули, по дизайну), два сабагента (`deleg_07713107`, deepseek-v4-flash по 12 кошельков, каждый читал instructions/schema из файла) → 24 вердикта, `score --import` **0 invalid/unknown**: 23 dropped, 1 watch (KienNguyen_NFT, 42, +37% на $15 cost), 311 тестов. **Затем автор решил: «never traded on Robinhood» — не dropped, а наблюдать без вердикта.** Построен статус `idle`: (1) `score.idle_when(ctx)` — три признака того, что судить есть о чём: филлы нашей ленты, книга fomo, `indexer_stats.open_cost` (за что-то платили). Нет ни одного — только followers → `apply_score` превращает dropped в `idle`, summary дописывает «Observed, not judged…». (2) `track.py` TRACKED += idle — такие продолжают сканироваться, и первый же филл (`track_wallet`) возвращает их в `tracking` → снова в очередь скоринга. (3) Из экспорта-очереди они исключены самим `pending_for_scoring` (idle там не запрашивается). (4) Косметика: `db.STATUSES`, mark ◷ и label IDLE в боте, `idle` в `/api/leaderboard` (pattern), `/api/health` counts, `site/src/lib/api.ts` (Stats, verdictClass), `leaderboard.astro` (valid), `cli.chain_counts` (Codex-прогноз считает и idle). (5) Миграция: 17 из 23 сегодняшних dropped — follower-only → `idle` (включая их строки score_history, чтобы сводки не считали их dropped); 6 с `open_cost` (реально платившие, −84…−99% unrealized) остались dropped по делу: им есть за что судить. **Заодно:** 10 зависших runs (7 track 05:00–10:55, 1777, 2 enrich_tokens 4–5 дней) помечены `finished_at` + `error='interrupted (dead process…)'` — не блокировали ничего. Итог: queue 1 (`_logjam`), 17 idle наблюдаются, 312 тестов зелёные (311 + idle-тест).

**Сессия 28 (11 окт): score-люк для 26 новых трейдеров не закрылся — экспорт их отказывает по дизайну.** Прогнал локальный путь `fomo_lokal.py` (Ollama, `qwen3.5:9b`; дефолт `qwen35-8k` в скрипте не установлен) против 25 трейдеров в статусе `tracking`. `score --export` вернул `exported: 0, nothing_to_judge: 25`: у всех 25 ноль филлов на ленте, ноль PnL fomo, ноль `fomo_user_id`/`open_positions` — только `followers` из trenches. `export_contexts` (score.py:323) режет такие контексты намеренно («a verdict on nothing is worse than a queue»), и `--force` это не обходит. 26-й (Cryptoaeon) уже проскорен пробой сегодня (score 30, active, `ollama-gemma-e4b-8k-64k`). Итог: 0 новых вердиктов, 25 всё ещё без балла. **Решение на человеке:** либо оставить их в очереди, пока не наторгуют (текущий дизайн), либо форсить вердикт по пустому контексту (против правила score.py). **Сборщик в момент прогона работал** (`radar-sammeln.py` → `fomo_agent.cli track`, run #1771, старт 13:01:23), но БД в WAL, мои запросы read-only — блокировки не было. **Зависший track-прогон (545 с) замечен:** все завершённые track-раны сегодня идут ровно 544–547 с (это нормальная длительность прохода, не зависание), но 7 track-ранов с утра (05:00–10:55) висят с `finished_at IS NULL` — не закрылись. 310 тестов зелёные.

**Сессия 27 (30 сен): локальный квикстарт и новый потолок ноды.** Исходный ТЗ: `C:\Users\Honor\Downloads\fomo-agent-claude-code-prompt_1.md` (фазы 0–5). Этот файл — единственный источник правды о том, что сделано и что дальше. Обновляй его в конце каждой сессии.

**Сессия 27 (30 сен): локальный квикстарт и новый потолок ноды.** Прогнал README-квикстарт на этой машине (`pip install -e .` → `.env` → `init` → `discover --trenches` → `track` → `score --export` → `serve`; `bot` ждёт `TELEGRAM_BOT_TOKEN`). **Нода сменила потолок:** `eth_getLogs` теперь отказывает диапазон длиннее 30 000 блоков текстом «narrow the block range» (раньше резала по 10 000 логов в ответе, и 200k-окно проходило целиком). `_too_big` не узнавал сообщение — весь проход трекинга падал (`errors: 25`). В `rpc.py`: детект новых фраз + разбор «only N are allowed» (`_named_cap`), шаг = N, но не шире половинного спана, чтобы отказ всегда сужал диапазон. После правки: track 25 кошельков, 12 филлов, 0 ошибок, 20 запросов. **Тест про инвайты падал на пустом `.env`:** `pro.enabled()` требует `pro_token`, который фолбэчится на `PUBLIC_TOKEN_CA`; оба пусты в свежем `.env`, тест ставил только цену. `tests/test_wave2.py` теперь сам ставит `pro_token` — тест не зависит от .env сервера. `score --export` → 113 кошельков проскорены и импортированы (`--import`, модель `manual:deepseek-v4-flash`): 1 active, 41 watch, 71 dropped, 0 invalid. **Delegation в Hermes-конфиге был сломан:** `delegation.model: Ollama/gemma4` через omniroute 401 (нет креды), локальный Ollama не поднят — все сабагенты падали. Переведён на рабочий провайдер (`hermes config set delegation.model deepseek/deepseek-v4-flash-0731` + `provider nous`), теперь постоянно. 310 тестов зелёные. Мелочь: в корне лежит неиспользуемый `.env.template` (копия `.env.example`?), стоит удалить.


**Сессия 22 (18 сен): волны — сеятель пойман по форме, не по размеру.** Вечером 17 сен
четыре токена (CSHIB, NCAT, DROCK, PXPND) получили по одной покупке в 13 топовых кошельков
(unipcs, Salem, DumbCrayonEater, picadura, Rowdy, 0xAvast, Aurelius, AvgJoes…) в одном порядке, с
шагом 6 с, внутри двух минут от первого филла: по $30 на первых двух, $32–$94 и $32–$299 дальше.
Через вход fomo, из казначейства fomo, получатель в calldata там же, где у настоящей покупки —
receipt не отличает (проверено: entrypoint, relayer, события, UserOperation — всё одно). $30 выше
dust-порога у 8 из 13, и на каждый ушёл burst (359–415 чатов), потом launch. **Сделано:**
`provenance.waves` — ≥5 trusted-кошельков, у которых единственная покупка токена легла в очередь
без разрыва > 45 с и ни одна не больше $500 → kind=`seed`, токен уходит из всех лент по правилу
seeded (`SEED_WAVE_*`). Реплей за неделю: те четыре + FLAI, PAIDCAT, CLANKER, PONSWAP, OPAIRH,
MUSE 0x0e74, MUSEB, TINU, Robinshib (13), **ни одного настоящего бёрста**. Плюс: burst требует
разбег ≥180 с между первым и последним входом (`HOT_MIN_SPAN_S`; настоящие 312+ с, сеяные 90–122);
продажи ≥50% от покупок окна — распределение, не вход (`HOT_MAX_SELL_RATIO`); токен моложе 30 мин
пушится, только если пул показывает продажу или покупателя сверх наших (`safety.only_the_cohort`,
`HOT_YOUNG_S`); launch с именем, пушенным за сутки, — клон, не пушится, burst на клоне — 1.5×
conviction (`TELEGRAM_CLONE_HOURS`). Сайт: `seeded` на филле и волна в плашке токена. По сводке
18 сен: daily_report — вердикты `dead` (пул не торговался) и `seeded`, блок `WAVES_24H`,
`vol_since`; health «scoring queue» считает то, что экспорт возьмёт; цены переспрашиваются у
токенов с покупкой за 7 дней/балансом/открытой позицией (`PRICE_REFRESH_DAYS`, было 6 300
токенов и 786 429-х в день), unsellable — раз в сутки; holdings сохраняет прочитанное до отказа
ноды; `API_WORKERS=3` (status-0 в час пушей); задача сводки — датированный results-файл и `&&`.
Trenches переехал на rhtrenches.com (301, клиент теперь идёт за редиректом; 147 кошельков);
`traders.pnl_*` теперь зеркалят борд fomo на каждом проходе (были двухнедельной давности у 178 из
501). X: @FomoBrainRH, первый пост — борд дня (`assets/cases/day-2026-09-17`,
`scripts/render_board.py`), пост+ответ по CPU ушли; watcher должен перезапускаться при смене
`X_ENABLED` (очередь пишет он). **Не сделано / на человеке:** FOMO_SESSION пустая — discovery по
fomo.family стоит, нужен перелогин (`scripts/fomo_session_from_curl.py`); анонс окончания grace
20 сен; ротация fomoapi-ключа.

**Сессия 22, продолжение (18 сен): три волны продукта.** *Волна 1:* `links.py` / `site/src/lib/links.ts` —
каждая ссылка на fomo.family с рефкодом (`FOMO_REF_CODE`, `FOMO_REF_PARAM`, `FOMO_REF_URL`; код ещё не
задан), «buy on fomo» первым в каждом пуше, кнопка на токене, профиль у трейдера, футер, блок бота,
`links` в `/api/token`. `pipeline/record.py` + `/record` и `/paper` (сайт, бот, `/api/record`): все
алерты с 11 сен (леджер добит `scripts/backfill_pushes.py` теми же свечами): 70 из 84 выше входа
(83%), 23 до ×2, медиана ×1.50; paper $100 в каждый алерт по входу, выход по часовому чтению
(первая цифра +$2,807 была артефактом — см. ниже, честная −$598). `pipeline/follows.py` — `/follow <handle>`: все филлы
кошелька через тик (free 3 / PRO 50 / 30 в час, только настоящие филлы). `pipeline/board.py` +
`assets/boards/day.html` — борд дня из леджера, рендер playwright на сервере
(`/opt/fomoradar/pw`, `BOARD_DIR=/opt/fomoradar/boards`), `radar-board.timer` 07:05 UTC ежедневно и
недельный по понедельникам 07:20; `fomo-radar board [--hours 168] [--post]`. *Волна 2:*
`pipeline/webhooks.py` — `/webhook <https url>` для PRO-ключа: burst/launch/followup POST-ом с
`X-Radar-Signature` (HMAC ключом), в потоке, выкл после 20 отказов; `pipeline/referrals.py` —
`/invite`, неделя PRO обоим, до 10 в месяц; `pipeline/prefs.py` — `/alerts`, `/minconv`, `/quiet`,
`/settings` (порог conviction теперь свой у чата, NULL пока не задан — раньше копировался и не
читался); `pipeline/cards.py` + `assets/boards/card.html` — карточка 1200×675 при пике ≥ ×2: в чаты
фото с follow-up-подписью, в X отдельным постом, в Discord; `pipeline/discord.py` —
`DISCORD_WEBHOOK_URL` зеркалит алерты/follow-up/карточки (нужен вебхук канала от автора).
*Волна 3:* `pipeline/deployers.py` — создатель токена с чейна (mint = первый Transfer с нуля;
прямой деплой → отправитель, через фабрику → первый не-контрактный получатель после сжигания;
fomo-кошельки — EOA с делегацией EIP-7702, 23 байта кода), репутация: молодой токен не пушится,
если у создателя за неделю уже есть seeded/unsellable/dead (`DEPLOYER_MAX_BAD=1`); NCAT и CSHIB —
один ключ `0x16a858…`, TINU и MUSEB — `0x595a2c…`. `pipeline/crews.py` — кошельки, покупающие
одни токены в одну минуту (≥4 общих за неделю, ≥50% меньшего), одна команда = одно мнение,
бёрсту нужно ≥2 (`HOT_MIN_CREWS`); на проде команда unipcs+DumbCrayonEater+frankdegods — это
«VIP-цели» сеятеля ($199–$304 за 1–3 мин до очереди по $30), окно пометки волн расширено на 5
мин назад. `scripts/exit_rule.py` — все правила выхода по леджеру (hold N / tp+sl / trail), первый
прогон см. ниже. **Сайт лежал 40 минут (09:14–09:54 UTC)** из-за отсутствующего импорта в
лейауте при статусе 200 — деплой теперь читает тела страниц. **Не сделано:** execution engine —
в `docs/fomo-endpoints.md` нет эндпоинта покупки, нужен захват реальной покупки в HAR
(`scripts/capture_fomo_endpoints.py`); мультичейн — отдельный проект (Helius/Codex бюджет,
FOMO_SESSION, второй бот). Volна-1 пункт 1 ждёт рефкод.

**Сессия 26 (25 сен): X выключен, сводка за 25.09.** *X:* постинг остановлен по требованию
автора — `X_ENABLED=0` в серверном `.env` (бэкап `.env.bak-2026-09-25`, 600), очередь `x_posts`
аннулирована (`attempts=3`, error «x posting stopped 25 Sep»), бот перезапущен,
`xpost.enabled()` → False. Токен `/opt/fomoradar/x_token.json` оставлен на месте — отзывать
доступ надо со стороны X (Settings → Security and account access → Apps and sessions →
Connected apps → Revoke), иначе он просто лежит неиспользованным. Гайд по отвязке аккаунта от
основного — в переписке, ключевое: **developer-аккаунт, которому принадлежит приложение, это
самая прочная связь**, плюс e-mail/телефон/устройство/браузер. *Сводка:* `FOOMS` — launch и burst
двумя минутами друг за другом, цены входа 0.000746 и 0.000880 (18% разницы, не 10×; расхождение
«сейчас» в отчёте — разное время измерения), но доля когорты **0.575 и 1.0** при ликвидности
$13.2k и объёме $4M после пуша: пул, где кроме нас никто не торгует. Вместе с row и CREDITS
(23 сен, доли 1.0 и NULL, оба ×0.05) это три случая подряд, поэтому введён **потолок**
`HOT_MAX_COHORT_SHARE=0.9` (`crowd_objection` теперь ловит оба конца: слишком мало — идём за
толпой, всё — толпы нет). *Gecko 429 (542/сутки):* очередь переоценки была 3,502 токена каждые
2 часа; теперь два такта — `PRICE_HOT_DAYS=2` (торговался за 2 дня или держится) каждые 2 часа,
остальные раз в сутки (`PRICE_COLD_MAX_AGE_S`). Замер на сервере: очередь **540 вместо 3,502**.
*«Люди»:* 353 адреса взяли 15,509 страниц трейдеров под браузерным UA — узкое число теперь
требует ещё и человеческого темпа (≤20 страниц в час), в отчёт добавлен блок `walkers`.
*Вердикты:* в отчёт печатается легенда `VERDICTS` (в т.ч. `dumped`), чтобы описание рутины не
расходилось с кодом. *Поток бёрстов — измерен, менять нечего.* Один алерт за сутки: это не новые гейты
(депт-гейт не задержал ни одного, единственный hold — namesake на лаунче FOOMS). Перепись по
ленте за 3 дня (`scratch/gc3.py`, точная формула conv = Σ(score/100)²): **правило бёрста срабатывает
2.7 раза в день**, не 15 (первая прикидка считала conviction без квадрата и врала). Из 8
кандидатов: 2 сняты правилом «меньше 180 с» (скрипт, не когорта), **5 — правилом «лента уходит»**
(sells ≥ 50% buys), 1 — глубиной. Дальше проверено, права ли лента (`scratch/gc4.py`, 7 дней,
$100 в каждый, час): **задержанные — −$97 на 11 измеренных** (BLESS ×0.06, FOOMS ×0.33, CREDITS
×0.50, AGE ×0.65…), **пропущенные — +$210 на 7** (VDT ×1.70, ORE ×1.55, SURGE ×1.41, HELIX ×1.41;
у всех пропущенных sells/buys = 0.00). То есть sell-ratio режет ровно убыточную половину, и
тишина в фиде — это рынок (филлов за сутки вдвое меньше), а не пережатые пороги. Пороги
оставлены как есть. 310 тестов зелёные.

**Сессия 25 (23 сен): сводка за 23.09 — OOM, квота на API, глубина пула, честные «люди».**
*Главное:* `radar-daily` убит OOM-killer в 06:52 (6.6 ГБ; свопа на сервере не было) — отчёт читал
сутки журнала caddy (725k строк, 760 МБ) целиком и держал каждую строку dict-ом. Теперь читает
потоком через `Popen` и хранит только счётчики: **248 МБ** пикового RSS, прогон под потолком
зелёный. Плюс `MemoryMax=1500M` + `MemorySwapMax=0` на юните (падает один, а не машина) и **swap
2 ГБ** на сервере (`/swapfile`, в fstab; инструкция в `deploy/README.md`). *Квота на API:*
`API_RATE_PER_DAY=20000` на адрес без ключа — ровный опрос никогда не упирался в минутное окно, и
двое (`trench-radar-probe` 324k запросов и голый Mozilla на `/api/trader/*`) дали 43% трафика и
11 ГБ отдачи за сутки; 429 объясняет, что ключ снимает лимит и превращает опрос в пуш.
Loopback (рендер сайта) и ключи не считаются. *Глубина пула:* row и CREDITS — 9 и 11 доверенных
кошельков, conv 5.16 и 6.47, оба пула **без глубины в базе** (полчаса от роду, скринер не
проиндексировал), оба ×0.05 через час. По леджеру за 60 дней (117 отправленных): «глубина
неизвестна» −$334, `<$25k` −$86, `$25–100k` −$799, `>$100k` **+$983**; по бёрстам порог
«известна и ≥$10k» оставляет 27 из 39 (+$610) и режет −$176. Введено: `safety.depth` (спрашивает
скринер про этот пул в момент пуша и сохраняет), `safety.thin`, `HOT_MIN_LIQ_USD=10000`, гейт в
`watch.push`. *Люди на сайте:* старое правило считало распределённый краулер (47.79/47.82, один
хит с адреса) людьми. Теперь два числа: широкое (браузер, не сканер, не облако краулера,
Accept-Language) — 3,204 IP / 4,367 просмотров, и узкое (вернулись за второй страницей или
подтянули ассет) — **417 IP / 1,580 просмотров**; `drive_by_ips` 27. Пиковый час считается по
узкому. *Мелочи:* число чатов в PUSHES берётся из леджера (backlog-quieting нового подписчика
читалось как «пуш в 1 чат» — INFRAETH); новый блок `LAUNCHES_UNSENT` — лаунчи, записанные и никому
не отправленные. *Не баг:* 16 `Forbidden` на бёрсте 20:51 — это первый бесплатный пуш нашёл все
чаты, заблокировавшие бота за месяц; все 16 помечены `active=0` тем же тиком, второй раз им не
писали. 310 тестов зелёные.

**Сессия 24, ещё (22 сен): бёрсты бесплатно, лаунчи — только по запросу, бот разнесён.**
*Почему:* за 30 дней $100 в каждый бёрст — **+$523** (37 измеренных, 51% выше колла, 11 × ×2),
в каждый лаунч — **−$1,205** (76, 34%, 16 × ×2); две трети пушей были лаунчами. При этом grace
кончился 20 сен 12:00 UTC и алерты уходили в 8 оплаченных чатов из 439 — 431 человек не получал
ничего и продолжал приходить (49 подписок 20-го, 15 — 21-го). *Сделано:* **бёрст-алерты
бесплатны всем** (`watch.push` больше не фильтрует по `pro.entitled_row`); **лаунчи сняты с
пуша совсем** — `bot.broadcast` заменён на `bot.sweep_launches`, который пишет их в леджер
**нулём чатов** (`pushes.record(..., shadow=True)`: без X-поста, без вебхука, без карточки;
`followups` по такой строке только меряет и закрывает). Леджер по-прежнему копит данные, но
`record.rows/report` по умолчанию берут только отправленное (`sent_only=True`, в API
`?include_unsent=1`) — запись продукта это то, что реально получили люди. Лаунчи отвечают на
**`/launches`** (алиас `/fresh`, бесплатно) и несут свою правду в том же сообщении:
`launch_record` дописывает «over 30 days $100 into every launch was −$1,205 at the 60-minute
read… The alerts are the bursts». PRO теперь: `/follow`, `/signals`, `/exits`, ключ API и
вебхуки; бесплатно: бёрст-алерты, `/hot`, `/launches`, `/top`, `/record`, `/paper`, дайджест.
Тексты бота (`HELP`, `HELP_PRO`, `PRO_ONLY`, `/start`, меню команд) и страница `/pro` переписаны
под этот расклад. *E (техдолг):* `bot.py` (1,350 строк) разнесён в пакет `fomo_agent/bot/` —
`telegram.py` (транспорт, 108), `words.py` (все форматтеры, 711), `subs.py` (подписчики, что
уходит по таймеру, 253), `commands.py` (ответы и цикл, 319), `__init__.py` реэкспортирует все
имена, так что `from fomo_agent.bot import X` и `bot.analyze.fresh` в тестах работают как
раньше. Перенос дословный. *Темп Telegram:* с 8 чатов на 439 упираемся в лимит Bot API (~30/с) —
`Telegram.call` ждёт `retry_after` и повторяет (3 попытки), рассылка держит
`TELEGRAM_SEND_GAP_S=0.04` между сообщениями, `send_each` не роняет остальных из-за одного
плохого чата. 307 тестов зелёные.

**Сессия 24, продолжение (22 сен): вторая дверь — ключ с вебхуками покупается на сайте.**
Аудит показал: 1,672 адреса читают API каждые сутки, а вебхуков продано 0 — потому что путь к
ним шёл через телегу (/start → /pro → котировка → сжигание → /claim → /apikey → /webhook).
Платёжный рельс при этом самообслуживаемый: котировка резервирует уникальную сумму, наблюдатель
матчит сжигание по сумме. Единственная привязка — выдача доступа на `chat_id`. Снята:
`pipeline/checkout.py` — веб-заказ это аккаунт `web:<secret>` (32 hex, живёт в localStorage
страницы, он же bearer), котировка берётся на него, `pro.record` при матче зовёт
`checkout.redeem` вместо `grant`, ключ выдаётся заказу и несёт **свой срок** (`api_keys.paid_until`,
миграция 31); `keys.Keyring` и `webhooks.targets` пускают ключ либо по своему сроку, либо по PRO
чата. Продление (`/api/checkout/<secret>/renew`) **не меняет ключ** — receiver, уже прошитый им,
продолжает работать. Никакого фантомного подписчика в `bot_subscribers` не создаётся,
`watch.confirm` веб-заказы пропускает (некому писать). API: `POST /api/checkout`,
`GET /api/checkout/<secret>`, `POST /api/checkout/<secret>/renew`, `GET /api/me`,
`POST /api/webhook`, `POST /api/webhook/test` (подписанный тестовый POST формы реального
события); все под `UNCACHED_PREFIX`. Страница `site/src/pages/webhooks.astro` — питч с живыми
цифрами, пример payload, подпись, виджет: «Get a key» → сумма и адрес с копированием → опрос
каждые 6 с → ключ + поле URL + «Send a test». Реклама там, где больно: заголовок
`X-Radar-Webhooks` на каждом ответе без ключа и та же строка в теле 429 («stop polling — the
alerts can be POSTed to you»). Цена та же, $20/30 дней, сжигается — шаг флайвила на месте.
Тесты `tests/test_checkout.py` (заказ → сжигание → ключ → хук → истечение; 304 зелёных).

**Сессия 24 (22 сен): сводка за 22.09 и черта по доле когорты.** *Регрессия моя, поймана
сводкой:* probe через роутер (сессия 23) читал «Exceeds max tx» на переводе 1% как honeypot —
шесть токенов за сутки (VDT, который сделал ×2 с продавцами, ORE ×2, KARURE, KEEL, ZEC) легли в
unsellable; void не ушёл ни по одному (пуши были старше 12 ч). Теперь ревёрт с текстом лимита
(`_is_limit`: max tx / max wallet / exceeds…) переспрашивается суммой в стотысячную; на сервере
шесть вердиктов сброшены (`sellable=NULL`), sweep переспросит. *Доля когорты:* все четыре пуша
21-го легли с `cohort_share=NULL` — Gecko индексирует новый пул минутами, а лаунч уходит внутри
них. Теперь объём пула читается с цепочки: `rpc.pool_currencies` (Initialize пул-менеджера
`RPC_POOL_MANAGER=0x8366…`, топик `0xdd466e67…`, валюты пула — нативный ETH 0x0 / WETH / USDG) и
`rpc.pool_volume_usd` (Swap-события по id пула, топик `0x40e9cecb…`, |amount| стороны котировки,
цена WETH); Gecko — запасной путь; «cohort share of X unmeasured: why» в журнале. Исследование
`scripts/crowd_share.py` с мелкими корзинами (93 алерта): <1% −$327, 1–2% −$1,398, 2–3% −$250,
3–5% +$741, 5–10% +$206, 10–33% +$402; таблица порогов — **3%**: оставлено 37 (+$1,364, 54% выше
колла), срезано 56 (−$1,975, 18%). `HOT_MIN_COHORT_SHARE=0.03` включён; ждать ~60% меньше
пушей. Свечи исследования кешируются (`/tmp/crowd_candles.json`), перерасчёт мгновенный.
*Лаунч не раньше 3 минут* от первой доверенной покупки (`TELEGRAM_LAUNCH_MIN_AGE_S=180`): DEED
ушёл через две минуты после начала волны засева, seeded задним числом. *Токен в журнале:*
`cli.Redacting` вычищает секреты из каждой строки и трейсбэка, «poll failed» пишет класс и
начало без URL; **токен бота перевыпустить** (лежал в journald дважды). *Журнал:* `SystemMaxUse`
1G → 4G (держал 21 ч: uvicorn 776k строк/день + caddy 822k), access-log uvicorn выключен.
*Страницы при лежащем Gecko:* нетерпеливый клиент с таймаутом `GECKO_IMPATIENT_TIMEOUT_S=4`
вместо 20, дальше кеш. *Сканер:* daily_report исключает из «людей» IP с ≥100 429 за окно
(`SITE.scanners`, `journal_from` — с какого часа журнал жив); jail `caddy-429` (300 за минуту →
час бана) в `deploy/fail2ban/`. *Шум:* `watch.held` — «not pushed» раз в час на токен (AGE был
48 раз). *Вердикт vydamo_* — dropped, по делу. *Контроль через 20 минут после деплоя:* ORE и KARURE
переспрошены — «goes through at a hundred thousandth», вердикт unknown (честно); VDT/ZEC ждут
sweep (переспрашивает только тронутые доверенными за сутки); журнал API — 0 строк; jail
caddy-429 считает (49 отказов, банов 0); 429 Gecko — 7 за полчаса при работающем исследовании.

**Сессия 23, продолжение (21 сен): пять предложений сделаны.** *Клон известного тикера:*
`analyze.LISTED_TICKERS` (топ рынка по имени, `LISTED_TICKERS_EXTRA` в .env добавляет) +
`analyze.borrowed_name` — имя с биржи или уже запускавшееся на цепочке за `NAMESAKE_DAYS=14`;
в сообщении строка «⚠ $ZEC is a listed ticker; this is a Robinhood Chain token wearing its name;
the 4th $ZEC on this chain in 14 days · 0x824c… 3d ago · 0xd113… 11d ago honeypot»; лаунчу
нужно `NAMESAKE_BAR_MULT=1.5` × heat, бёрсту × conviction (bot.due, watch.push). *Void в X:*
`xpost.void` — реплай под постом пуша тем же фактом, а пост, ещё стоящий в очереди, снимается
(`attempts=3, error='voided before posting'`); вызывается из `safety.void_pushes` при первом
void. *Толпа против когорты:* `safety.cohort_share` — доллары когорты / объём пула за час
(gecko `volume_usd.h1` через `crowd()`), пишется в `pushes.cohort_share` (миграция 30), строка
«of the pool's hour 4%» в сообщении, в вебхуке и в `/api/record`; гейт `HOT_MIN_COHORT_SHARE`
(0 = выкл) — `scripts/crowd_share.py` меряет по леджеру (когорта за полчаса до пуша против
минутных свечей пула), результат ниже. *Раздача:* `analyze.distributing` —
`DISTRIB_MIN_SOLD_USD=50k` продаж и ≥`DISTRIB_RATIO=5`× покупок за 7 дней; модель видит
`flags.distributing`, `apply_score` держит статус не выше watch и дописывает причину в summary и
тег; профиль (`flow_7d`, `distributing`, `pnl_gap` при расхождении fomo/индексер ≥
`PNL_GAP_USD=100k`), карточка бота и страница трейдера показывают. */follow с каждого пуша:*
`bot.follow_line` — «follow the best of them: /follow_unipcs» (лучший по скору из вошедших;
хендл не из алфавита команд — двухсловная форма), `/follow_<handle>` разбирается как `/follow`.

**Сессия 23 (21 сен): сводка за 21.09 — что починено, что оказалось не так, как прочитано.**
*Ложная тревога:* «watcher завис на 23 минуты» (02:10 → 02:33 UTC) — не завис. Тик без филлов
ничего не пишет, поэтому непрерывность `from` в журнале ничего не говорит о сканировании; лента
collect (независимые 12k-блочные сканы 02:13–02:32) тоже нашла 0 филлов ростера в тех блоках —
цепочка была тиха (переводы через роутер упали с ~370 до ~180 на 12k блоков). Чтобы такое больше
не читалось как дыра: **heartbeat** `watch: alive · tick N · head · fills, last N min ago`
каждые `WATCH_HEARTBEAT_S=300`, строка `watch: tick took Ns` при тике дольше 2× интервала,
RPC-клиент наблюдателя с таймаутом `WATCH_RPC_TIMEOUT_S=30` (было 90 — цепочка `_post` из
четырёх попыток по всем эндпоинтам могла молчать 12 минут), HEALTH «watcher gaps» называет обе
причины и говорит, чем их различить. *ZEC:* honeypot ушёл лаунчем в 7 PRO-чатов на 20-й минуте
(пул v4-типа → chain-probe «unknown»; правило тишины ждало 30 минут при 8 покупках) и был помечен
на 36-й (91/0). Теперь **тишина говорит тем раньше, чем больше купили**: ожидание =
`SELL_SILENCE_MIN_AGE_S × SELL_SILENCE_MIN_BUYS / buys`, пол `SELL_SILENCE_FLOOR_S=300`
(8 покупок — 30 мин, 16 — 15, ≥48 — 5); вердикт тишины — единственный «нет», который
переспрашивается (`check` через `max_age_s`, `sweep` каждые полчаса — фиды токен уже выкинули,
больше некому; первая продажа снимает его), revert остаётся финальным;
для пула без адреса probe идёт на роутер (`RPC_ROUTERS`) и считается только revert. **Void:**
`safety.void_pushes` — токен, запушенный в последние `TELEGRAM_REALERT_HOURS` и ставший
unsellable, отзывается в те же чаты одним сообщением (`fmt_void`: факт из `sell_note`, «off every
feed, the record counts it as a honeypot», без советов), ключ `void:<mint>` в `bot_sent`, вебхук
`event: void` (в `/docs` API), зеркало в Discord. *Follows:* чат, заблокировавший бота, остаётся в
`follows`, но `follows.alerts` теперь джойнит `bot_subscribers.active=1` — ни попыток, ни строк в
`bot_sent`; `/start` возвращает всё. *daily_report.py:* `fill:`/`void:` ключи вынесены из пушей
в блок `FOLLOWS`; вердикты: `dumped` (пик ≥1.5, сейчас <0.5 — FN), `failed` при `now<0.5`
независимо от возраста («+» на 0.24× больше не «open»), `voided` на строке; COLLECT считает
`holdings_cut_short` и `gecko_429`; WATCH — `heartbeats` и `slow_ticks`. *Gecko 429 (785 за
сутки):* лимит 30/мин считается по IP, а лимитеров было шесть (collect, bot, watch, 3 воркера
API) по 20 каждый. `ratelimit.SharedRateLimiter` — окно в SQLite-файле `RATELIMIT_PATH`
(по умолчанию рядом с БД, `/opt/fomoradar/ratelimit.db`), одно на машину; `take()` без ожидания
для нетерпеливого клиента API, `GECKO_MAX_REQ_PER_MIN=25`, из них `GECKO_RESERVE_PER_MIN=5`
держатся для request-потоков (график на странице токена), батчи ждут на остальных и держат
`GECKO_MIN_INTERVAL_S=2` между вызовами на всю машину (пачки по три в секунду Gecko режет и
при 22/мин). Замер с сервера: 20-й вызов в минуту — там, где начинаются 429, потому
`GECKO_MAX_REQ_PER_MIN=20`. Главный потребитель оказался `/api/hot` (80 запросов/мин от ботов):
`hot.recent` меряет каждый бёрст окна по свечам, и три воркера освежали ~40 отыгранных пулов
каждые 5 минут — `api.candles_for` теперь держит свечи бёрста старше суток `SETTLED_TTL=6h`.
Колонка `who` в леджере лимитера (`SELECT who, COUNT(*) FROM calls GROUP BY who`) показала
настоящего едока: `serve` 14–18/мин — это `/api/token/<mint>/chart` (263 вызова за полчаса от
fomo-paper, MemeDesk, DegenTape, shadow-dashboard; 80 разных пулов), по своему 5-минутному
кешу в каждом из трёх воркеров. Теперь кеш свечей общий через БД (`candle_cache`, миграция
29) и живёт по шагу свечи: 24h — 10 мин, 7d — 20, 30d — 60 (`CANDLE_TTLS`); при 429 отдаётся
последнее, что видел любой воркер. `live_lookup` не при чём: из 306 адресов за полчаса
неизвестных 6. Замер после всего: **2 × 429 за 25 минут против 12** днём раньше, `serve`
4–6 слотов/мин вместо 14–18, «allowance spent» у API — 0 (график отдаётся всегда).
Тесты `tests/test_ratelimit.py`, 289 зелёных. SSH: sshd под брутфорсом
(fail2ban: 167 в бане, 4.7k неудач) и MaxStartups роняет лишние коннекты — не опрашивать
сервер циклом по ssh каждые 20 с, одна сессия с циклом внутри. Holdings «after 1800 of 2000 pairs: rate limited» — пасс
сохраняет прочитанное, остаток идёт первым в следующем (`stale_pairs` сортирует по давности),
данные самовосстанавливаются; в отчёт добавлен счётчик.

**Сессия 22, ещё (18 сен): paper-артефакт, трейл, борд рук.** Paper +$2,807 был артефактом: у
строк леджера, измеренных только по ленте (свечей на момент follow-up не было), в `now_x` лежала
текущая котировка против входа, а не закрытие часа — musebook читался как ×25.94.
`scripts/remeasure_pushes.py` перечитал 91 строку по свечам, 14 без свечей очищены (часовое
чтение NULL, tape-best оставлен); honeypot в paper = −$100 (ставка ушла); `dead` требует
`vol_usd` не NULL. Честно: **час −$598** (89 сделок, 35%). Файлы на рабочем столе с +$2,807 —
недействительны. Рядом второе чтение тех же свечей — **трейл** (`hot.outcome` → `trail`,
`pushes.trail_x`, миграция 28, `TRAIL_DROP=0.2`): выход на первой свече с low на 20% ниже
бегущего максимума внутри часа, по этому уровню, иначе по последнему закрытию; первая свеча —
особый случай (стоп под входом). Итог **+$102** (87 сделок, 32%, лучший +$201, худший −$100).
`record.report` отдаёт `totals.paper_trail`, `curve_trail`, `trail_drop`; `/paper` в боте и на
сайте показывают оба чтения (пунктирная кривая — трейл), API тоже. `scripts/exit_rule.py`
(горизонт 4 ч, 68 алертов): трейл −20% — единственное правило, платившее и на бёрстах, и на
лаунчах (+$1,044); **решение о правиле выхода отложено на неделю данных**, трейл — измерение, не
пуш, механика exit-пушей не меняется. **Борд рук** — `pipeline/hands.py` + `assets/boards/hands.html`
(1080×1350) и `hands-wide.html` (16:9), генератор из леджера/ленты/журнала Caddy: /PAPER (кольцо
88% как якорь, оба чтения рядом, hook «the hour exit sells the peak short»), /FOLLOW (топ-4 по
pnl_30d, цепочка chain → chat 20 s → screener 5 min), /INVITE, /WEBHOOK (читатели API за сутки,
кто «тяжёлый» = потенциальный плательщик, burn = n × $20), «smarter alerts» (волны за неделю,
ключ создателя, команда). Каждый блок несёт тег тг-команды и короткое пояснение — по требованию
автора. Отдаётся с `fomoradar.app/boards/` (Caddy `handle_path /boards/*`, root
`/opt/fomoradar/boards`), `radar-hands.timer` 07:10 UTC, PNG ×2, `hands.mp4` (8 с, ffmpeg),
`hands.json`; `?still=1` без движения. Права: `/opt/fomoradar` 751, БД 640, `x_token.json` 600.
Запись экрана — с `https://fomoradar.app/boards/hands.html` (вертикаль) или `hands-wide.html`.

**Сессия 21: PRO — доступ к алертам за токен, сожжённый. `pipeline/pro.py`.**

**Как работает.** `/pro` в боте → точное число $FOMOBRAIN на $20 по цене пула (основание,
округлённое вверх до сотни-тысячи, плюс хвост 1–999 — уникально среди открытых котировок) →
человек отправляет ровно столько на `0x…dEaD` из любого кошелька; вотчер тем же тиком читает
`Transfer(to=dead)` одним `eth_getLogs`, сумма совпала → `paid_until += 30 дней`, бот
подтверждает. Ничего не подключается и не подписывается: сумма — квитанция. Котировка живёт
30 минут, точная сумма принимается ещё 6 часов после (перевод в пути), и всё это время сумма
зарезервирована. Круглая сумма или переплата за несколько месяцев → лежит без чата, `/claim <tx>`
привязывает (receipt с чейна, если вотчер пропустил блок); tx — первичный ключ, второй раз не
зачтётся. Страница `/pro/<код>`: сумма и адрес с copy, таймер, опрос `/api/pro/<код>` каждые
8 с, зелёная при оплате. `/pro` на сайте — условия и кнопка `t.me/<бот>?start=pro`.
**Гейт:** пуши launch/burst и `/hot /signals /fresh /exits` — PRO; `/top`, адреса, хендлы,
дайджест — бесплатно. `PRO_PRICE_USD=0` — гейта нет (так идут тесты); `PRO_GRACE_UNTIL` —
все, кто подписался раньше этой даты, бесплатно до неё (запуск); `PRO_TRIAL_DAYS` — новичкам.
Напоминания за 3 дня, за день, по истечении — по одному на оплаченный период, продление
сбрасывает. `cli pro` — цифры и ручной grant/claim для поддержки; `PRO` в daily_report.
Проверено на чейне: перевод FOMOBRAIN на dead проходит (симуляция от трёх держателей), 18
знаков, налога нет. 12 тестов в `tests/test_pro.py`. Telegram-правила (Stars для цифровых
товаров «внутри приложения») — оплата вынесена на сайт, бот только называет сумму; дверь A
(Stars-подписка) — следующий шаг, если придёт уведомление. **На сервере:** `PRO_PRICE_USD=20`,
`PRO_GRACE_UNTIL=1789905600` (20 сен 2026 12:00 UTC) — до этой даты все, кто подписался
раньше неё, бесплатно; вотчер читает burn-логи только пока есть открытая котировка (RPC
бюджет). Ждёт боевого прогона с тестового кошелька и анонса.

**17 сен.** По сводке: один WARNING на потерянный скан вместо 400; `TELEGRAM_DEDUPE_S=1800`;
`collect scans` смотрит сутки; промахи Gecko в API и `fomo disabled` — DEBUG; `daily_prep.sh` ждёт
конец collect и переспрашивает свечи; запасной RPC читает `eth_getLogs` и при «rate limited after
4 attempts». **Новое:** `pipeline/pushes.py` — леджер пушей (`pushes`: kind, mint, ts, px, heat,
conviction, wallets, liq, chats) и через `TELEGRAM_FOLLOWUP_MIN=60` минут тем же чатам: пик и
когда, сейчас, объём — факт, не совет; через две недели по нему читается правило выхода.
`pipeline/keys.py` — `/apikey` для PRO-чатов, `X-API-Key` = 600/мин (`API_KEY_RATE_PER_MIN`),
без ключа 120, без User-Agent — 400 (`API_REQUIRE_USER_AGENT`). `fresh(now=)` — реплей ленты
на момент пуша; по 38 лаунчам порог heat ничего не отделяет чисто (≥2.5: 50% до 2× у 22
оставленных против 19% у 16 отрезанных, но среди отрезанных musebook 12× и VLAD 3.6×); пауза
после последней покупки — **6 минут** (`TELEGRAM_LAUNCH_MAX_GAP_S=360`: 13/32 до 2× внутри,
1/6 снаружи; две минуты стоили бы SWARM 8× и musebook 12×). `scripts/paper.py` — бумажная
торговля по всем пушам с кэшем свечей в `/opt/fomoradar/daily/candles/`. История: 82 пуша с
11 сен, 66 измерено, **54 (82%) торговались выше цены пуша** после свечи пуша, 26 (39%) ≥2×,
медиана пика 1.62×; bursts 54% до 2× против 36% у launches; сейчас выше цены пуша 13 из 69.

**16 сен, по сводке за день.** Нода Robinhood шатается сама (бэкенды `10.31.x.x:8547`
таймаутят, до 44/час): вотчер на такой отказ теперь ждёт 5 с, не 25 (`WATCH_NODE_ERROR_WAIT_S`),
скан ростера пробует второй раз через 10 с, `eth_getLogs` при отказе ноды читается через запасной
dRPC ломтями по 100 блоков (`RPC_SPARE_SLICE_BLOCKS`). HEALTH: `collect scans` (доля проходов
с потерянным сканом за 6 ч) и `watcher gaps` (самая долгая тишина на ленте). API: промах живого
поиска токена помнится час (`_missed`), `API_WORKERS=2`, `API_CACHE_TTL_S=30` на сервере;
34.186.82.14 (UA `node`, 52k запросов/час) — `respond 429` в Caddy. Пуши: launch только если
последняя покупка когорты ≤120 с (`TELEGRAM_LAUNCH_MAX_GAP_S`; по 26 пушам все победители ≤72 с,
5 из 6 поздних провалились), одно сообщение на токен за 10 мин (`TELEGRAM_DEDUPE_S`), опрос
лаунчей раз в минуту; в пуше строка про клонов по имени за 24 ч (`analyze.namesakes`); токен,
у которого только пулы-ловушки (комиссия ≥10%) — unsellable. Скоринг: позиция с прибылью без
cost basis помечена `unearned` (685 из 3 508 открытых, все крупнейшие — переводы/эирдропы),
кошельки без ленты и книги не экспортируются. `radar-daily.timer` 06:50 UTC готовит
`/opt/fomoradar/daily/<date>/` (report.jsonl, pending.json, digest.txt, health.txt); десктоп-задача
читает их. Карантин >100k строк делает VACUUM сам.

**15 сен, диагностика после двух дней без присмотра.** Резолюция 13 сен отдала профиль Stavyyy
адресу 0x8f10b4… — роутер/арбитражный бот: 275 399 филлов за сутки по 5 315 токенам, лента
выросла с 4–5 тыс. до 309 тыс. строк в день, БД 757 МБ, страницы p95 3 с, и его строки с
кривыми ценами дали «748×» на скоркарде (PVE, TICK, HUMANITY…). **Закрыто:** `pipeline/noise.py`
— адрес с >300 филлов/час (`NOISE_FILLS_PER_HOUR`) карантинится вотчером каждый тик: dropped,
флаг bot, филлы удалены, профиль отвязан, адрес в `noise_addresses`, резолюция его больше не
предлагает; `cli noise [--scan]`. Первый тик снёс 625 117 строк, VACUUM 757 → 139 МБ за 1,6 с.
`outcome()` читает с ленты только kind=trade с $≥1, свечи с чистым множителем 10ⁿ к цене филла
(пулы с 32-байтным id — ×1000 у GT) пересчитываются, а не выбрасываются. Честный счёт 13–15 сен
(21 пуш, 12 токенов): 2× — PROPPED 2.75, SYNTH 384 (алерт на старте кривой), IPO 3.9,
STANDARD 2.5; TICK 1.9; остальные 0.4–1.4. 121 кошелёк оценён в чате (15 active, 99 watch,
7 dropped). $FOMOBRAIN за два дня −96% ($0.000336 → $0.0000136, FDV $13.5k); PRO: 6 оплат,
$120 сожжено. Открыто: API под ботами (6 чужих клиентов, ~750k запросов/48ч) — p95 страниц
2,7 с, кэш-хиты по 0,5 с, один воркер на 40% CPU → следующий шаг: 2 воркера + TTL кэша 30 с.

**Нода Robinhood режет `eth_getLogs` на 10 000 логов (с 10 сен), 13 сен это сломало
15-минутный проход:** 400 кошельков × 200k блоков > 10k, каждый кошелёк падал, 800 запросов
за проход впустую, ноль сделок, вотчер стоял за ними в 429 (49 отказов/час). Тестовый burn
зачёлся через `/claim`, не тиком. **Закрыто:** `RobinhoodRPC.logs()` делит отказанный диапазон
пополам и помнит размер, который нода отдаёт (`_max_span`); упавший скан не повторяется по
каждому кошельку; проход отдаёт источнику хэши, которые уже на ленте (`skip_known`) — receipts
только за новое (было: сотни, стало 18 запросов/проход, 5 063 из 5 324 филлов уже были);
`RPC_WINDOW_BLOCKS=12000` на сервере; `RPC_URLS` = dRPC free (ключ в `.env`) как запасной на
один отказанный вызов — не переключение: их free-план отдаёт head/eth_call/receipt по одному,
отказывает на диапазон >100 блоков и на batch (500), такие вызовы возвращаются ждать ноду.
Burn-чтение с собственным курсором и вторым глазом в боте (`pro.Cursor`, `bot.Burns`).

**Сессия 20: нетерпеливый клиент, кейс CATGPT, аудит сайта и бота.**

**Зависания на /hot убраны.** GeckoTerminal-клиент внутри API спал в лимитере и делал шесть
бэкоффов на 429 прямо в потоке запроса — при 30 читателях `/hot` и `/api/hot` держали
соединения по 40–60 с, Caddy записал 2 737 ответов со статусом 0. Теперь у API свой клиент
`GeckoTerminal(patient=False)`: нет окна — `Busy`, страница рисуется без свечей, ни один запрос
не ждёт чужого лимита. Пайплайн (digest, hot --backtest) остался терпеливым. После выката —
ни одной медленной минуты в логе.

**CATGPT — первый честный кейс всплеска, по секундам.** Пул 23:49:53, первая доверенная покупка
23:57:22, лонч-пуш ушёл бы в 23:57:39 (heat 3.4, шесть кошельков за 16 минут), седьмой кошелёк
перевёл conviction через 4.0 в 00:00:21, алерт в 00:00:44 — 23 секунды от сделки до Telegram,
на цене 0.00000098. Пик 13.9× в 03:00, спустя сутки 5.2×. Собрано в инфографику 1600×900
(`assets/cases/make_case.py`, `assets/cases/catgpt/`): шаг conviction с нумерованными
входами, полоса когорты с аватарками fomo, часовые свечи × цена алерта, рейка часов.

**Аудит сайта, 24 часа Caddy-лога.** 52 775 запросов с 4 288 адресов; 0,45 ГБ; после выката
нетерпеливого клиента страницы p50 23 мс / p95 560 мс, API p50 13 мс / p95 182 мс, ни одного
ответа дольше 5 с. Кто читает: FomoPilot/0.1 (9 551 с одного адреса, каждые
9 с — чужой бот на нашем API), python-httpx (5 618, 435 из них — 429: лимитер работает),
ClaudeBot (2 435, 1 646 разных страниц — индексация), PaperBot, dime-fomo-radar,
LocalFomoTracker, rh-copytrader — API уже используют шесть чужих клиентов. Единственный
провал за сутки — 172×502 в 11:23–11:24: uvicorn при рестарте ждал зависшие в Gecko запросы 64 с,
а сайт (`After=radar-api`) ждал его. **Закрыто:** `timeout_graceful_shutdown=3` в uvicorn,
`TimeoutStopSec=8` в api/bot/watch, деплой рестартует api+site парой, потом bot+receive;
лимитер страниц в `site/src/middleware.ts` — token bucket на адрес, 60 залпом и 120/мин
дальше, 429 с Retry-After, loopback без XFF не считается (проверено локально: 61 прошло,
9 отказано); `robots.txt` закрывает `/api/` от индексации. Что не сделано и не нужно пока:
Cloudflare-прокси (решение автора, у Porkbun: DDoS и боты до сервера), fail2ban на 429 (лимитер
и так отвечает за 0,3 мс).

**Аудит бота: три подписчика на четыре тысячи посетителей — потому что `/start` не подписывал.**
Теперь `/start` = подписка + короткая справка; `/stop` (и `/unsubscribe`, `/mute`) выключает и
говорит, что фиды продолжают отвечать; `/subscribe [порог]` объясняет четыре вида пушей и
частоту («обычно 5–15 в день, 3 — больше, 8 — меньше»); справка начинается с «пришли адрес или
хендл», пять фидов, без операторских `/status`, `/health`, `/digest`, `/watch`, `/dropped` (они
работают, просто не в списке); `setMyCommands` при старте — меню из семи команд. Тестов 195.

**Сессия 19: мозг на главной, сайт под нагрузкой, GitHub.**

**Мозг.** Радар на главной заменён на концепт v6.1 (`site/src/components/Brain.astro`): облако из
~6 000 частиц в форме органа, секущая плоскость, возбуждение, которое расползается по соседям через
пространственный хэш, шесть станций, кошельки ходят по нервам. Портретная компоновка справа от
заголовка — три станции сверху, три снизу, концы нервов читаются из прямоугольников панелей. На
телефоне станции прячутся, облако вдвое реже; reduced-motion — один кадр. Надпись «gpt-6 astra» в
станции JUDGE оставлена как в концепте — по просьбе автора, для индексации постов; скоринг в коде
модель-агностичный (export/import в любой LLM-чат).

**Сайт под нагрузкой — нашлась дыра.** Лимитер API считал все серверные рендеры сайта одним
посетителем `127.0.0.1`: 120 запросов в минуту на всех, ~40 просмотров главной, дальше каждый видит
«The data service is not answering». Закрыто три слоями: loopback без X-Forwarded-For не
лимитируется; 10-секундный кэш в `site/src/lib/api.ts` с одним запросом в полёте на адрес; тот же
10-секундный кэш внутри API на каждый GET (`remember_responses`), с дедупликацией промахов — при
истечении записи под 60 читателями тяжёлый запрос запускает один, остальные ждут. Изнутри
сервера: API 804 запр/с, сайт 207 стр/с при 60 одновременных. Снаружи при 80 читателях серверные
p50 3–16 мс, p95 100–200 мс, max 0,8 с, ошибок ноль. Секунды в моём внешнем тесте были дорогой и
TLS с моей стороны, не сервером.

**GitHub: `github.com/cvxv666/fomo-robinhood-radar`**, публичный, MIT, CI зелёный, описание,
homepage, десять тем. Перед публикацией: скан секретов по дереву и по всей истории — чисто; адрес
сервера убран из восьми файлов (`update.sh` требует `RADAR_HOST`, `.bat` отказываются без него,
в документах `<server>`); README открывается сегодняшним продуктом, четырьмя «вещами» (четвёртая —
провенанс), бейджами и галереей из шести скриншотов в 2× (`docs/screens/`, сняты headless Chrome на
сервере через loopback — на холодном старте он не верит собственному сертификату сайта);
`.env.example` несёт все настройки месяца. Футер сайта ведёт на репозиторий (`PUBLIC_REPO_URL`
теперь передаётся в сборку). CI с первого раза упал: `monotonic()` считает от загрузки, на свежем
раннере ноль в `last_alert` означал «ждать интервал перед первой рассылкой» — `-inf`.

**Мелочи.** Страница `/about` доведена до четырёх «вещей», 101/101, всплеска и меток dust/gift/
seeded. Метки dust/gift появились и в «Recent fills» трейдера. Удалены неиспользуемые
`Scope.astro` и `Verdict.astro`. Тестов 192.

**Что осталось — на стороне автора:** `HEARTBEAT_URL` (healthchecks.io, период 20 / grace 10) —
единственное, что не мониторится извне; перевыпустить ключ fomoapi (дважды был в чате). **В коде:**
бенчмарк калибровки против рынка (табло всплесков — первый кусок); скриншот страницы Bursts в
галерею, когда на ней будут настоящие всплески; 401 покупок без квитанции за окном узла остаются
NULL — несущественно.

**Сессия 18: чья это сделка. Самая большая дыра проекта, найденная пользователем в первый же час.**

**Первый живой всплеск оказался подделкой.** JUGGERNAUT-клон `0x3adde…`: 17 доверенных
кошельков «купили» за минуты, пуш ушёл на $20K капы, токен сделал 22×. Вопрос пользователя —
«а unipcs точно сам купил, или ему прислали?» — и ответ: **никто из семнадцати не покупал.** Четыре
чужих ключа вызвали роутер fomo напрямую, заплатили своим ETH (`tx.value` 0,03–0,24) и указали
получателем свопа доверенный кошелёк. Наш `routed_fills` читал «токен пришёл от роутера» как
«кошелёк купил» — и так же читает любой трекер.

**Вторая дыра в тот же час.** ASTRO `0x2c99…` — первое место в сигналах на 27 «покупках» по
$0,46–0,87, доставленных 18 доверенным кошелькам **через официальный поток fomo**: entrypoint
`0xccc88a9d…`, горячий кошелёк USDG `0xf70da978…`, подписи релееров. Структурно неотличимо от
настоящей покупки. Тридцать пять долларов за верх страницы.

**Что не помогает: подписант.** 100% покупок за сутки подписаны не кошельком — так устроен fomo:
142 релеера за день, многие с vanity-адресами `0x4337…` (ERC-4337). «Подписал не владелец» —
норма каждой сделки на этой цепочке.

**Что помогает — три слоя (`pipeline/provenance.py`, миграция 18, `trades.kind`):**

1. **`direct`** — транзакция отправлена *в сам роутер*, а не в entrypoint fomo. Из квитанции,
   которую мы и так забираем. Сделка через приложение fomo никогда так не выглядит. Такой филл —
   реальная рыночная активность, но ничья сделка: не считается нигде.
2. **`dust`** — покупка меньше max($5, 10% медианы этого кошелька). Трейдеры делают мелкие
   пробники (unipcs — медиана $17), поэтому пыль хранится и показывается, но не входит в
   conviction. На 30 днях порог режет ~7% доверенных покупок, все — пробники.
3. **Засеянный токен** — ≥3 доверенных кошелька получили direct/dust за сутки → токен исключён из
   сигналов, всплесков и fresh, на странице метка `seeded`, филлы помечены. Схема становится
   самоубийственной: чем больше кошельков засеешь, чтобы выглядело как когорта, тем вернее токен
   исчезнет. За один день правило поймало ASTRO 17, PEPAI 10, NEXA 8, DANBO 8, CHIP 3 — и ни
   одного настоящего.

Сканер пишет `direct`/`flow`; `classify` доводит `flow` до `trade`/`dust` по медиане кошелька
(`traders.median_buy_usd`, обновляется каждым проходом). Старые строки — NULL, считаются сделками,
пока `cli verify-fills` не заберёт их квитанции: ограниченный хвост, не постоянное состояние.
Всплеск на засеянном токене остаётся в записи (лента на нём сработала), но из табло выпадает.

Фикстура `tests/fixtures/rpc_receipts_gift_vs_genuine.json` — две настоящие квитанции: подарок
unipcs'у и настоящая покупка FLYBRAIN. Тестов 187.

**Разметка семи дней сделана:** 23 313 покупок, 21 165 trade, 1 287 direct, 469 dust, 401
без квитанции (за окном узла). 12% покупок доверенных кошельков за неделю — не их; задеты 197 из
249. По штукам топы засеяны сильно (kyle 199 из 298 за 30 дней, unipcs 266 из 500), по деньгам —
почти нет (kyle $2,4K из $466K): посев работает копейками и раздувает счётчики, не денежную картину.

**Порог пыли пришлось смягчить с 10% до 2% медианы**, а правило «засеян» дополнить условием
«подсаженных больше, чем настоящих покупателей»: при 10% derek518 с медианой $4 969 набрал серию
покупок по $150–380, они стали «пылью», и SHROOM с $1,6M ликвидности и 43 настоящими покупателями
выпал из лент. Это обратная атака — за $5 пыли спрятать чужой токен, — и второе условие её
закрывает. `cli resize-fills` пересуживает размер под новый порог.

**Пересчёт двадцати кошельков** (≥10% покупок за 30 дней чужие), в чате, по собственным филлам:
0xnobi 80→66 и 0xWives 70→64 ушли в watch (у обоих одна позиция и мало своего), kyle 88→85
(12 ранних входов из 77 токенов, а не 48 из 124), остальные ±2, unipcs/0xAvast/Quanterty без
изменений. Ростер: 167 active, 155 watch, 52 dropped. Старые вердикты в `score_history`.

**Сессия 17: всплеск — и наблюдатель, который его видит за двадцать секунд.**

**Вопрос был: FLYBRAIN, сегодняшний раннер, — когда он попал в радар?** Восстановил по ленте.
Первый доверенный кошелёк вошёл в 19:15 UTC ещё на бондинг-кривой, второй — в 19:17 (порог сигнала
«2+ кошелька» пройден), к 20:18 восемь active-кошельков и conviction 4.4 — порог пуша. В базе это
лежало в 20:35, пул вышел на DEX в 20:51, забег начался в 23:00 (0.0004 → 0.035 к 02:00, 27× от
цены выхода). Оговорка: между сигналом и забегом цена сначала упала втрое.

**Задержка «сделка → пуш» была 15–20 минут:** `track` раз в 15 минут внутри общего прохода плюс
120-секундный таймер бота. Для цепочки с блоком в 0,1 с это много.

**Правило «всплеск» (`pipeline/hot.py`).** Скользящее окно по *первым* покупкам доверенных
кошельков: сумма (score/100)² тех, кто впервые вошёл в токен за последние W минут, ≥ Δ от ≥ N
кошельков. Тот же conviction, что везде, — только с часами. Прогнал по всей ленте
(`cli hot --backtest`), 36 дней, 116 тысяч филлов, цена — та, что подразумевает каждый филл.

Что показал бэктест (нынешние оценки, горизонт 24 ч):

| правило | срабатываний/день | достигли 2× | достигли 3× | медиана через 24 ч | ниже 0,5× |
|---|---|---|---|---|---|
| сигнал как есть (2+ кошелька за сутки) | 52 | 36% | 23% | 0,61× | 43% |
| всплеск Δ3 / 30 мин | 8 | 40% | 27% | 0,75× | 40% |
| **всплеск Δ4 / 30 мин** | **5** | **39%** | **27%** | **0,82×** | **42%** |
| всплеск Δ5 / 60 мин | 4 | 47% | 31% | 0,83× | 40% |

Честная картина: всплеск лучше базовой линии по каждой метрике и в десять раз избирательнее, но
это всё ещё монетка с положительным хвостом — ~40% доходят до 2× за сутки, ~40% заканчивают день
ниже половины. Ценность в лучшей цене (медиана 1,6–1,9×), а не в «держать сутки»: выход важнее
входа. FLYBRAIN с его 27× — хвост, не медиана.

Два уточнения, которые решили пороги. Первое: девять из десяти всплесков — в первый час жизни
токена (когорта апает лончи), и это как раз монетка. Те немногие, что случились на возрасте 1–6 ч
(«когорта вернулась в токен, переживший первый час»), — лучший срез: 50–82% до 2×, но выборка
8–13 штук. Поэтому возрастного фильтра нет, а возраст печатается в сообщении. Второе: при Δ ≥ 2
минимум кошельков не работает — три нужны арифметически. Пороги: **Δ 4,0 за 30 минут от 3
кошельков** — те же «четыре восьмидесятки», что у пуша сигналов, только с часами. Всё в `.env`.

Отдельно про сами оценки: 6 сентября первая волна скоринга дала средний балл 45 и половину
недоверенных; 9-го рескоринг поднял 304 кошелька до 66, 202 перешли черту доверия. «Первый
вердикт» как основа бэктеста — это те самые оценки, которые признали неверными; поэтому основной
режим — нынешние оценки за всю ленту (с оговоркой, что это чтение ответа заранее; сам скоринг
проверен вне выборки в `calibrate.py`), а strict-режим — 5 дней и та же картина.

**Наблюдатель (`pipeline/watch.py`, `radar-watch.service`).** Каждые 20 секунд: «голова» цепочки
одним запросом, два `eth_getLogs` только по новым блокам, квитанции пачкой, — 4 запроса на тик,
12 в минуту на собственном лимите 15. Филлы пишутся через тот же `insert_trade`, `fill_key`
делает пересечение с 15-минутным проходом безвредным. Состояния между перезапусками нет
нарочно: первый тик читает минуту назад, отставание больше 6000 блоков обрезается — дыры
закрывает 15-минутный проход, а алерт получасовой давности не алерт. На каждом тике — правило
всплеска и пуш подписчикам сразу, дедуп по `hot:{mint}` в `bot_sent`. Проверено вживую: филлы в
базе через ~20 с после блока.

Экономия в `rpc.py`: `head()` отдаёт номер и время блока одним вызовом и запоминает пробу;
короткий диапазон рядом с уже датированным берёт скорость у той пробы вместо второго запроса.
Было 6 запросов на тик, стало 4.

В боте: `/hot` (список всплесков за окно) и пуш `▲ $SYM · burst · +4.2 in 7 min`.

**Всплеск как часть продукта, а не только бота.** Три места:

- `/api/hot` — что горит сейчас и каждый всплеск за окно с тем, что случилось после. Торговому
  движку в первую очередь нужен именно он.
- Сайт: страница `/hot` (то же самое, плюс табло: сколько всплесков, сколько дошли до 2×, сколько
  закончили ниже половины, медиана лучшей цены) и метка `▲ burst` на строках ленты сигналов.
- Дайджест: строка «N bursts · of M old enough to judge, K reached 2x, L ended below half».

Под этим — таблица `bursts` (миграция 17): наблюдатель записывает всплеск в тик, когда тот
сложился, независимо от подписчиков. Потом по ленте читается, что цена сделала после — лучшая
и последняя цена филлов и текущая котировка, всё в единицах цены, которую заплатил последний
вошедший. Так бэктест, выбравший порог, становится живым: через месяц ответ на вопрос «работает ли
эта лента» будет измерен, а не вспомнен.

Цена всплеска — из филлов его собственных участников, не «кто торговал последним»: лох, купивший
через минуту после, — не та цена, о которой алерт.

Наблюдатель называет токен сам, в момент всплеска: первый живой всплеск читался `$0x3adde1`,
токену было 9 минут, а именование идёт раз в 15. Один запрос через тот же lookup, что у сайта.

**Первый живой всплеск — JUGGERNAUT, 16:16 UTC:** 11 кошельков за 8 минут, +7.8, токену 9
минут, unipcs 96 в числе вошедших. К 16:20 — 16 кошельков, +11.1. Записан, поименован, на
странице и в ленте с меткой. Подписчиков у бота по-прежнему ноль, так что пуш никуда не ушёл.

Тестов 179.

**Сессия 16: сутки на API — и утечка, которую они показали.**

**API-дорога держит.** 15 проходов за сутки, 36 кредитов, ни одного отказа, ни одного конфликта
кошельков. Борда 24h каждые два часа приносит по 7–21 новой привязке — трейдеры на ней сменяются, и
каждый приходит с верифицированным адресом. Стало 911 юзеров, 561 с кошельком, 233 из них
верифицированы источником, 86 тезисов. Лента: 5 960 филлов за сутки.

**API-процесс дорос до 2,3 ГБ за 22 часа.** Не маршрут токена и не маршрут трейдера — оба прогнаны
тысячами вызовов в процессе, не сдвинулись. Это `GeckoTerminal()` внутри `candles_for`, на каждый
промах кэша, и это два бага в одной строке. Каждый экземпляр приносил свой лимитер, который поэтому
никогда не видел двух вызовов подряд, — и краулер, гуляющий по страницам токенов (8 375 рендеров за
сутки), получал 429 прямо в страницу. И каждый приносил свой пул соединений, который никто не
закрывал: refcount не спасает httpx-клиент, который сделал хоть один запрос, — пул и соединения
ссылаются друг на друга. Итог: **581 открытое TLS-соединение к Gecko** и память при них.

Починено: один клиент на процесс под локом (и для DexScreener на пути live-lookup тоже), лимитер
берёт лок и держит его через сон — второй поток должен встать в очередь, а не решить, что место
есть. Кэш свечей теперь выкидывает протухшее — раньше просроченная запись не отдавалась, но и не
удалялась. `MemoryMax=1G` на юните: следующая утечка такой формы станет перезапуском в логе, а не
машиной, которая перестала отвечать. После деплоя: 55 МБ, 7 сокетов.

**Побочная жертва — сборщик.** `enrich-tokens` занимал 6,5 минуты из 15-минутного слота: те же
429 от Gecko, спровоцированные API, и бэкофф 15/30/45 с. После починки — 95 секунд. `radar-collect`
теперь укладывается в ~5 минут вместо 10–13.

**Что ещё видно за сутки:** бот с нулём подписчиков — дайджест и здоровье уходят в никуда, нужен
`/subscribe` из своего чата. RPC-лимитер спит 666 с за два часа (90 раз) — это он работает, но один
`holdings` за сутки всё же упёрся в 429 самого RPC; в пределах fail-soft, не трогал.

Тестов 165.

**Сессия 15: сбор переехал с браузера на HTTP.**

**Аккаунт fomo ограничен.** «Account restricted — This account is restricted from using the app».
Ничего хитрого мы не делали — три лидерборда и пара десятков запросов кошельков каждые полчаса, — но
со стороны это ровно то, как выглядит скрапер. Прокси тут не помогает: блок на уровне аккаунта.

Наблюдение шло 80 минут, ничего не трогая: **403 всё это время, без единого просвета**. Это не
временный лимит, который сам отпускает через час, — значит ждать было нечего и переезд был не
преждевременным.

**Перешли на fomoapi.io.** Тот же набор данных по обычному HTTP, без браузера и без аккаунта,
который можно потерять. Две вещи делают эту дорогу дешёвой:

- **Лидерборд стоит 1 кредит и уже несёт верифицированные кошельки** — Solana и EVM прямо в строке.
  Резолвер за 10 кредитов не нужен вообще. Мы выводили кошелёк пересечением: кто торговал тот же
  токен в ту же минуту. Теперь есть чем проверить: **101 совпадение и ни одного расхождения** на
  300 строках. Наш резолвер точен везде, где его вообще можно проверить.
- **Одна страница тезисов — 50 записок по всей цепочке за 5 кредитов.** Раньше тезисы стоили по
  токену и приходили только с той вкладки, на которой стоял браузер.

**Что API не заменяет — ленту.** Их эндпойнт свопов это окно в последние 100 филлов на трейдера,
без пагинации, так и написано в документации. Наша лента — 109 669 филлов, прочитанных с цепочки
бесплатно. Они не конкурируют.

**Первые проходы:** 300 строк, 18 новых юзеров, **134 новые привязки кошельков**, 17 тезисов.
Стало 447 из 831 юзеров с адресом, из них 130 верифицированы источником.

**Бюджет решает расписание.** Бесплатный ключ — 1000 кредитов в месяц, это 32 в день, и два вызова
стоят по-разному: 2 кредита купили 18 трейдеров и 125 кошельков, 5 кредитов — 16 записок. Поэтому
борда 24h каждые 2 часа (`radar-fomo.timer`, 12/день), борда 7d и страница тезисов каждые 8
(`radar-fomo-slow.timer`, 18/день). Итого 30 в день, 900 в месяц.

**Сторож бюджета — не план, а подстраховка.** Месяц считается по `runs`, где каждый проход и так
пишет свою стоимость, — отдельная таблица не нужна. Борды покупаются первыми, тезисы только если
остатка хватает: под давлением деградирует самое дешёвое, а не то, что случайно оказалось последним
перед 402. `cli health` показывает потраченное за месяц отдельной проверкой.

**Браузерный стек выключен, не удалён.** `radar-browser`, `xvfb`, `wm`, `vnc`, `novnc`, `crx` и
сторож. Держал 750 МБ Chrome ради страницы, которую ему больше не дают читать. Возвращается одной
командой — она записана в `deploy/README.md`.

**Два бага в деплое, найденные попутно:**

1. `tar -xzf` поверх каталога добавляет и заменяет, но никогда не удаляет. Файл, удалённый в репо,
   жил на сервере вечно: там до сегодня лежали `pipeline/site.py`, `pipeline/web.py` и
   `tests/test_site.py` — 1165 строк кода, которого нигде больше нет. Из-за этого сервер и локальная
   машина расходились в числе тестов (170 против 163) — и это единственное, что вообще выдало
   проблему. Теперь `update.sh` сверяет распакованное с тем, что лежит, и удаляет лишнее.
2. Юнит-файлы едут в репозитории, а работают из `/etc/systemd/system`, и переносить их приходилось
   руками. `update.sh` теперь обновляет установленные и **называет** те, что приехали, но не
   установлены: запустить юнит — это решение, а не шаг деплоя.

**Проверка здоровья** принимает обе дороги (`kind IN ('fomoapi','fomo_ingest')`) и по-прежнему
требует лидерборд в payload, иначе пустая доставка снова сойдёт за сбор.

Тестов 163 — и на сервере теперь столько же.

**Сессия 14: сторож держал дверь закрытой.**

**Простой 5 часов 20 минут.** Сбор с fomo встал в 20:47 и не возобновлялся до 02:13. Лента с
цепочки при этом шла всё время — её собирает `radar-collect` по RPC, браузер ей не нужен, — так что
замерла только половина: лидерборды, позиции и тезисы.

**Причина — сам сторож.** Он видел молчание и делал ровно то, что было написано: перезапускал
браузер каждые 10 минут. А перезапуск взводит будильник расширения заново, с нуля. Период у
будильника 30 минут. То есть перезапуск на каждом проходе не просто не помогал — он **гарантировал,
что будильник никогда не досчитает до срабатывания**. Сторож своими руками не давал случиться тому,
ради чего существует.

Браузер всё это время был в порядке: залогинен, токен живой, скрипт на странице загружен,
расширение 0.17.0 установлено. Одно сообщение, отправленное в страницу и переданное мостом в service
worker, собрало всё накопившееся разом: три лидерборда, 568 свопов, 31 нового юзера и первые 33
тезиса.

**Починено эскалацией от дешёвого к дорогому** (`browser.collect_now`, `cli browser --collect`):
сначала тычок через мост, и только если следующий проход всё ещё видит тишину — перезапуск. Старый
комментарий в скрипте утверждал, что снаружи в расширение не достучаться, потому что Chrome
отказывает отладчику на extension-таргете. Это правда про extension-таргет и не имеет значения:
страница подключается, а мост был там с самого начала.

**Корневая причина того, почему будильник перестал срабатывать, не найдена.** Правка делает сторожа
работающим, а не будильник надёжным. Если тишина повторится — смотреть надо на MV3 и на то, как
Chrome усыпляет service worker.

**Тезисы поехали.** 33 записи, и содержание оправдывает затею: `ogle` (92) объясняет механику
сжигания PONS каждые 15 минут, `AvgJoesCrypto` (90) пишет про price-to-buybacks 1.8x. Пока все с
одного токена — того, на котором стоит вкладка; следующий сбор возьмёт серверный список из 12.

**Ещё в этой сессии:** вкладка `/exits` на сайте; внешний пинг «мёртвой рукой»
(`radar-heartbeat.timer`, ждёт `HEARTBEAT_URL`); дневной дайджест (`radar-digest.timer`, 18:00);
проверка здоровья и сторож больше не считают пустую доставку за сбор; `.gitattributes` и
нормализация в `update.sh` — на Windows `pathlib.write_text` сам ставит CRLF, и так уехало 60
файлов, из-за чего `install-extension.sh` падал с `set: pipefail: invalid option name`.

Тестов 156.

**Сессия 13: то, что трейдер сказал, и то, что он продал.**

**1. Тезисы приходили к нам всё это время и выбрасывались.** В ответе `/hodlers/top`, который мы и
так запрашиваем, у каждого холдера есть опциональное поле `comment` — записка трейдера к позиции.
`parse_holders` вычитывал pnl, себестоимость, баланс, `isDev` и проходил мимо. Это единственное
поле во всей системе, которое **сказано**, а не выведено из ленты.

Главное было не в парсере. Сборщик видел холдеров **одного** токена — той страницы, на которой
стоит вкладка. Какие токены важны, страница знать не может: нужны баллы. Поэтому ранжирование
осталось на сервере, а список едет обратно **в ответе приёмника на доставку** — расширение этот
ответ и так читало (`deliver()` уже делал `await r.text()`). Ни нового эндпойнта, ни расписания, ни
второго round-trip. `/hodlers/top` принимает массив, так что дюжина имён — один запрос.

Тезисы показываются только от кошельков **с вердиктом**: незаскоренный хэндл с «wagmi» это шум.
Правка тезиса переписывает текст, но не дату: вызов, написанный до движения, — доказательство, те
же слова после — комментарий, и различает их только `first_seen_at`. Миграция 16, расширение 0.17.0.

**2. Сигнал на выход (`analyze.exits`, `/api/exits`, `/exits`).** Мы публиковали только входы, а
лента входов не может показать момент, который стоит денег: токен висит на ней, пока покупка внутри
окна, независимо от того, сидит ли покупатель ещё внутри.

Продажа — не выход. Подрезать десятую часть у победителя это управление позицией, поэтому кошелёк
считается ушедшим, только когда продал **половину** того, что лента видела купленным, — в токенах,
не в долларах, потому что доллары двигаются вместе с ценой. Остаток на цепочке перебивает ленту.
Кошельки, сидевшие в имени до начала нашей ленты, исключены, а не угаданы: размер входа неизвестен,
значит доля выхода неизвестна тоже.

Первый же прогон: **CRUMBS**, который утром стоял в `/fresh` с 22 доверенными покупателями через 3
минуты после открытия пула, к вечеру показал 19 кошельков, вышедших полностью.

**3. Проверка скоринга (`pipeline/calibrate.py`, `cli calibrate`).** 374 вердикта роздано и ни разу
не проверено. Тест вне выборки по построению: `score_history` помнит дату первого вердикта, и
считаются только позиции, открытые **после** неё. Пересчёты игнорируются — пересчёт как раз и есть
момент, когда балл подглядывает в ответ.

```
band      wallets  closed    win   median  realized       all   marked
active         33     125    36%    0.87x     0.88x       225    0.88x
watch         120     678    34%    0.80x     0.85x      1034    0.93x
dropped        95     348    26%    0.62x     0.74x       572    0.84x
```

Порядок по реализованным сделкам верный и подтверждается тремя независимыми мерами. Но **моя же
гипотеза не подтвердилась**: я решил, что все полосы ниже 1.0x потому, что победители остались
открытыми, дописал колонку с оценкой открытых позиций по текущей цене — и порядок сломался, `watch`
обогнал `active`. Балл отделяет плохих от хороших и **не отделяет `active` от `watch`**, а это
ровно то, что мы публикуем как рекомендацию.

Чего не хватает: рыночного бенчмарка. 0.88x само по себе не значит проигрыш рынку. Отчёт печатает
это предупреждение под таблицей. Следующий шаг — считать, что делал сам токен от момента входа.

**4. Дневной дайджест (`pipeline/digest.py`, `/digest`, таймер 18:00).** Пять вещей, меняющих
решение: зашли, купили, вышли, сказали, добавились. Тихий день говорит об этом одной строкой, а не
наряжается в отчёт. На живых данных CRUMBS попал во все три блока сразу — история дня одного токена
в одном сообщении.

**5. Три скрипта деплоя ехали на сервер с CRLF.** `install-extension.sh` падал с
`set: pipefail: invalid option name` — выглядит как баг bash, а это виндовый перевод строки.
`update.sh` уцелел случайно: на сервере он исполняется как heredoc, а не как файл. `.gitattributes`
прибивает всё исполняемое на сервере к LF, `.bat` — к CRLF.

**6. fomoapi.io проверен бесплатным ключом.** `wallets.evm` отдаёт **торговый** кошелёк, не
внутренний аккаунт: 7 из 8 точных совпадений с теми, кого мы связали независимо. Но для шести
хэндлов, которых наш резолв не осилил, пять возвращённых адресов имеют **ноль филлов** в нашей
30-дневной ленте — то есть покупка подписки закрыла бы «285 нерезолвленных» адресами кошельков,
которые на нашей цепочке не торгуют. Шестой вскрыл конфликт, который наш резолвер уже поймал сам и
отказался связывать (`onchain_note = conflict: … already attributed to SimonMHans`).

Где подписка всё же стоит денег: `/v2/token/{addr}/devs` — деплойер и инсайдеры с себестоимостью,
чего у нас нет никакого пути получить. Ончейн-стрим за $599 не нужен: мы читаем ту же цепочку сами.

**7. Отбраковка ботов** оказалась уже сделанной и лучше, чем значилось в плане: `looks_automated`
требует трёх условий сразу, а не двух — частота **и** узость по токенам **и** короткий холд.
Частота сама по себе бота не выдаёт, лучшие ранние входы тоже стреляют сотнями сделок. Поймано двое.

Тестов 151.

**Сессия 11: страницы отвечают из ленты сделок, а не из трёх мешков fomo.**

Пользователь ткнул в две дыры, и обе оказались одной ошибкой: страница отвечала из `fomo_positions`, а там лежат только `topHoldings` — три крупнейших мешка на трейдера из ответа лидерборда.

**1. Страница токена вела с пустой половины.** Лента считала conviction по *покупателям* (13.3 у CME), страница токена — по *держателям* (0.0), и это два разных числа под одним именем. Свежий токен ни у кого не дорос до топ-3, поэтому держателей ноль, хотя 24 доверенных кошелька его набирают. Теперь страница ведёт блоком «кто покупает» (таблица по кошелькам: балл, куплено, продано, когда вошёл) и показывает то же conviction, по которому ранжирует лента. «Кто держит» — вторым блоком, и когда пуст, объясняет почему.

**2. Книга трейдера собирается из ленты.** 26 тысяч филлов за месяц уже знали ответ: свернуть покупки и продажи одного токена в позицию — получается вся книга. У DumbCrayonEater 3 позиции превратились в 30, у unipcs — в 86. Появился блок **«что вернулось обратно»**, отранжированный по реализованному PnL: закрытые целиком и подрезанные, с долей выхода.

Чтобы это стало возможным:
- `sources/rpc.py` пишет `token_amount` — размер лежит в том же логе, который он и так читает, а `decimals` каждого токена берётся одним батч-запросом `eth_call` (кэш на процесс);
- `parse_pair` забирает `priceUsd`, который приходил в том же ответе, что и ликвидность, и выбрасывался. Миграция 11 добавила `tokens.price_usd/price_at`, `enrich-tokens` вторым проходом переспрашивает цену у токенов, в которых лежат чьи-то деньги (`PRICE_MAX_AGE_S`, `PRICE_REFRESH_LIMIT`);
- `analyze.ledger()` и `analyze.book()` — единственное определение позиции; страница, терминал и бот читают его оттуда.

**Чего страница не делает — не выдумывает то, чего не видела.** Кошелёк, продавший больше, чем лента видела купленным, вошёл до нас: «выручка минус вложено» там была бы прибылью из половины записи. Такие имена исключены и посчитаны отдельно («11 further names were left out»), а win rate считается только по позициям, проданным целиком, и показывается от пяти таких сделок.

**Ещё:** «сидит в тех же именах» тоже переехало на ленту — совпадение по трём мешкам почти всегда ноль, по книге у DumbCrayonEater 11 общих имён с unipcs.

**3. Книга оценивается с цепочки, а не по тому, что мы успели увидеть.** Пользователь показал книгу unipcs: 108 имён, из них 39 с ценой, остальные — прочерки. Две причины, обе исправлены.

- **DexScreener почти не индексирует Robinhood Chain.** Замер 2026-09-08: из 30 токенов, которые держат отслеживаемые кошельки, он вернул пары по трём и цену — ни по одному. GeckoTerminal по тем же тридцати ответил на все, и в одном ответе отдаёт `symbol`, `decimals`, `price_usd`, `fdv_usd` и резерв. `/networks/{net}/tokens/multi/{адреса}` теперь первый источник обогащения, DexScreener — запасной для остальных сетей. Цена нашлась у 417 из 434, у 400 из 400, у 393 из 396.
- **Очередь обогащения голодала.** Токен, которого не знает ни один источник, не получал ни имени, ни цены, поэтому попадал в начало очереди (она сортируется по устареванию котировки) и вытеснял оттуда те, у кого цена есть — каждый проход, вечно. Миграция 13 добавила `tokens.checked_at`: штампуется факт запроса, а не факт ответа.

**4. Индексатор остатков (`pipeline/holdings.py`).** `balanceOf` — бесплатное чтение, 40 в один HTTP-раунд. 5019 пар (кошелёк, токен) обошлись в 142 запроса. Это снимает сразу две дыры: позиции, открытые до начала нашей ленты, и филлы, записанные старым источником без размера («UNSIZED»).

Сверка вышла лучше, чем я ожидал: **PROLOGUE у DumbCrayonEater мы теперь оцениваем в $110 932, fomo показывает $110 845** — расхождение 0.08%, и это два независимых пути к одному числу. ICOIN $97.4k против $100.1k, BOW $33.6k против $32.3k. У unipcs MEME был «UNSIZED», стал $1.04M; вся книга — $18.1M.

Что остаток **не** даёт — стоимость входа. Кошелёк, держащий больше, чем лента видела купленным, доплачивал до нас по неизвестной цене, поэтому такие позиции показываются с размером и стоимостью, но без PnL: состояние `held`, прочерк в колонке прибыли. Появилась строка **Book value** — единственная портфельная величина, которой не нужна цена входа.

**5. Страница токена: «кто держит» теперь тоже с цепочки.** Список держателей брался из тех же `topHoldings`, поэтому у всего, кроме нескольких крупных имён, был пуст, а conviction по держателям — ноль. У баланса ограничения «топ-3» нет: в списке каждый отслеживаемый кошелёк, у которого есть хоть сколько-то токена, со количеством и стоимостью. У CME: 24 покупателя и **10 держателей на $94k**, conviction по держателям 5.3 — там, где раньше был текст «пока ни у кого не показано».

**6. График на странице токена — свой, не виджет.** Пользователь спросил про виджет с DexScreener / Gecko / defined.fi. Проверил все три на живом пуле Robinhood Chain:

| | что вышло |
|---|---|
| DexScreener | вечное «Loading pair…» — сеть не индексируется |
| GeckoTerminal iframe | рисует свою панель инструментов и пустой холст |
| defined.fi | вставляет всё своё приложение целиком, со строкой Sign In и баннером «Get the App» |

Зато свечи у GeckoTerminal есть и полные: `/networks/{net}/pools/{pool}/ohlcv/{hour|day}` отдаёт OHLCV с объёмом. Поэтому страница рисует график сама — `site/src/components/Chart.astro`, чистый SVG на сервере, без чужого JS. Заодно он подчиняется тем же правилам, что и остальная страница, а не роняет тёмно-синий виджет на чёрный холст: волосяная сетка, одна ценовая линия, объём на своей базовой линии, переключатель 24h/7d/30d обычными ссылками.

Адрес пула приходит бесплатно в том же ответе, что и цена (миграция 15, `tokens.pool_address`), свечи кэшируются на 5 минут — значит один запрос вверх по течению на всех посетителей. Свеча запуска, растянутая на три порядка, переключает ось в логарифм и подписывает это, иначе всё после неё схлопывается в прямую.

**7. Лента свежих запусков — `/fresh`, четвёртая вкладка.** Лента сигналов ранжирует всё, что доверенные кошельки покупали за сутки, сколько бы они это ни держали. На вопрос «во что они заходят прямо сейчас» она не отвечает. Новая вкладка берёт только те токены, у которых *первая* доверенная покупка попала в окно — вход, а не позиция.

**Метрика — `heat`:** conviction, помноженная на то, насколько рано каждый кошелёк зашёл. Полный вес на запуске, половина через час, десятая часть через десять часов. На токене, который открылся утром, *когда* человек купил — это большая часть того, что его покупка означает: кошелёк с баллом 88, зашедший через четыре минуты, взял другой риск, чем он же на следующий день по графику, который уже все видят. Conviction их не различает.

На живых данных это переставляет страницу: PORT с пятью покупателями через 8 минут после запуска обходит WORTHLESS с шестью через 27.

**Ликвидность — главный фильтр.** На живом суточном окне токен с наибольшим числом доверенных покупателей (17!) имел **$29 ликвидности** — пул уже слили. По головам он бы возглавил страницу. Такие считаются и выносятся под таблицу («36 more had trusted buying, but the pool is drained»), а не выбрасываются молча.

Сейчас на сервере: 40 запусков за сутки, 36 отсеяно. Во главе CME — 24 кошелька, первый через **5 минут** после открытия пула, $224k, ликвидность $264k.

В боте то же самое командой `/fresh`. Пуш по heat — следующий шаг, вся обвязка (подписчики, `bot_sent`, дедуп) уже есть.

**8. Пуш запусков в Telegram включён.** Бот умел отвечать на `/fresh`, но сам не писал — то есть лента, которая стоит больше всего пока ей минуты, доставалась только тем, кто спросил.

Порог взят из живого распределения за сутки на сервере: `heat >= 1.0` — 28 сообщений, `2.0` — шесть, `3.0` — три. По умолчанию **2.0** (`TELEGRAM_MIN_HEAT`): шесть в день читают, тридцать — отключают.

Горячий запуск обычно проходит и по второй ленте, поэтому оба фида описали бы один токен дважды. Дедуп в `bot_sent` и так был по паре (чат, токен), а не по ленте — кто описал первым, тот и сказал; тест это фиксирует.

Подписчиков в базе **0**, отправлено сообщений **0** — включение никого не задело.

**9. Сбор fomo переехал на сервер. Cloudflare пропускает датацентровый IP.**

Главный вопрос, висевший с сессии 9, закрыт: **настоящий Chrome с адреса Contabo открывает fomo.family без челленджа**. Значит ноутбук из схемы уходит — как только браузер на сервере залогинен.

Стоит: Xvfb (:99) + fluxbox + Chrome 152 без headless и без автоматизационных флагов (headless палится в User-Agent, `--enable-automation` ставит `navigator.webdriver` — именно это отбивает вход Google/Apple). Расширение force-installed политикой. Вход по требованию — noVNC через SSH-туннель (`radar-signin.bat`), обе службы поднимаются только на время входа.

Четыре ловушки по дороге, все в `deploy/`:
- `ProtectSystem=strict` делает /tmp read-only → Chrome не создаёт singleton-сокет → `PrivateTmp=yes`;
- `--load-extension` в Chrome 137 стал пустышкой, к 152 исчез и флаг, который это отменял: принимается, виден в `chrome://version`, не делает ничего → CRX + `ExtensionInstallForcelist` с локального update.xml (по `file://` Chrome манифест не берёт — раздаём по loopback, `radar-crx.service`);
- `--disable-extensions-except` выключал ровно то расширение, что поставила политика;
- `chmod 0600` на файле политики: Chrome читает политики от своего пользователя, молча игнорирует нечитаемый файл **и удаляет** расширение, которое тот велел поставить. Одна строка в логе, ничего в UI.

**10. Перенос сессии: доезжает всё, кроме самого входа.**

Сделан канал: дамп в консоли своего браузера → scp → `POST /seed` у приёмника (хранится до одного чтения, потом удаляется) → расширение вписывает в страницу. Транспорт работает, 11 ключей доехали.

**Но логин Privy лежит в HttpOnly-cookies, а `document.cookie` их не отдаёт.** На сервере после переноса: 15 ключей localStorage, из них 6 `privy:` — но это PKCE-состояние (`code_verifier`, `state_code`, `caid`), не токен. Cookies только аналитические (`_ga`, `_fbp`) плюс Cloudflare. `privy:token`/`refresh_token` в localStorage нет ни там, ни у пользователя — значит Privy в cookie-режиме.

Вывод: **консольным дампом сессию не перенести в принципе.** Либо вход руками один раз, либо экспорт cookies тем, кто видит HttpOnly (расширение с правом `cookies`, либо CDP).

**11. Браузером теперь управляем через DevTools, а не клавиатурой.**

`fomo_agent/browser.py` + `cli browser`: спросить страницу и получить ответ, а не скриншот. Родилось из того, что синтез нажатий оказался ровно настолько ненадёжен, как звучит — devtools, которое может не открыться, вставка, которая может не попасть, и фотография для догадок. `websockets` уже есть в extra `[api]`, новой зависимости нет.

`--remote-debugging-port` слушает только loopback и `navigator.webdriver` не ставит.

**12. Вход сделан — сбор fomo идёт с сервера сам.**

Пользователь вошёл через noVNC. Первый же автоматический проход: лидерборды 24h/7d/30d по 150,
**66 новых пользователей**, 25 резолвнутых кошельков, 429 свопов, 1302 позиции (359 новых).
База fomo-юзеров 353 → 419. Дальше каждые 30 минут само.

Регистр не работал из-за раскладки, которую я же и добавил: две группы (`us,ru`) плюс модификатор
переключения ломают маппинг keysym→keycode в x11vnc, и Shift не доезжает. Одна группа `us` + `-xkb`.

**13. Бэкфилл ленты (`pipeline/backfill.py`).** Каждый прочерк в колонке PnL — одна и та же
граница: лента начинается там, где начался трекинг. Граница не фундаментальна, `eth_getLogs`
ответит про любой диапазон — он лишь отказывается от слишком дорогих.

Ширина оказалась не константой, а переговорами: 200k блоков проходят на горячих свежих блоках и
отвечают «log query timed out» неделей раньше. Поэтому отказ = диапазон делится пополам и обе
половины запрашиваются снова, до пола; 429 = пауза и тот же диапазон ещё раз. Идём от свежего к
старому, значит прерванный прогон уже заполнил то, что ближе к сегодня.

**Отдельная ловушка:** `INSERT OR IGNORE` делал повторное чтение бессмысленным — а именно в тех
строках и не хватало размеров (трекер знал цену задолго до того, как научился писать размер).
Теперь поздний проход дописывает только те поля, где `NULL`; чужую запись не перетирает никогда.

**14. Что тихо сломано (`pipeline/health.py`, `/health` в боте, таймер в 07:40).** Каждая поломка
здесь выглядела одинаково снаружи: сайт отдаёт, страницы рисуются, числа стоят. Ничего не падает,
когда протухает сессия fomo или меняется контракт роутера — лента просто становится плоской, а
плоская лента читается как тихий рынок, пока кто-нибудь не посмотрит на даты.

Сторож роутера: `RPC_ROUTERS` — один захардкоженный контракт, и если fomo переедет, филлы исчезнут
без единой ошибки. Отличить «сменили роутер» от «сегодня никто не торговал» можно ровно одним
вопросом — есть ли у кошельков вообще ERC-20 трафик при нулевых филлах. Это и спрашивается, а в
сообщении названа настройка, которую чинить.

**15. Ещё:** `new-tokens` в расписании сбора (жил только в `run`-цикле, который на сервере никто
не запускает); журнал ограничен гигабайтом и месяцем (`deploy/journald/`).

**16. Пересчёт баллов: 304 кошелька, очередь пуста.** 302 в экспорте (новые с последних сборов
плюс просроченные) и ещё 2, доехавшие пока шли партии. Итог по всей базе: **169 active, 153 watch,
52 dropped из 374**, средний балл 77 / 61 / 43 по статусам.

Сдвиг вверх у тех, кого пересматривали, объясняется одним: у большинства теперь видна
себестоимость позиции. Раньше «PnL 1.9M» был числом без опоры, теперь рядом стоит «AI ×71 от
входа в 25k» — и это разные вердикты. Отсюда же и новые понижения: 48 ранних входов у одного
кошелька не спасают, если в книге `PING` списан целиком, а `SAPIEN` потерял две трети — раньше
эта половина картины просто не показывалась.

Флаги ставились скупо и только там, где форма однозначна: `one-hit` — семи, у кого весь результат
это один нерасшифрованный мешок; `bot` — одному (895 филлов по 282 токенам, медиана удержания
6 минут, 67k оборота: дробовик, а не отбор); `wash` — одному (46.6M оборота против книги в 54k).

Партии: `batch1..batch6.json` в scratchpad, `merge.py` сверяет покрытие и схему до отправки —
302 из 302, без дублей и расхождений со списком.

Тестов 132.

**Сессия 10: продукт выехал в интернет. Сайт, API, бот и туннель работают на сервере.**

**Живое прямо сейчас:**
- Сайт — **https://fomoradar.app** (Astro, серверный рендер; голый IP и www редиректят на него)
- Бот — **@fomoradarRH_bot** (поднялся без прокси; блокировка Telegram оказалась чисто провайдерской, в Германии её нет)
- API — `/api/*` и `/docs` через Caddy

**1. Имя продукта: FOMO Robinhood Radar.** Название сети в каждом `<title>`, в описаниях, в шапке, в OpenAPI и в справке бота — это поисковый трафик по «robinhood chain token analyzer». Python-пакет остался `fomo_agent` (переименование задело бы каждый импорт ради невидимого пользователю). CLI отзывается на `fomo-radar` и на старое `fomo-agent`.

**2. Сайт на Astro** (`site/`). Маршруты: лента сигналов, лидерборд с фильтром по вердикту, `/trader/<хэндл>`, `/token/<адрес>`, поиск. Всё рендерится на сервере, значит гуглится и разворачивает превью. Дизайн — GT Planar: чёрный холст, структура из белых волосяных линий, ноль теней и градиентов, цвет только функциональный.

Обогащение, которого просил пользователь («простовато»): **радарная развёртка на живых данных** (азимут = когда вошёл первый доверенный кошелёк, дальность = conviction, сильнейшие в центре, размер точки = число согласных кошельков), список контактов вместо подписей на циферблате, крупная типографика, пульс филлов по часам, гистограмма распределения баллов, панели с угловыми скобками, идентиконы на адрес.

**3. HTTP API** (`fomo_agent/api.py`, FastAPI). Логики внутри нет: маршрут зовёт ту же функцию, что и терминал. Незнакомый токен получает живой lookup в DexScreener и честный ответ `tracked: false`, а не 404.

**4. Telegram-бот** (`fomo_agent/bot.py`, 420 строк, ноль новых зависимостей). Long polling, поэтому работает откуда угодно. Пушит сигнал, когда conviction переваливает порог подписчика, и не шлёт один токен дважды за 12 часов. Текстом принимает адрес токена и хэндл трейдера.

**5. Сервер: Contabo Cloud VPS 4, €5.28/мес, Ubuntu 26.04, Германия.** Пять systemd-юнитов: `radar-api`, `radar-site`, `radar-bot`, `radar-receive`, плюс таймеры `radar-collect` (каждые 15 минут) и `radar-backup` (ночью в 03:20, храню 14 копий). Наружу слушает только Caddy. `ufw` открывает 22/80/443, `fail2ban` включён, автообновления безопасности включены.

**Ubuntu 26.04 приехал с Python 3.14** — на три минорные версии свежее нашего CI. Поэтому деплой прогоняет тесты на сервере: 98 из 98 зелёные и там.

**6. Безопасность.** Пользователь прислал root-пароль в чат. Вход по паролю в SSH выключен целиком (проверено: пароль отбивается), root-пароль сменён на случайный, которого никто не знает. Доступ только по ключу `~/.ssh/fomoradar`.

**7. Туннель для fomo.** Расширение как постило на `127.0.0.1:8787`, так и постит — SSH local forward уводит этот порт на приёмник сервера. Расширение менять не пришлось вообще. Наружу ничего не торчит: приёмник на loopback, дотянуться можно только через туннель по ключу, за ним второй замок — `RECEIVER_TOKEN`. Проверено сквозь: с токеном 200 и запись в базу, без токена 401.

**8. Инфраструктура в репозитории.** `deploy/` — не описание, а копии живых файлов: юниты, Caddyfile, скрипты для Windows. `deploy/update.sh` пакует дерево, заливает, ставит зависимости, **прогоняет тесты на сервере**, пересобирает сайт, перезапускает службы. Базу не трогает, `.env` сохраняет.

**Найденные по дороге баги:** sqlite отказывался закрывать соединение в чужом потоке (веб-фреймворк делает ровно это — были бы случайные пятисотки); `serve --reload` следил за рабочей папкой и перезапускался в цикле от переписываемого WAL; котировочные активы протекали в книгу трейдера; шкала conviction схлопывалась; Caddy не мог писать в свой каталог логов.

**Что осталось — в разделе 5 ниже, он переписан по фактическому состоянию сервера.**

**Сессия 9: Codex больше не нужен для трекинга. Сайт из трёх экранов. Репозиторий готов к публикации.**

**1. Трекинг переехал на публичный RPC Robinhood Chain — бесплатно и без ключа.**

`eth_getLogs` принимает *список* значений для позиции топика. Значит один запрос спрашивает «все Transfer, у которых получатель — любой из этих 302 кошельков», второй — то же по отправителю. **Два запроса покрывают весь ростер**, сколько бы он ни рос, вместо ~1 запроса Codex на кошелёк. Квитанции по найденным сделкам берутся пачками по 40 в один HTTP-раунд.

Заодно выяснилось, как вообще устроена сделка fomo на цепочке 4663:
- Транзакцию отправляет релеер, кошелёк трейдера **никогда не является её `from`** — поэтому наивный поиск по отправителю ничего не находит.
- Каждый филл идёт через один роутер `0xb92fe925dc43a0ecde6c8b1a2709c170ec4fff4f`. Нога кошелька против роутера и даёт направление: пришёл токен — покупка, ушёл — продажа. Это же отсекает аирдропы и переводы, которых в логах кошелька большинство.
- **Ровно один филл на транзакцию** (проверено: 1018 транзакций, во всех по одной ноге), поэтому размер сделки однозначен — это крупнейший прыжок котировочного актива внутри транзакции: USDG, если маршрут в стейбле, иначе WETH по цене с DexScreener.
- Блоки идут раз в ~0.1s. 200k блоков это ~5.6 часа и это **максимальное окно**, дальше эндпоинт отвечает `log query timed out`. Метки времени интерполируются по двум зондам вместо запроса на каждый блок.
- Эндпоинт отдаёт **403 на дефолтный user-agent httpx** — отсюда `RPC_USER_AGENT`.

**Сверка с лентой trenches за то же окно: 209 из 209 филлов совпали по стороне и токену, медианная ошибка в долларах 0.00%.** Полный проход: ~30 бесплатных запросов, 0 из бюджета Codex. `TRACK_SOURCES=rpc,trenches,codex,helius`.

`cli init` теперь показывает **прогноз Codex 3 480/мес из 10 000, из них на трекинг 0** (было ~9 500). Весь остаток — только поиск новых токенов. Резолв кошельков тоже переехал на RPC (`RESOLVE_SOURCES=rpc,codex`): один `eth_getLogs` с фильтром по адресу токена отдаёт всех, кто торговал им в окне. Проверено на unipcs — тот же кошелёк, что у trenches, 11 окон из 12, отрыв 13x.

**2. Найдена и исправлена ошибка в данных: котировочный актив выдавал себя за сигнал.**

USDG — долларовый стейбл Robinhood Chain, через него проходит каждая сделка. Codex пишет своп со стороны пула, то есть «продал токен X за USDG» попадает в базу как **покупка USDG**. Таких строк 3 857 из 25 139. В первой сборке ленты USDG возглавил список сигналов с 66 покупателями. Котировочные активы (`QUOTE_TOKENS` в `sources/rpc.py`) теперь исключены везде: сигналы, лента, таблица токенов, мешки трейдера и счётчик филлов в шапке. После фикса топ ленты осмысленный: SPY 28, SLINK 27, MEME 18, PONS 17.

**3. `pipeline/site.py` — сайт из трёх экранов вместо одного списка.**
- **Signals** — токены, которые за окно купили ≥2 трейдера со скором 60+, отранжированные по числу согласных, рядом лента всех филлов доверенных кошельков.
- **Tokens** — всё, что когорта держит, по нереализованной прибыли, с себестоимостью и кратностью.
- **Traders** — прежний ростер плюс крупнейшие открытые мешки каждого.

Опубликовано по прежней ссылке: https://claude.ai/code/artifact/88b379a4-ddb5-4cc9-bdf6-50db95268ef0. `web.py` оставлен, но `cli page` теперь зовёт `site.py`.

**4. `enrich-tokens` теперь именует и торгуемые токены, а не только удерживаемые** (раньше смотрел только в `fomo_positions`). 1 508 токенов названо за 73 бесплатных запроса; из 1 815 торгуемых адресов известны 1 623.

**5. Репозиторий готов к публикации.** `git init`, ветка `main`, два коммита, LICENSE (MIT), CI на GitHub Actions (pytest на 3.11 и 3.12), README переписан под Robinhood-фокус. Аудит секретов: ключ Codex лежит только в `.env`, который в `.gitignore`; в отслеживаемых файлах ключей нет. `DEEP_MODEL` переведён на `claude-sonnet-5`.

**6. Все 304 трейдера перескорены с учётом открытых позиций.**

В контекст скоринга добавлен блок `open_positions` — пять крупнейших мешков с себестоимостью и кратностью. Это самое прямое доказательство, какое вообще есть: не «сделал миллион», а «PONS 134.5x на входе 68k». В дайджест добавлены колонки `bestX` и `topBag`.

Скоринг прошёл в чате партиями по 25-35 (`score --export` → вердикты → `--import`), файлы `s1..s11.json` в scratchpad. Итог по старым 304: **157 active, 95 watch, 52 dropped** (было 57/194/53). Плюс резолв нашёл **48 новых кошельков** (97 попыток, 55 разрешено, 1 295 бесплатных RPC-запросов), они тоже проскорены — файлы `n1..n2.json`. **Итого 349 проскоренных: 177 active, 120 watch, 52 dropped.** Сдвиг вверх — потому что у 208 из 304 кошельков появилась проверяемая себестоимость, и стало видно, что за цифрой fomo обычно стоит реальный ранний вход, а не один нерасшифровываемый мешок.

Принцип, по которому разводились похожие цифры: несколько выигрышных позиций с настоящей себестоимостью > одна огромная без неё. Отдельно помечены `one-hit` (весь PnL из одного билета) и два бота на Solana (600 сделок за 30д в 6-7 токенах, холд 1-2 минуты).

**7. Найдены и убраны 49 фантомных трейдеров.** При экспорте всплыли кошельки с хэндлом, PnL в миллионы и нулём сделок — на bsc, ethereum и base, которые мы вообще не трекаем. Это `resolve_execution_wallets` продолжал писать в `traders` внутренние адреса fomo, хотя ещё в сессии 6 доказано, что они не торгуют. Функция теперь только аннотирует `fomo_users`. Заодно `needs_review` добавлен в очередь скоринга — без этого статус был тупиком, а не очередью повтора, и эти строки четыре сессии никто не видел.

**8. Дедупликация сделок (миграция v9).** Два источника нумеруют один и тот же филл по-разному (log index против номера в ленте), поэтому одна сделка попадала в базу дважды под разными первичными ключами. Добавлена колонка `fill_key` с уникальным индексом, 66 дублей удалено. Себестоимость позиций больше не может быть отрицательной — проверка перенесена в `upsert_fomo_position`, где её нельзя обойти; 243 старые строки почищены.

**Тесты: 60 (было 30).** Новые: `tests/test_rpc.py` (9) на фикстурах, снятых с живой цепочки, `tests/test_site.py` (7), `tests/test_analyze.py` (7), `tests/test_db.py` (5). Тест `test_the_quote_asset_never_reaches_the_page` и поймал утечку USDG в мешках трейдеров.

**10. Эвристика отбраковки ботов (пункт A.4 из списка работ).** Два кошелька в этой сессии оказались маркет-мейкерами: 600 сделок в 6-7 токенах при холде 1-2 минуты. Частота сама по себе бота не выдаёт — лучшие ранние входы здесь тоже очень быстрые (rizerya: 259 сделок в 100 токенах). Отличает **узость**: все три условия должны сойтись одновременно (`BOT_MIN_TRADES_7D`, `BOT_MAX_TOKENS`, `BOT_MAX_HOLD_MIN`). Проверено на всём ростере: ловит ровно этих двух и ни одного из 300 остальных.

**9. Анализаторы: `cli token <адрес>` и `cli trader <хэндл>`.** Первый отвечает, чьи деньги в токене: кто из ростера держит, по какой себестоимости, кто торговал за окно. Качество держателей считается как сумма (score/100)² — один трейдер на 85 весит больше десяти на 40, потому что кошелёк может завести кто угодно. Второй — вердикт, мешки, свежие филлы и те, кто сидит в тех же именах. Метрика conviction выведена на страницу в таблицу токенов.

**Осталось перед выкладкой на GitHub: ротировать ключ Codex** — он был вставлен в чат.

**Сессия 8: позиции по токенам. Появился анализатор токенов.**

Задача была тянуть `/trades?userId=`, но эндпоинт отвечает **400**: ему обязателен ещё и `tokenAddress`, то есть это позиция в одном токене, а не список. Собирать так пришлось бы по запросу на каждую пару трейдер-токен.

Оказалось не нужно: **`topHoldings` уже лежит в ответе лидерборда**, который мы и так забираем. Три крупнейшие открытые позиции на трейдера с адресом токена, количеством, ценой, стоимостью и PnL. Ноль дополнительных запросов. Парсер `parse_top_holdings`, таблица `fomo_positions` (миграция v8).

Собрано: **872 позиции, 289 трейдеров, 244 токена, 245.7M нереализованного PnL**.

Важная деталь: у части позиций `pnl` больше всей стоимости позиции, то есть он включает и уже вынутую прибыль. Себестоимость тогда восстановить нельзя, и она пишется NULL, а не отрицательным числом — иначе все кратности превращаются в мусор. 245 таких строк.

Названия токенов добирает `cli enrich-tokens` через DexScreener: 226 токенов за 11 запросов, бесплатно, мимо бюджета Codex.

Первая витрина анализатора токенов (кто в чём сидит): PONS — 44 держателя, 56.5M открытой прибыли, 8.8x; AI — 51 держатель, 49.6M, 32.7x; STONK — 65 держателей, 28.4M, 9.1x.

**Сессия 7б: приоритет источников исправлен.** Скоринг сначала шёл по ончейн-потоку, потому что цифра fomo не выводилась в таблицу. Это была ошибка: **PnL с лидерборда fomo — настоящая прибыль в долларах, включая открытые позиции.** Вход на 5k в токен, который сделал 500x, это миллионы на бумаге и ноль реализованного; ончейн-поток такого не показывает, а накапливающий трейдер всегда выглядит убыточным. Правило зафиксировано в `SYSTEM` и `EXPORT_INSTRUCTIONS` в `pipeline/score.py`: fomo PnL — главный сигнал, ончейн-поток — только проверка на вменяемость.

Перескорены все 224 трейдера с цифрой fomo. Итог: **57 active, 194 watch, 51 dropped** (было 13/117/174). Страница пересобрана, `fomo 30d` показывается как основная метрика.

Также сюда же: `score --export --digest N --offset M` печатает таблицу для скоринга, и **колонка fomoPnL в ней теперь первая** — именно её отсутствие и привело к ошибке.

**Сессия 7: база выросла втрое, все проскорены, страница обновлена.**
- 184 кошелька разрешено из fomo-лидерборда, **182 из них нет у trenches**. Трекаемых робинхудовских трейдеров **302** против 108 заимствованных.
- Все **304 трейдера проскорены** через чат: 13 active, 117 watch, 174 dropped. Партии: `scored_b1..b3.json`.
- Страница пересобрана и опубликована: https://claude.ai/code/artifact/88b379a4-ddb5-4cc9-bdf6-50db95268ef0
- `score --export --digest N --offset M` печатает компактную таблицу для скоринга в чате.
- Найден конфликт атрибуции (`SerAvocado` получил кошелёк `SimonMHans`) — добавлена защита: адрес, за который уже поручился другой источник, не переписывается, а помечается конфликтом.
- Точность резолвера на пересечении: **41 из 42**. Из 182 найденных кошельков 178 реально торгуют.

**Замечание по скорингу новых.** У кошельков из fomo нет готовой статистики trenches (реализованный PnL, винрейт), поэтому судить пришлось по нашим ончейн-агрегатам: разница между проданным и купленным за 30 дней, число сделок, токенов, время удержания. Это грубее: покупатель, который набирает позицию, выглядит как убыточный. В сводках это оговорено, но уверенность у таких вердиктов ниже (0.35–0.55 против 0.6–0.85 у trenches-трейдеров).

**Кандидат на замену Codex найден и проверен.** У Robinhood Chain есть публичный RPC без ключа: `rpc.mainnet.chain.robinhood.com`. Проверено: `eth_chainId` возвращает 0x1237 (4663), `eth_getLogs` отдаёт трансферы по адресу. То есть трекинг можно перевести на бесплатный источник, написав индексатор логов Transfer (~200 строк) плюс цены из GeckoTerminal. Blockscout отпадает: 403 на своём хосте, 402 на общем.

**Сессия 6: расширение проверено вживую и решена главная задача — вычисление настоящих кошельков.**

Расширение работает: собрало 285 уникальных трейдеров fomo (3 лидерборда по 150) и 4835 свопов. Но обнаружилось, что **все адреса, которые отдаёт fomo, — внутренние**. Проверено против Codex: у `address`, `evmAddress`, `swap.recipient` и `trade.userAddress` ноль ончейн-событий, тогда как у настоящего кошелька того же трейдера их сотни.

**Решение: `pipeline/resolve.py`.** Fomo сообщает, каким токеном человек торговал и в какую секунду. Все, кто торговал этим токеном в ту же минуту, — подозреваемые. Повторяем на 12 токенах и взвешиваем: редкое окно на 3 участника весит 1/3, толкучка на 200 — 1/200. Побеждает тот, кто набрал больше и чаще. Приёмка двойная: минимум 3 попадания И (отрыв по весу ≥1.4 ИЛИ вдвое больше попаданий, чем у второго).

**Точность измерена на живых данных: 27 из 27** совпадений с независимым списком trenches, ноль ошибочных адресов. Из 49 попыток резолв удался в 40 (82%), из них **13 кошельков, которых у trenches нет вообще**.

Также: `pick_tracker` теперь учитывает адрес. У trenches есть только их 108 кошельков, поэтому для найденных нами адресов источник прозрачно переключается на Codex (`Trenches.covers()`).

Цифры: 285 пользователей fomo известно, 40 разрешено, **253 ждут** (нужны новые прогоны расширения), робинхудовских трекаемых трейдеров 128 против 108 у конкурента.

Стоимость: ~11 запросов Codex на трейдера. Разрешить оставшиеся 253 обойдётся примерно в 2 800 запросов разово, при месячном лимите 10 000 и текущем фоне 3 480.

**Сессия 5: первая публичная функция готова.**
- Все **110 трейдеров проскорены** через чат (`SCORER=manual`, модель `manual:claude-opus-5`): 11 active, 33 watch, 66 dropped. Файлы вердиктов: `scored.json`, `scored_rest.json`.
- `pipeline/web.py` + команда `page` — собирает автономную HTML-страницу из базы. Опубликована: https://claude.ai/code/artifact/88b379a4-ddb5-4cc9-bdf6-50db95268ef0
- **Решение пользователя: фокус только на Robinhood Chain.** `DEX_CHAINS=robinhood`. Код остался мультичейновым, сузились только дефолты. Прогноз Codex упал до ~3 480/мес.
- Принцип скоринга, зафиксировать: считается **реализованный** PnL. Нереализованные марки на открытых мешках не доказательство, сколько бы их ни было. Высокий винрейт при отрицательном итоге хуже низкого при положительном — значит, режут прибыль и держат убытки.

### Отложено, обсуждено с пользователем
1. **Сайт с лентой сигналов** — когда ≥2 active-трейдера покупают один токен в течение часа. Данные уже есть (`/api/tape` + скоры). Это второй экран и главный продукт.
2. **Донабор трейдеров сверх чужих 110** — расширение даёт лидерборд fomo по 150 записей на окно (24h/7d/30d), то есть до ~450 уникальных против 108 у trenches. Это и есть путь роста базы.
3. **Самостоятельный парсинг fomo** — расширение для этого и написано, осталось проверить его в живом Chrome.

**Сессия 4 (вторая половина): расширение Chrome + локальный приёмник.** Пользователь решил, что данные fomo нужны любой ценой ради маркетинга. Вместо подделки TLS-отпечатка (ломкая и нечестная) сделан честный путь: запросы делает сам браузер.
- `extension/` — MV3-расширение. Скрипт в MAIN-world перехватывает токен из запроса приложения и дёргает эндпоинты **страничным `fetch`**, то есть запросы неотличимы от собственных запросов приложения. Bridge в ISOLATED-world связывает его с service worker, тот по будильнику шлёт собранное на локальный приёмник. Попап: эндпоинт, токен, интервал, число кошельков за прогон, «Collect now», «Forget resolved».
- `fomo_agent/receiver.py` + `cli receive` — HTTP на 127.0.0.1:8787, `POST /ingest` кладёт payload через тот же `import_browser_export`, `GET /health` показывает объём. Есть общий секрет `RECEIVER_TOKEN`, CORS для расширения, запись каждого приёма в `runs`.
- Расширение помнит уже разрешённые UUID и не тратит на них прогоны.
- **Не проверено вживую:** само расширение в Chrome. Приёмник покрыт тестами (`tests/test_receiver.py`, 4 штуки, поднимают настоящий сервер на свободном порту).

**Сессия 4: подключён robinhoodtrenches.com.** Чужой открытый API (без ключа, отвечает серверно) индексирует 108 отобранных трейдеров fomo на Robinhood Chain. Он отдаёт готовую связку «хендл → исполняющий кошелёк», ту самую, ради которой мы бились с Cloudflare, плюс посчитанные PnL, винрейт и время удержания. Что сделано: источник `sources/trenches.py`, discovery `discover --trenches`, трекинг первым в `TRACK_SOURCES`, статистика в контекст скоринга, команда `trenches` для здоровья. Живой прогон: 108 трейдеров импортировано, трекинг 40 кошельков стоит **1 HTTP-запрос вместо 105 к Codex**. Прогноз бюджета Codex упал с 9 480 до **3 720** в месяц.

**Сессия 3: фаза 0 по fomo закрыта, но с оговоркой.** Эндпоинты сняты из HAR, адаптер и парсеры написаны и покрыты тестами на настоящих ответах. Две находки, обе меняют планы:
1. **Серверные запросы к fomo невозможны.** Cloudflare режет любой не-браузерный клиент на входе: 430 `{"error":"unauthorized"}`, воспроизведено даже точной командой cURL из Chrome со свежим валидным токеном. ТЗ запрещает агрессивный обход, поэтому данные fomo приходят через экспорт из браузера: `scripts/fomo_export.js` → `cli fomo-import`. Плюс токен Privy живёт ровно час, так что автоматический опрос всё равно был бы нежизнеспособен.
2. **fomo торгует не с тех адресов, что в профиле.** Подробности ниже.

**Сессия 2: Helius больше не нужен.** Codex умеет отдавать историю сделок кошелька на бесплатном плане, причём с USD по каждой сделке и на всех трёх сетях. Скоринг работает без `ANTHROPIC_API_KEY` через экспорт/импорт в чат. Пайплайн сквозной: свежий токен → его покупатели → сделки → скор → отчёт.

## 0. Как запустить и проверить

```bash
.venv/Scripts/python -m pytest -q                     # 23 теста, все офлайн
.venv/Scripts/python -m fomo_agent.cli page --out radar.html   # публичная страница из базы
.venv/Scripts/python -m fomo_agent.cli init           # ключи, источники, прогноз бюджета Codex
.venv/Scripts/python -m fomo_agent.cli new-tokens --dry-run
.venv/Scripts/python -m fomo_agent.cli discover --mint <mint> --makers   # покупатели токена → кандидаты
.venv/Scripts/python -m fomo_agent.cli track --address <wallet> --show
.venv/Scripts/python -m fomo_agent.cli run --once
```

- Python 3.11, venv в `.venv/`, пакет установлен через `pip install -e .`. На Windows перед живыми прогонами ставь `PYTHONIOENCODING=utf-8`.
- Bash-хередоки с одинарными кавычками здесь ломаются; правки делай через Write/Edit или python-скрипт из scratchpad.
- Не git-репозиторий. `.gitignore` готов: `.env`, `*.db`, `.venv`, captures, `pending_scores*.json`.

## 1. Ключи и внешние сервисы

| Сервис | Переменная | Статус | Заметки |
|---|---|---|---|
| Codex (данные defined.fi) | `CODEX_API_KEY` | **есть, проверен вживую** | Almost Free: 1$ разово, 10 000 запросов/мес, 5 rps. Теперь несёт три функции: новые токены, discovery трейдеров, трекинг сделок. Ключ светился в чате, перевыпустить перед публикацией. |
| Anthropic | `ANTHROPIC_API_KEY` | нет, **не блокирует** | без него `SCORER=auto` переключается в manual: скоринг идёт через чат. |
| Helius | `HELIUS_API_KEY` | нет, **не блокирует** | у пользователя истёк план. Бесплатный тариф у Helius бессрочный: 1M кредитов/мес, Enhanced Transactions стоит 100 кредитов = ~10k вызовов/мес. Можно завести заново, но необходимости нет. |
| fomo.family | — | **только экспорт из браузера** | Cloudflare блокирует серверные вызовы (430), токен Privy живёт 1 час. Рабочий путь: `scripts/fomo_export.js` в консоли → `cli fomo-import <файл>`. `FOMO_SESSION` намеренно пуст. Непрерывный discovery делает Codex. |
| DexScreener, GeckoTerminal | без ключа | работают | 60 rpm и ~30 rpm. |
| robinhoodtrenches.com | без ключа | **работает, подключён** | чужой индексатор fomo-трейдеров на Robinhood Chain. `TRENCHES_MIN_INTERVAL_S=900`. Может исчезнуть в любой момент — падает мягко. |
| Telegram | `TELEGRAM_*` | не начато | фаза 4, опционально. |

### Что доступно на бесплатном плане Codex (проверено запросами)

| Запрос | Доступ | Для чего |
|---|---|---|
| `filterTokens` | **да** | свежие токены с серверными фильтрами |
| `getTokenEvents` | **да** | сделки по токену → его покупатели (discovery) |
| `getTokenEventsForMaker` | **да** | история сделок кошелька (трекинг) |
| `filterWallets` | нет, `NOT_AUTHORIZED` | лидерборд кошельков по PnL — был бы прямой заменой fomo |
| `detailedWalletStats` | нет | готовые PnL/winrate по кошельку |
| `balances` | нет | балансы кошелька |

## 2. Бюджет Codex — следить обязательно

10 000 запросов в месяц, это узкое место всей системы. `init` печатает прогноз по текущему конфигу и предупреждает при превышении. Текущий расклад (~9 480/мес):

| Статья | Формула | В месяц |
|---|---|---|
| Новые токены | 1 запрос / `CODEX_MIN_INTERVAL_S` (900 с) | 2 880 |
| Discovery покупателей | `DISCOVER_TOKENS_PER_PASS` (3) на новые токены | ~600 |
| Трекинг кошельков | только те цепи, что не покрыты бесплатным источником | 0 |

Robinhood-кошельки ушли на trenches, поэтому Codex остаётся только на Solana и Base. `init` теперь считает это по реальному составу базы.

Дефолты интервалов подняты специально: со старыми (60 с на трекинг) квота сгорала за 7 часов.

## 3. Что сделано

### Скелет (фаза 1) — готово
`config.py` (всё через `.env`), `db.py` (sqlite, миграции по `user_version`, сейчас **v3**: `tokens.chain`, `trades.chain`), `models.py` (pydantic + `norm_addr` + `QUOTE_DECIMALS`), `ratelimit.py`, `cli.py` (typer).

### Триггер новых токенов (фаза 2а) — готово, проверено вживую
Мультичейн `DEX_CHAINS=solana,base,robinhood`. Три источника в `pipeline/new_tokens.py::fetch_new_tokens`, дедуп по (сеть, адрес). Фильтры в `sources/filters.py`: mcap 500k–1B, ликвидность ≥10k, возраст ≤24 ч.

| Источник | Что видит |
|---|---|
| `codex` | основной, ~126 из 137 токенов в прогоне, серверные фильтры + доли снайперов/бандлеров |
| `geckoterminal` | `trending_1h`, `trending_6h`, `top_volume`; фид `new` отключён (пыль) |
| `dexscreener` | только токены с профилем/бустом |

### robinhoodtrenches.com — **новое, проверено вживую**
`sources/trenches.py`. Эндпоинты без авторизации: `/api/traders` (108 кошельков + PnL, винрейт, лучшая и худшая сделка), `/api/tape` (лента заливок, максимум 500, пагинации нет — параметры игнорируются, всегда отдаёт свежие), `/api/closed` (закрытые позиции с `pnl_pct` и `hold_seconds`), `/api/tokens`, `/api/overview`, `/api/status`.

- Трекинг: `Trenches` реализует протокол `Tracker`, лента кэшируется, поэтому проход по N кошелькам стоит один запрос.
- Только Robinhood Chain (4663) и только их выборка из 108 кошельков.
- Статистика кладётся в `traders.stats_json` (миграция v6) и попадает в контекст скоринга блоком `indexer_stats`.
- `robots.txt` без запретов, но ходим раз в 15 минут со своим User-Agent.

### Discovery трейдеров без fomo (фаза 1/2) — **новое, проверено вживую**
`pipeline/discover.py::discover_makers` → `Codex.token_makers(mint, chain)`: берёт последние свопы по токену, агрегирует кошельки по объёму покупок, отбирает тех, кто купил больше `DISCOVER_MIN_BUY_USD` (500$), пишет как `candidate` с `source=makers:<mint>`. Живой прогон: 192 кошелька по токену, 2 прошли фильтр. `poll_new_tokens` сам запускает это для `DISCOVER_TOKENS_PER_PASS` самых крупных новых токенов.

### Ончейн-трекинг (фаза 2б) — **новое, проверено вживую**
`pipeline/track.py` переписан на выбор источника по цепи, `TRACK_SOURCES=codex,helius`:

- **Codex** (`sources/codex.py::maker_events` + `parse_maker_event`): все сети, сторона сделки из `eventDisplayType`, USD из `priceUsdTotal`, SOL из raw-amount по `QUOTE_DECIMALS`. Token-to-token свопы пропускаются. Живой прогон: 600 сделок по одному кошельку.
- **Helius** обёрнут в `HeliusTracker`, Solana-only, включается сам при наличии ключа.
- Кошельки, чью сеть никто не поддерживает, считаются в `unsupported`.
- Порядок обхода: least-recently-tracked first, срез `TRACK_MAX_WALLETS_PER_PASS`.

### Скоринг (фаза 3) — **работает без API-ключа**
`SCORER=api|manual|auto` (auto = api при наличии ключа, иначе manual).

- **api**: как раньше, Haiku по умолчанию, `--deep` Sonnet, retry → `needs_review`. **Вживую не проверялся, ключа нет.**
- **manual**: `score --export pending_scores.json` пишет контексты + инструкции + JSON-схему; модель в чате читает файл и выдаёт массив результатов; `score --import results.json --model-label "manual:<модель>"` валидирует через тот же `ScoreResult` и пишет в БД и `score_history`. Формат ответа: `docs/example_scores.json`. **Проверено сквозняком**, кошелёк-бот получил score 15 / dropped.
- В `run` шаг score в manual-режиме просто обновляет файл экспорта.

### Отчёт и цикл (фаза 4) — базовая версия
`report` (топ active, новые, dropped, покупки за сутки с `**SIGNAL**` при ≥2 кошельках), `run [--once]` с записью каждого шага в `runs` и мягкими ошибками.

### fomo (фаза 0) — **сделано, кроме сессии**
`docs/fomo-endpoints.md` заполнен из HAR (314 запросов). `sources/fomo.py` реализован: реальные пути, троттлинг 1 req/s, кэш, 401/403/**431** → `FomoSessionExpired`. Парсеры покрыты тестами на фикстурах из настоящих ответов.

**Как теперь заходят данные fomo.** `scripts/fomo_export.js` вставляется в консоль DevTools на fomo.family: перехватывает токен из запроса приложения, тянет лидерборды за 24h/7d/30d, разрешает исполняющие кошельки топ-25 трейдеров, при открытой странице токена забирает холдеров, и скачивает JSON. Дальше `cli fomo-import <файл>` прогоняет нетронутые payload-ы через те же парсеры. Обновлять руками пару раз в неделю.

**Ключевая находка (пункт 4 фазы 0).** Адрес в профиле fomo — не тот, с которого идут сделки. У `frankdegods` профиль `A5SEXYJY…`, а свопы идут с `923mtHov…` на Solana и `0x3e98397d…` на Robinhood. Узнать исполняющий кошелёк можно только через `/v2/users/{id}/swaps`. Поэтому:
- лидерборд и холдеры складываются в новую таблицу `fomo_users` по UUID;
- `resolve_execution_wallets` делает по запросу на пользователя и только тогда заводит строку в `traders`, по одной на цепь;
- трекинг всегда идёт по исполняющему адресу.

Инструменты: `scripts/parse_fomo_har.py` (декодирует base64, чинит обрезанный HAR, маскирует секреты), `scripts/fomo_session_from_curl.py` (кладёт сессию в `.env`, не печатая её), команды `fomo-check` и `fomo-resolve`. `scripts/capture_fomo_endpoints.py` починен, но упирается в Google-блок и оставлен как запасной.

### Тесты
`tests/test_resolve.py` — 5 тестов на логику вычисления кошелька (вес окон, пороги приёмки, разбор свопов на ноги).
`tests/test_receiver.py` — 4 теста на локальный приёмник (реальный сервер на loopback: приём, CORS, отбраковка мусора, общий секрет).
`tests/test_parsers.py`, 19 штук, все офлайн: **trenches (трейдеры, заливки, отбраковка)**, **импорт браузерного экспорта (идемпотентность, адреса, цепи)**, **fomo (лидерборд, холдеры, исполняющие адреса)**, helius (4 кейса), dexscreener, geckoterminal, codex-токены, **codex maker-события (buy/sell/EVM/отбраковка)**, кросс-источниковый дедуп, **round-trip ручного скоринга**, схема ScoreResult, БД.

## 4. Что нужно от пользователя

Блокеров не осталось, всё работает. По порядку важности:

0. **Перевыпустить ключ Codex** на dashboard.codex.io и вписать новый в `.env` — старый был вставлен в чат, а репозиторий готов к публикации. После этого `gh repo create` и пуш.
1. **Поставить расширение** (`chrome://extensions` → Developer mode → Load unpacked → папка `extension/`) и запустить `cli receive`. Дальше данные fomo идут в базу сами, пока открыта вкладка fomo.family. Инструкция: `extension/README.md`. Ручной путь через `scripts/fomo_export.js` остаётся запасным.
2. `ANTHROPIC_API_KEY`, если надоест скорить через чат.
3. Решить, поднимать ли план Codex: `filterWallets` дал бы готовый лидерборд прибыльных кошельков и снял бы нужду в fomo вообще.

## 5. Фронт работ, по приоритету

Переписано 2026-09-08 по фактическому состоянию сервера. Старый список устарел: половина
пунктов про Codex, ключ которого отозван, а трекинг и сигналы уже сделаны.

### Блокеры — без них продукт медленно протухает

- [ ] **Браузер на сервере не залогинен в fomo.** Всё остальное стоит и работает: Chrome,
      расширение, приёмник, Cloudflare пропускает. Не хватает одного входа руками —
      `radar-signin.bat`, раскладка починена (`us,ru`, Alt+Shift), пароль можно вставить из
      буфера, 2FA с телефона. Профиль хранит сессию, Privy сам обновляет токен, так что это
      разово. Перенос сессии дампом не поможет: логин в HttpOnly-cookies (см. п.10).
      Пока не сделано — не обновляются лидерборд, `pnl30d` и `topHoldings`.
- [ ] **Скоринг руками.** `ANTHROPIC_API_KEY` на сервере не стоит, поэтому новые кошельки
      висят без балла, пока их не прогонишь через `score --export` → чат → `--import`.
      Сейчас неоцененных 3 из 352, но это потому, что ростер не пополнялся 45 часов.
      Решение: либо ключ на сервер (тогда `score` встаёт в таймер), либо принять ручной цикл
      и добавить в бот команду «сколько ждёт оценки».
- [ ] **Сторож роутера.** `RPC_ROUTERS` захардкожен одним контрактом. Сменит его fomo — филлы
      просто станут нулём, и это никак не заметно: страница не пустеет, она замирает.
      Нужна проверка «за сутки ноль филлов при живых трансферах» → лог + сообщение в бот.

### Ближайшее, делается без пользователя

- [ ] **`new_tokens` не в расписании.** `radar-collect` гоняет resolve → track → enrich →
      holdings; открытие новых токенов последний раз было 23 часа назад. Добавить в юнит.
- [ ] **74 нерезолвленных fomo-юзера.** Кошельки известны, адрес не сматчен — каждый это
      трейдер, которого нет в продукте. Резолв бесплатный по RPC; упирается в порог
      уверенности (`resolve_min_ratio`), стоит посмотреть на отбракованных вручную.
- [ ] **Отбраковка ботов до скоринга.** Медианный холд < 5 минут и > 200 сделок за неделю —
      ставить `dropped` эвристикой. Экономит скоринг и чистит лидерборд.
- [ ] **Бэкфилл ленты глубже.** Окно RPC — 5.6 часа на запрос, история берётся кусками назад.
      Это то, что закроет прочерки в колонке PnL: сейчас позиция, открытая до начала нашей
      ленты, показывает размер и стоимость без прибыли (состояние `held`).
- [ ] **Дневной дайджест в бот.** `report` последний раз бежал 4 дня назад и ни в каком
      таймере не стоит. Одно сообщение в сутки: что зашло, что вышло, кто появился.
- [ ] **Логи в файл с ротацией** и внешний пинг на `/api/health` (сейчас про падение узнаём
      только открыв сайт).

### Позже

- [ ] **Chrome под Xvfb на сервере** — пропустит ли Cloudflare датацентровый IP. Если да, дома
      можно ничего не держать. Если нет, вкладка остаётся на ноутбуке, и это единственная
      неавтоматическая часть.
- [ ] **Полная книга из fomo** (`/v2/users/{id}/balances`). Сильно подешевела после
      индексатора остатков: размер и стоимость позиции мы теперь берём с цепочки. Осталась
      ценна только ценой входа для позиций старше нашей ленты.
- [ ] Домен → одна строка в Caddyfile + `PUBLIC_SITE_URL` и `API_CORS_ORIGINS`.
- [ ] GitHub: `fomo-robinhood-radar`, баннер и логотип в SVG, README под маркетинг, скриншоты.
      **Пользователь делает это последним, публичным запуском.**
- [ ] `SKILL.md`: примеры запросов, формат вывода, режим ручного скоринга в чате.
- [ ] Solana через публичный RPC — только если вернём Solana в фокус.

### Сделано и вычеркнуто из старого списка

Трекинг через RPC, лента сигналов, пуш в Telegram, свежие запуски (`heat`), книга трейдера из
ленты, индексатор остатков, цены через GeckoTerminal, график на странице токена, сайт, API,
бот, сервер, туннель. Пункты про Codex закрыты вместе с ключом.

## 6. Архитектурные решения, которые не надо пересматривать без причины

- fomo — только discovery, и уже не единственный: `discover_makers` покрывает ту же задачу через Codex.
- Эндпоинты fomo не выдумываются, только из дампа фазы 0.
- Пороги в `config.py`/`.env`, не в коде.
- Источники (токенов и трекинга) независимы и падают мягко: `fetch_new_tokens` и `build_trackers` ловят исключения.
- Бюджет Codex — жёсткое ограничение. Любой новый вызов сначала проверяется против прогноза в `init`.
- Только чтение. Никаких приватных ключей, никакой торговли.
