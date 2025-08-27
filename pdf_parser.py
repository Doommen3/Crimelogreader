import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List

import pandas as pd

try:
    import pdfplumber
except ImportError as exc:  # pragma: no cover - handled at runtime
    raise SystemExit("pdfplumber is required to run this script") from exc


@dataclass
class ColumnSpec:
    name: str
    start: float
    end: float


def group_rows(words, y_tolerance=3):
    rows = []
    current_y = None
    current_words: List[dict] = []

    for w in sorted(words, key=lambda w: (w["top"], w["x0"])):
        if current_y is None or abs(w["top"] - current_y) <= y_tolerance:
            current_words.append(w)
            current_y = w["top"] if current_y is None else (current_y + w["top"]) / 2
        else:
            rows.append(current_words)
            current_words = [w]
            current_y = w["top"]
    if current_words:
        rows.append(current_words)
    return rows


def assign_columns(words, columns: List[ColumnSpec]):
    row = {c.name: [] for c in columns}
    for w in words:
        x = w["x0"]
        for c in columns:
            if c.start <= x < c.end:
                row[c.name].append(w["text"])
                break
    return {k: " ".join(v).strip() for k, v in row.items()}


def parse_pdf(pdf_path: Path, column_specs: List[ColumnSpec]) -> pd.DataFrame:
    rows = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            word_rows = group_rows(page.extract_words())
            for r in word_rows:
                rows.append(assign_columns(r, column_specs))
    return pd.DataFrame(rows)


def main(argv=None):
    argv = argv or sys.argv[1:]
    if len(argv) < 2:
        raise SystemExit("Usage: pdf_parser.py <pdf> <output_csv>")
    pdf_file = Path(argv[0])
    out_csv = Path(argv[1])

    columns = [
        ColumnSpec("case_number", 0, 90),
        ColumnSpec("date", 90, 170),
        ColumnSpec("offense", 170, 340),
        ColumnSpec("location", 340, 520),
        ColumnSpec("disposition", 520, float("inf")),
    ]

    df = parse_pdf(pdf_file, columns)
    df.to_csv(out_csv, index=False)


if __name__ == "__main__":  # pragma: no cover
    main()
