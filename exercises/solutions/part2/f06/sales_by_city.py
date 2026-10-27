"""F6 your turn, solved: sale 5 has the letter O instead of a zero ("1O0").
Log every row that isn't a whole number, with the reason, and skip it."""

import csv
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
FILE = Path(__file__).parent / "sales.csv"


def total(rows):
    result = 0
    for row in rows:
        raw = row["amount"].strip()
        try:
            result += int(raw)
        except ValueError:
            logging.warning("sale %s has amount %r, which isn't a whole number; skipping it", row["sale_id"], raw)
    return result


with FILE.open() as f:
    rows = list(csv.DictReader(f))
logging.info("loaded %d rows", len(rows))
print("Total sales:", total(rows))
