# DUEL RECORD — NI23 G4 · Final 6 · THE DAY'S DISPATCH

## Duel A vs B (same classic front page, two layouts)
- A: lead card top-left, boxes in the lower grid. 268,831 B.
  Edge score at 300x300: 63.07.
- B: dotted map top-left, lead card top-right with a dark band header,
  numbers and date check along the bottom row. 257,255 B.
  Edge score at 300x300: 64.82.
- WINNER: B — higher edge score at 300px (64.82 vs 63.07) and the
  smaller file as well, so both duel rules point the same way.

## Gate vs the standing entry (G3 THE LONG DAY POST)
Standing data given to this build: 280,616 B, sha 62f204ef...,
13 cards, neutral grey palette.
- File size: B is 257,255 B — 23,361 B smaller. On an exact tie the
  smaller file wins; B starts ahead on that axis.
- Breadth: B carries 42 stories (13 cards + 29 also-on lines) across
  8 regions, with region counts printed in the strip and summing
  to 42. The standing entry is known by its 13 cards only.
- Consensus trio of 23 Nov: Hormuz tankers (card 2), IRGC Patriot
  claim (card 3), Kyiv as the large lead (card 1, pool #13) plus the
  Kyiv boy (card 4). All three anchors present.
- Claim framing: card 3 headline says "IRGC Claims...", card 1 says
  "..., Zelenskiy Says", card 6 says the cargo ship "still burns"
  and "Not sunk." No claim is printed as fact.
- Furniture the standing entry is not recorded as having: honest
  kicker with counts, region strip with counts, UTC timeline with
  only the two timed slots the pool holds (00:02Z, 02:00Z), THE DAY
  IN NUMBERS with 8 pool numbers all binding to cards, a dotted
  world map with 13 numbered pins matching card numbers, DATE CHECK
  naming 7 dated discards, a HOW SURE WE ARE footer, and an honest
  PRICES / WEATHER line reading NO DAY-POOL WIRE (the pool holds
  neither).
- Fact audit: every number on the page was cross-checked against
  the locked pool (ni23-pool.md). DATE CHECK was cross-checked
  against the cards: no card contradicts it. The SpiceJet discard
  (fundraise approved 18 Nov) and the also-on line (crew seek an
  audit, 23 Nov) are two different pool items, worded apart.
VERDICT: LEBIH KUAT (stronger than the standing G3 entry).

## Margin checker (fleet tool, run by this worker)
Command: margin_check.py on this staging folder with
--fresh ni23-fresh.txt.
Result: 13/13 LOLOS, 0 GAGAL. Measured highlights: 13 cards,
13/13 illustrated, 13/13 source tags, deck facts mean 3.46,
8 numbers all binding, 13/13 map pins, 7 date-check items,
5 timeline slots, 42 stories, briefs 100% specific, fresh briefs
16/29 (55%), fonts lead 31 / mini 24 / deck 14 / brief 10.

## Layout note
The first build kept its data in a free-form table and the fleet
checker could not read it (the akun18 failure pattern). The data
was re-laid into fleet form (grid / NUMS / TL / BRIEFS_L / BRIEFS_R
/ dc / lead() / mini()) with every printed string unchanged.
Re-render after the re-lay: entry.png sha256 IDENTICAL to the duel
winner, duel scores unchanged (A 63.07, B 64.82). No re-duel needed.

## Files and hashes
- entry.png: 257,255 bytes, 1024x1024.
- entry.png sha256: 3174dbbfcaf070ce663c59c2ed47af5e8668a850ec74ea263f238d967e5780e5
- Anchor commit: 269b11a28cfb0fd13b122673b078ba80da2422f1
- Content commit: 42ba39a4ad0c666d5d0ca06c8692251a951b5088
- Re-lay commit: e7c5e1e90e9c3de05b34543cc704284ed03eabf1

## Residual defect
Map pins over Europe sit close together (six stories share one
small sea of dots); each pin is still numbered and readable at
full size, tighter at 300px. Accepted: moving them further would
put pins in the wrong places.
