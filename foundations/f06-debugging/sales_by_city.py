"""F6: this script has a bug. Run it, read the error, find the line.

Run:  uv run python foundations/f06-debugging/sales_by_city.py
"""

import csv
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
FILE = Path(__file__).parent / "sales.csv"


def load(path):
    with path.open() as f:
        return list(csv.DictReader(f))


def total(rows):
    result = 0
    for row in rows:
        result += int(row["amount"])
    return result


rows = load(FILE)
logging.info("loaded %d rows from %s", len(rows), FILE.name)
print("Total sales:", total(rows))
