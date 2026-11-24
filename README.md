# THE DAY'S DISPATCH

Monday 23 November 2026 — the whole day on one page: 13 large cards,
29 shorter lines, a numbered map, the day in numbers and a date check.
Lead story: fourteen missing after the Kyiv strike, Zelenskiy says.

## Run

- `python3 compose.py` — draws the page, duels two layouts at small
  size, and keeps the stronger one as `entry.png`.
- `python3 main.py` — copies `entry.png` into the folder named by
  MAKEFUN_OUTPUT_DIR (default `out`).
- `python3 test_entry.py` — checks size, dimensions and fresh words.
