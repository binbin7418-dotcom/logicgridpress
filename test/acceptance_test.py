#!/usr/bin/env python3
"""LogicGridPress acceptance test: generate a real 6-puzzle book and
assert every puzzle is proven unique from its clues alone, clues are
all true, clue counts are in a sane band, PDF structure is right, and
generation is deterministic for a fixed seed."""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from logic_grid_press import build_book, generate_puzzle, verify_puzzle
import random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond)))
    print(f"[{'PASS' if cond else 'FAIL'}] {name} {detail}")


def main():
    t0 = time.time()
    rng = random.Random(11)
    sigs = []
    for _ in range(2):
        p = generate_puzzle(4, random.Random(11))
        sigs.append(sorted(c["text"] for c in p["clues"]))
    check("generation is deterministic for a fixed seed", sigs[0] == sigs[1])

    s = build_book(6, OUT, seed=7, houses=4)
    check("book PDF written", os.path.getsize(s["pdf_path"]) > 5000,
          f"{os.path.getsize(s['pdf_path'])} bytes")
    counts = [r["clues"] for r in s["puzzles"]]
    check("clue counts in sane band (5-16)", all(5 <= n <= 16 for n in counts),
          f"counts {counts}")
    check("every puzzle verified unique-from-clues",
          all(r["unique_solution"] and r["verified"] for r in s["puzzles"]))
    check("page count = 2 + 2*6", s["pages"] == 14, f"got {s['pages']}")

    from pypdf import PdfReader
    r = PdfReader(s["pdf_path"])
    check("PDF reopens with 14 pages", len(r.pages) == 14)
    mb = r.pages[0].mediabox
    check("page size 612x792", float(mb.width) == 612 and float(mb.height) == 792)

    # one 5-house expert puzzle, generated and verified end-to-end
    p5 = None
    rng5 = random.Random(3)
    for _ in range(30):
        p5 = generate_puzzle(5, rng5)
        if p5:
            break
    ok, why = verify_puzzle(p5) if p5 else (False, "no puzzle")
    check("5-house expert puzzle generates + verifies unique", ok,
          f"clues={len(p5['clues']) if p5 else 0} {why}")
    print(f"(total {time.time() - t0:.1f}s)")
    failed = [x for x in results if not x[1]]
    print(f"\n{len(results) - len(failed)}/{len(results)} PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
