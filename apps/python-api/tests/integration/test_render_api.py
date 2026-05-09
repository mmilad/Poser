import json
from pathlib import Path

import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from poser.api.app import app


def test_validate_and_render_endpoints():
    payload = json.loads(Path("tests/fixtures/scenes/minimal_scene.json").read_text())
    client = TestClient(app)

    r1 = client.post("/v1/validate-scene", json=payload)
    assert r1.status_code == 200
    assert r1.json()["valid"] is True

    r2 = client.post("/v1/render", json=payload)
    assert r2.status_code == 200
    body = r2.json()
    assert "job_id" in body
    assert body["manifest"]["seed"] == 1234
