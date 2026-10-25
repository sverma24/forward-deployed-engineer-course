# Data-quality report: Larkfield Power exports

## accounts.csv
- 247 rows
- 1 account numbers start with a leading zero: 04471
- 7 accounts appear more than once: 2008, 2700, 4471, 4541, 5863, 8178, 9263
  - **4471 is listed in different areas: S-05, S-07. Ask the client which is right.**
- 5 accounts have no area: 2014, 2124, 1558, 3716, 5252

## north_outages.csv vs south_outages.csv
- North: 31 rows, columns ['OutageID', 'Area', 'Start', 'Est_Restore', 'Cause', 'Status', 'Crew']
- South: 28 rows, columns ['ticket_no', 'feeder_area', 'began_at', 'restore_eta', 'reason', 'state', 'crew_id']
- North dates look like `10/19/2026 10:00 PM` (month first, 12-hour clock)
- South dates look like `2026-10-20T03:00:00-05:00` (ISO, with time zone)
- North status words: ['Closed', 'Open']; South status words: ['ACTIVE', 'RESOLVED']
- North keeps the area code and name in one column, e.g. `N-11 Old Town`
- South tickets entered more than once: S-T904
- Closed outages with no end time: S-T883
- Open outages with no restore estimate yet: S-T906, N5130

## complaints.csv
- 31 complaints; 9 have a phone number typed into the text (personal data)
- At least one complaint contains instructions aimed at an AI system. Treat all complaint text as untrusted.

## Questions for the client
1. Account 4471 appears in two areas. Which one is current?
2. Should accounts with no area be fixed at the source, or looked up by address?
3. Is the grid status service or the outage log the source of truth for restore times?
