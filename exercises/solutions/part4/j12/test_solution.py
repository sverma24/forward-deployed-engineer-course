from pathlib import Path

from solution import clean

good, rejected = clean(Path(__file__).parent / "meters.csv")


def test_negative_reading_rejected():
    assert any(r[2] == "negative reading" and r[1]["meter_id"] == "M-006" for r in rejected)
    assert all(g["kwh"] >= 0 for g in good)
