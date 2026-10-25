from fastapi.testclient import TestClient

from status_api import app

client = TestClient(app)


def test_known_station():
    assert client.get("/stations/seattle").json()["city"] == "Seattle"


def test_unknown_station_is_404():
    assert client.get("/stations/atlantis").status_code == 404
