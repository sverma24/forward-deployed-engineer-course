-- C5 your turn, solved: closed outages that lasted more than 12 hours,
-- which is when the compensation policy starts paying.
SELECT outage_id, area_code, started_at, restore_eta,
       ROUND((julianday(restore_eta) - julianday(started_at)) * 24, 1) AS hours
FROM outages
WHERE status = 'closed' AND restore_eta IS NOT NULL
  AND (julianday(restore_eta) - julianday(started_at)) * 24 > 12
ORDER BY hours DESC;
