"""Summarize a local CSV file as deterministic JSON."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import TextIO


def summarize_csv(path: Path) -> dict[str, object]:
    if not path.is_file():
        raise ValueError(f"input is not a regular file: {path}")

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, strict=True)
        columns = reader.fieldnames
        if columns is None:
            raise ValueError("CSV header is required")
        if any(not column for column in columns):
            raise ValueError("CSV header names must be non-empty")
        if len(columns) != len(set(columns)):
            raise ValueError("CSV header names must be unique")

        missing = {column: 0 for column in columns}
        row_count = 0
        for row in reader:
            if None in row:
                raise ValueError("CSV row has more fields than the header")
            row_count += 1
            for column in columns:
                if row[column] in (None, ""):
                    missing[column] += 1

    return {"columns": columns, "missing": missing, "row_count": row_count}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path, help="local UTF-8 CSV file")
    return parser


def run(argv: list[str] | None = None, *, stdout: TextIO, stderr: TextIO) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = summarize_csv(args.csv_file)
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        print(f"csv-summary: {exc}", file=stderr)
        return 2
    print(json.dumps(result, sort_keys=True, separators=(",", ":")), file=stdout)
    return 0


def main() -> int:
    return run(sys.argv[1:], stdout=sys.stdout, stderr=sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())
