import csv
from pathlib import Path
from typing import Iterable


class CSVWriter:
    @staticmethod
    def write(path: str, rows: Iterable[dict]) -> None:
        rows = list(rows)
        if not rows:
            return

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)