from fastapi.testclient import TestClient

from app.cases.loader import loader
from app.main import app


def test_cases_load():
    cases = loader.list_cases()
    assert len(cases) >= 3
    assert all(c.truth for c in cases)


def test_public_api_does_not_leak_truth():
    client = TestClient(app)
    response = client.get("/api/cases")
    assert response.status_code == 200
    payload = response.json()
    assert payload
    assert "truth" not in payload[0]
    assert "alibi_claim" in payload[0]
