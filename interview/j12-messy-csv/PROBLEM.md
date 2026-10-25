# J12 practice: clean a messy meter-reading export

You get `meters.csv` from a client. Write `clean(path)` that returns a list of clean readings:
`{"meter_id": "M-001", "date": "2026-10-01", "kwh": 120.5, "site": "Warehouse A"}`

Rules the client confirmed:
1. Meter IDs are case-insensitive (`m-001` is `M-001`).
2. Dates come as `YYYY-MM-DD` or US `MM/DD/YYYY`. Store them as `YYYY-MM-DD`.
3. A row with a missing or non-numeric reading, or an impossible date, is rejected, not guessed.
4. An exact duplicate (same meter, same date, same reading) is kept once.
5. Return the rejected rows too, each with a reason, so they can go back to the client.

Talk while you code: say your assumptions out loud, and test the weird rows first.
