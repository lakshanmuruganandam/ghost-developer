from fastapi.testclient import TestClient
from src.main import app
import pytest

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "ghost-developer"}

def test_github_webhook():
    payload = {
        "action": "opened",
        "issue": {
            "id": 12345,
            "number": 42,
            "title": "Fix the AST parser bug",
            "body": "The parser is dropping async functions.",
            "state": "open"
        }
    }
    response = client.post("/webhook/github", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "accepted"
    assert "dispatched for issue #42" in response.json()["message"]

def test_github_webhook_ignored_action():
    payload = {
        "action": "closed",
        "issue": {
            "id": 12345,
            "number": 42,
            "title": "Fix the AST parser bug",
            "state": "closed"
        }
    }
    response = client.post("/webhook/github", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": "Ignored action"}
