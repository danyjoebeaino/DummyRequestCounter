import os
import sys
import fakeredis
from fastapi.testclient import TestClient

# Add project root to sys.path before importing app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import app.app as app_module  # noqa: E402


def test_root_returns_200(monkeypatch):
    """Test FastAPI root endpoint using fake Redis."""
    # use a fake in-memory Redis instead of a real server
    fake = fakeredis.FakeRedis()
    monkeypatch.setattr(app_module, "redis", fake)

    # ensure app uses predictable env vars for tests
    os.environ["REDIS_HOST"] = "fake"
    os.environ["REDIS_PORT"] = "6379"

    client = TestClient(app_module.app)
    r = client.get("/")
    assert r.status_code == 200  # nosec
    assert "Hello" in r.text  # nosec

    # call again to ensure the counter increments
    r2 = client.get("/")
    assert "visited 2" in r2.text  # nosec
