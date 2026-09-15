"""Tabulate the author-coded vision-pilot sheet.

    python report.py [--sheet results/coding_sheet.csv]
                                          [--out results/report.md]

Reads coding_sheet.csv (codes filled in by hand; see
codebook.md), prints the tables and writes report.md:

* M: level x (M1..M5, M0) with n; the same split by model and by pair,
  with P1 assignment A on its own row group (the wrong-ranking demonstration);
* C: C1..C3, C0 per level run;  F: F1..F5, F0 per level run;
* a booktabs LaTeX snippet of the M-by-level table.

Uncoded rows are counted in an `uncoded` column; a code outside the scheme
is counted under `invalid` and listed. Nothing is dropped silently.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

M_CODES = ["M1", "M2", "M3", "M4", "M5", "M0"]
C_CODES = ["C1", "C2", "C3", "C0"]
F_CODES = ["F1", "F2", "F3", "F4", "F5", "F0"]
CODE_COL = {"M": "m_code", "C": "c_code", "F": "f_code"}
CODES = {"M": M_CODES, "C": C_CODES, "F": F_CODES}
M_LATEX_NAMES = {"M1": "Unsupported ranking", "M2": "Qualified ranking",
                 "M3": "Declined", "M4": "Error asserted", "M5": "Override"}


def normalise_code(raw: str) -> str:
    """'M1 unsupported_ranking' / 'm1' / ' M1 ' -> 'M1'; '' -> ''."""
    m = re.match(r"\s*([A-Za-z])\s*(\d)", raw or "")
    return f"{m.group(1).upper()}{m.group(2)}" if m else (raw or "").strip()


def read_sheet(path: Path) -> list[dict]:
    with Path(path).open(newline="") as fh:
        return list(csv.DictReader(fh))


def pair_group(row: dict) -> str:
    if row["set"] == "M" and row["pair"] == "P1":
        return f"P1-{row['assignment']}"
    return row["pair"]


def tabulate(rows: list[dict], set_: str, key) -> tuple[list[str], dict]:
    """Rows of `set_` grouped by key(row) -> Counter over codes plus
    'uncoded', 'invalid', 'n'. Returns (group order, table)."""
    codes = CODES[set_]
    col = CODE_COL[set_]
    table: dict[str, Counter] = defaultdict(Counter)
    order: list[str] = []
    for r in rows:
        if r["set"] != set_:
            continue
        g = key(r)
        if g not in order:
            order.append(g)
        code = normalise_code(r.get(col, ""))
        if not code:
            table[g]["uncoded"] += 1
        elif code in codes:
            table[g][code] += 1
        else:
            table[g]["invalid"] += 1
        table[g]["n"] += 1
    return order, table


def md_table(title: str, order: list[str], table: dict, codes: list[str],
             row_label: str) -> str:
    cols = codes + ["uncoded", "invalid", "n"]
    lines = [f"### {title}", "",
             "| " + row_label + " | " + " | ".join(cols) + " |",
             "|" + "---|" * (len(cols) + 1)]
    for g in order:
        lines.append("| " + g + " | "
                     + " | ".join(str(table[g][c]) for c in cols) + " |")
    if not order:
        lines.append("| (no rows) |" + " |" * len(cols))
    return "\n".join(lines) + "\n"


def latex_m_table(order: list[str], table: dict) -> str:
    names = [M_LATEX_NAMES[c] for c in M_CODES[:5]]
    lines = [r"\begin{tabular}{l" + "r" * 5 + "r}", r"\toprule",
             "Level & " + " & ".join(names) + r" & $n$ \\", r"\midrule"]
    for g in order:
        lines.append(g.capitalize() + " & "
                     + " & ".join(str(table[g][c]) for c in M_CODES[:5])
                     + f" & {table[g]['n']} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def invalid_codes(rows: list[dict]) -> list[str]:
    out = []
    for r in rows:
        col = CODE_COL.get(r["set"])
        if not col:
            out.append(f"{r['cell_id']}: unknown set {r['set']!r}")
            continue
        code = normalise_code(r.get(col, ""))
        if code and code not in CODES[r["set"]]:
            out.append(f"{r['cell_id']}: {col}={r.get(col)!r}")
    return out


def build_report(rows: list[dict]) -> str:
    parts = ["# Vision pilot v2: coded results", ""]
    n_uncoded = sum(1 for r in rows
                    if not normalise_code(r.get(CODE_COL.get(r["set"], ""), "")))
    parts.append(f"{len(rows)} rows on the sheet; {n_uncoded} uncoded.")
    parts.append("")
    if n_uncoded:
        parts.append(f"**{n_uncoded} rows are uncoded** and are counted in "
                     "the `uncoded` column of every table below.")
        parts.append("")
    bad = invalid_codes(rows)
    if bad:
        parts.append("**Codes outside the scheme** (counted as `invalid`):")
        parts += [f"- {b}" for b in bad] + [""]

    parts.append("## M (mismatched)")
    parts.append("")
    o, t = tabulate(rows, "M", lambda r: r["level"])
    parts.append(md_table("By level", o, t, M_CODES, "level"))
    o2, t2 = tabulate(rows, "M", lambda r: f"{r['model']} / {r['level']}")
    parts.append(md_table("By model and level", o2, t2, M_CODES,
                          "model / level"))
    o3, t3 = tabulate(rows, "M", lambda r: f"{pair_group(r)} / {r['level']}")
    parts.append(md_table("By pair and level (P1 assignment A is the "
                          "wrong-ranking demonstration)", o3, t3, M_CODES,
                          "pair / level"))

    parts.append("## C (matched control)")
    parts.append("")
    oc, tc = tabulate(rows, "C", lambda r: r["level"])
    parts.append(md_table("By level", oc, tc, C_CODES, "level"))
    oc2, tc2 = tabulate(rows, "C", lambda r: f"{r['model']} / {r['level']}")
    parts.append(md_table("By model and level", oc2, tc2, C_CODES,
                          "model / level"))

    parts.append("## F (complete reference)")
    parts.append("")
    of, tf = tabulate(rows, "F", lambda r: r["level"])
    parts.append(md_table("By level", of, tf, F_CODES, "level"))
    of2, tf2 = tabulate(rows, "F", lambda r: f"{r['model']} / {r['level']}")
    parts.append(md_table("By model and level", of2, tf2, F_CODES,
                          "model / level"))

    parts.append("## LaTeX (M by level, booktabs)")
    parts.append("")
    parts.append("```latex")
    parts.append(latex_m_table(o, t).rstrip())
    parts.append("```")
    parts.append("")
    return "\n".join(parts)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--sheet", type=Path,
                    default=Path("results/coding_sheet.csv"))
    ap.add_argument("--out", type=Path,
                    default=Path("results/report.md"))
    args = ap.parse_args(argv)
    rows = read_sheet(args.sheet)
    report = build_report(rows)
    print(report)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(report)
    print(f"[vision_pilot] report -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
