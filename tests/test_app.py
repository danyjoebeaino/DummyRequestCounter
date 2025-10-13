import os
import app.app as app_module
from fastapi.testclient import TestClient
import fakeredis

def test_root_returns_200(monkeypatch):
    # use a fake in-memory Redis instead of a real server
    fake = fakeredis.FakeRedis()
    monkeypatch.setattr(app_module, "redis", fake)

    # optional: make sure the app uses a predictable host/port in case other code reads env
    os.environ["REDIS_HOST"] = "fake"
    os.environ["REDIS_PORT"] = "6379"

    client = TestClient(app_module.app)
    r = client.get("/")
    assert r.status_code == 200
    assert "Hello" in r.text
    # call again to ensure the counter increments
    r2 = client.get("/")
    assert "visited 2" in r2.text
