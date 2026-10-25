"""F2: a tiny API that answers in JSON, like most systems you'll connect to.

Run it:   uv run uvicorn status_api:app --app-dir foundations/f02-apis-json --port 8090
Try:      curl -i localhost:8090/stations/seattle
          curl -i localhost:8090/stations/atlantis
          curl -i localhost:8090/admin/reset
          curl -i -H "X-Api-Key: letmein" localhost:8090/admin/reset
"""

from fastapi import FastAPI, Header, HTTPException

app = FastAPI(title="Weather station API (demo)")

STATIONS = {
    "sydney": {"city": "Sydney", "temperature_c": 24, "raining": False, "wind_kmh": 9},
    "london": {"city": "London", "temperature_c": 11, "raining": True, "wind_kmh": 22},
    "seattle": {"city": "Seattle", "temperature_c": 9, "raining": True, "wind_kmh": 14},
}


@app.get("/stations/{name}")
def station(name: str):
    if name.lower() not in STATIONS:
        raise HTTPException(status_code=404, detail=f"no station called {name}")
    return STATIONS[name.lower()]


@app.post("/admin/reset")
@app.get("/admin/reset")
def reset(x_api_key: str = Header(default="")):
    if x_api_key != "letmein":
        raise HTTPException(status_code=401, detail="you need a valid API key for this")
    return {"reset": True}
