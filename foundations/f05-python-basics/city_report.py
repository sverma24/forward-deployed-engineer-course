"""F5: a small Python script: read a CSV, add things up in a function, print a report.

Run:  uv run python foundations/f05-python-basics/city_report.py
"""

import csv
from pathlib import Path

ORDERS = Path(__file__).parent.parent / "f03-spreadsheets-to-sql" / "orders.csv"


def total_by_city(rows):
    totals = {}
    for row in rows:
        amount = int(row["quantity"]) * int(row["price_each"])
        totals[row["city"]] = totals.get(row["city"], 0) + amount
    return totals


with ORDERS.open() as f:
    orders = list(csv.DictReader(f))

for city, total in sorted(total_by_city(orders).items(), key=lambda kv: -kv[1]):
    print(f"{city:8} ${total}")
