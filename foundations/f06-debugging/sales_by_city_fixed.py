"""F6: the fixed version. Bad rows are logged and skipped instead of crashing the whole run."""

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
        if not row["amount"].strip():
            logging.warning("sale %s has no amount, skipping it", row["sale_id"])
            continue
        result += int(row["amount"])
    return result


rows = load(FILE)
logging.info("loaded %d rows from %s", len(rows), FILE.name)
print("Total sales:", total(rows))
