"""F5 your turn, solved: also count the orders per city."""

import csv
from pathlib import Path

ORDERS = Path(__file__).resolve().parents[4] / "foundations" / "f03-spreadsheets-to-sql" / "orders.csv"


def summary_by_city(rows):
    totals, counts = {}, {}
    for row in rows:
        amount = int(row["quantity"]) * int(row["price_each"])
        totals[row["city"]] = totals.get(row["city"], 0) + amount
        counts[row["city"]] = counts.get(row["city"], 0) + 1
    return totals, counts


with ORDERS.open() as f:
    totals, counts = summary_by_city(list(csv.DictReader(f)))

for city in sorted(totals, key=lambda c: -totals[c]):
    n = counts[city]
    print(f"{city:8} ${totals[city]:<4} from {n} order{"s" if n != 1 else ""}")
