"""F5: use a package someone else wrote (httpx) to call the F2 weather API.

Start the API first (see foundations/f02-apis-json/status_api.py), then:
  uv run python foundations/f05-python-basics/weather_check.py seattle
"""

import sys

import httpx

city = sys.argv[1] if len(sys.argv) > 1 else "seattle"
reply = httpx.get(f"http://localhost:8090/stations/{city}")
if reply.status_code == 200:
    data = reply.json()
    print(f"{data['city']}: {data['temperature_c']} °C, raining: {data['raining']}")
else:
    print(f"The API said {reply.status_code}: {reply.json()['detail']}")
