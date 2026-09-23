#!/usr/bin/env python3
"""Perform dependency-free structural checks on the project files."""

from __future__ import annotations

import ast
import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = (
    "DTEK0042_Exercise_2.ipynb",
    "DTEK0042_Exercise_3.ipynb",
    "DTEK0042_Exercise_4_FINAL.ipynb",
)
DATA_FILES = {
    "ECG_800hz.txt": (None, 1),
    "PPG_record.txt": (",", 4),
    **{f"dataset/Noisy_data_{index}.txt": (None, 3) for index in range(1, 5)},
    **{f"dataset/Normal_data_{index}.txt": (None, 3) for index in range(1, 5)},
}


def validate_notebooks() -> None:
    for relative_path in NOTEBOOKS:
        path = ROOT / relative_path
        with path.open(encoding="utf-8") as notebook_file:
            notebook = json.load(notebook_file)

        if notebook.get("nbformat") != 4:
            raise ValueError(f"{relative_path}: expected notebook format 4")

        for cell_number, cell in enumerate(notebook.get("cells", [])):
            if cell.get("cell_type") != "code":
                continue
            source = "".join(cell.get("source", []))
            try:
                ast.parse(source, filename=f"{relative_path}:cell-{cell_number}")
            except SyntaxError as error:
                raise SyntaxError(
                    f"{relative_path}: code cell {cell_number} is invalid"
                ) from error

        print(f"validated notebook: {relative_path}")


def fields(line: str, delimiter: str | None) -> list[str]:
    if delimiter is None:
        return line.split()
    return next(csv.reader([line], delimiter=delimiter))


def validate_data() -> None:
    for relative_path, (delimiter, expected_columns) in DATA_FILES.items():
        path = ROOT / relative_path
        row_count = 0
        with path.open(encoding="utf-8", newline="") as data_file:
            for row_count, line in enumerate(data_file, start=1):
                values = fields(line, delimiter)
                if len(values) != expected_columns:
                    raise ValueError(
                        f"{relative_path}:{row_count}: expected "
                        f"{expected_columns} columns, found {len(values)}"
                    )
                try:
                    numeric_values = [float(value) for value in values]
                except ValueError as error:
                    raise ValueError(
                        f"{relative_path}:{row_count}: non-numeric value"
                    ) from error
                if not all(math.isfinite(value) for value in numeric_values):
                    raise ValueError(
                        f"{relative_path}:{row_count}: non-finite value"
                    )
        if row_count == 0:
            raise ValueError(f"{relative_path}: file is empty")
        print(f"validated data: {relative_path} ({row_count:,} rows)")


if __name__ == "__main__":
    validate_notebooks()
    validate_data()
    print("repository validation passed")
