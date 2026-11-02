# LogicGridPress

Build print-ready **logic grid (zebra) puzzle books for Amazon KDP** where every puzzle is *proven* — by an independent solver, from its clues alone — to have exactly one solution.

## Why

A logic grid puzzle with two solutions is a broken product: the solver reaches a fork the clues can't settle, and your book gets the review. Generators that print a solution grid without ever re-solving from the clues ship those forks. LogicGridPress makes proof part of generation:

1. A random solution grid is drawn.
2. True clues are collected and added until a backtracking solver finds **exactly one** solution.
3. Each clue is then trial-removed; clues that aren't needed are dropped (a minimal clue set — no padding).
4. Before the book is written, every puzzle is **re-solved from its clue list alone**; the unique answer must equal the generated grid, and every clue must be true in it.

## Use

**App (Windows):** launch `LogicGridPress.exe`, choose the puzzle count, houses (4 = classic, 5 = expert) and a seed, click **Build the book**. Output: `logic_grid_book.pdf` in a `logicgridpress_out` folder — title page, puzzle pages (solving grid + numbered clues), then full solution tables. 8.5×11in (612×792pt).

**Command line:** `python logic_grid_press.py out/ --puzzles=20 --houses=4 --seed=42`

A 6-puzzle sample book is included (`sample_book.pdf`).

## Details

- Clue types: same house, not same house, somewhere-left, immediately-left, next-to, and house-position clues — all phrased in plain English ("The coffee drinker is immediately to the left of the dog owner.")
- Theme: Maple Street — names, house colors, drinks, pets, and (for 5-house puzzles) hobbies
- Deterministic: same seed, same book
- Generation time: roughly 3–4 seconds per 4-house puzzle (the proof is the product); a 20-puzzle book takes about a minute

## Verified

Acceptance test (8/8 PASS, `test/acceptance_results.txt`): a 6-puzzle book shipped with 10–12 minimized clues per puzzle, every puzzle re-solved from clues alone to exactly one solution; a 5-house expert puzzle verified with 19 clues; PDF exactly 14 pages at 612×792pt; generation deterministic.

## Scope

Built-in theme only in this version. Clue sets are minimized greedily — every remaining clue is necessary, though a different minimal set may also exist. 100% local.

## Build from source

`pip install pyinstaller reportlab`, then `pyinstaller logicgridpress.spec`. Or push to GitHub and let the included Actions workflow build the Windows package.
