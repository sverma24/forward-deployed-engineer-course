from pathlib import Path

from solution import clean

good, rejected = clean(Path(__file__).parent / "meters.csv")


def test_ids_are_normalised():
    assert {g["meter_id"] for g in good} == {"M-001", "M-002"}


def test_us_dates_are_converted():
    assert {"meter_id": "M-002", "date": "2026-10-01", "kwh": 98.0, "site": "Office, Floor 2"} in good


def test_duplicate_kept_once():
    assert sum(1 for g in good if g["meter_id"] == "M-001" and g["date"] == "2026-10-02") == 1


def test_bad_rows_rejected_with_reasons():
    reasons = sorted(r[2] for r in rejected)
    assert reasons == ["exact duplicate of an earlier row (first one kept)", "impossible or unknown date",
                       "missing or non-numeric reading", "missing or non-numeric reading"]
