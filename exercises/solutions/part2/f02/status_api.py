"""F2 your turn, solved: add Toronto, and a /stations address that lists every station name.

Run:  uv run uvicorn status_api:app --app-dir exercises/solutions/part2/f02 --port 8091
Try:  curl -s localhost:8091/stations   and   curl -s localhost:8091/stations/toronto
"""

from fastapi import FastAPI, HTTPException

app = FastAPI(title="Weather station API (exercise solution)")

STATIONS = {
    "sydney": {"city": "Sydney", "temperature_c": 24, "raining": False, "wind_kmh": 9},
    "london": {"city": "London", "temperature_c": 11, "raining": True, "wind_kmh": 22},
    "seattle": {"city": "Seattle", "temperature_c": 9, "raining": True, "wind_kmh": 14},
    "toronto": {"city": "Toronto", "temperature_c": 4, "raining": False, "wind_kmh": 18},
}


@app.get("/stations")
def all_stations():
    # Declared before /stations/{name} reads more clearly, though FastAPI matches the exact path either way.
    return {"stations": sorted(STATIONS)}


@app.get("/stations/{name}")
def station(name: str):
    if name.lower() not in STATIONS:
        raise HTTPException(status_code=404, detail=f"no station called {name}")
    return STATIONS[name.lower()]
