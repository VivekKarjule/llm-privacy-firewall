import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")
from fastapi.testclient import TestClient
from src.proxy import app, _sessions

client = TestClient(app)
PROMPT = "Summarize the record, SSN 123-45-6789, email a.b@x.com."


def post(**kw):
    body = {"prompt": PROMPT, "strategy": "regex", "backend": "mock"}
    body.update(kw)
    return client.post("/chat", json=body)


def test_secret_never_leaves_but_user_gets_it_back():
    r = post().json()
    assert "123-45-6789" not in r["sanitized_prompt"]
    assert "a.b@x.com" not in r["sanitized_prompt"]
    assert "123-45-6789" in r["response"]          # rehydrated, even though mock mangled case
    assert r["entities_masked"] == 2


def test_session_keeps_consistent_placeholders():
    sid = post().json()["session_id"]
    r2 = post(session_id=sid, prompt="Again: SSN 123-45-6789").json()
    assert "[SSN_1]" in r2["sanitized_prompt"]
    assert r2["entities_masked"] == 2              # same SSN reused, no new entity


def test_bad_strategy_and_backend_rejected():
    assert post(strategy="magic").status_code == 400
    assert post(backend="nope").status_code == 400


def test_delete_session():
    sid = post().json()["session_id"]
    assert client.delete(f"/session/{sid}").status_code == 200
    assert client.delete(f"/session/{sid}").status_code == 404
    assert sid not in _sessions


def test_health():
    assert client.get("/health").json()["status"] == "ok"


def test_ui_page_is_served():
    r = client.get("/")
    assert r.status_code == 200 and "Privacy Firewall" in r.text


def test_response_has_raw_reply_and_entity_names_but_no_originals():
    r = post().json()
    assert "[SSN_1]" in r["raw_response"].upper() or "[ssn_1]" in r["raw_response"]
    assert {e["label"] for e in r["entities"]} == {"SSN", "EMAIL"}
    assert "123-45-6789" not in str(r["entities"])


def test_models_endpoint_returns_a_list():
    assert isinstance(client.get("/models").json()["ollama"], list)
