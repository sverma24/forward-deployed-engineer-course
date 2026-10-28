"""J12 your turn, solved: a meter can't use negative energy, so reject negative readings with a reason."""

import csv
from datetime import datetime


def parse_date(text):
    for fmt in ("%Y-%m-%d", "%m/%d/%Y"):
        try:
            return datetime.strptime(text.strip(), fmt).date().isoformat()
        except ValueError:
            pass
    return None


def clean(path):
    good, rejected, seen = [], [], set()
    with open(path, newline="") as f:
        for n, row in enumerate(csv.DictReader(f), start=2):        # line 1 is the header
            meter = row["meter_id"].strip().upper()
            date = parse_date(row["reading_date"])
            try:
                kwh = float(row["kwh"])
            except ValueError:
                kwh = None
            if date is None:
                rejected.append((n, row, "impossible or unknown date"))
            elif kwh is None:
                rejected.append((n, row, "missing or non-numeric reading"))
            elif kwh < 0:
                rejected.append((n, row, "negative reading"))
            elif (meter, date, kwh) in seen:
                # Keep the first copy, but still report the repeat: nothing is dropped silently.
                rejected.append((n, row, "exact duplicate of an earlier row (first one kept)"))
            else:
                seen.add((meter, date, kwh))
                good.append({"meter_id": meter, "date": date, "kwh": kwh, "site": row["site"].strip()})
    return good, rejected


if __name__ == "__main__":
    good, rejected = clean("meters.csv")
    for g in good:
        print("OK      ", g)
    for n, row, why in rejected:
        print(f"REJECTED line {n}: {why}: {dict(row)}")
