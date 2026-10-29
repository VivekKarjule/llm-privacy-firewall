"""
proxy.py - the firewall as a web service with a browser UI.

Run from the project root:
    uvicorn src.proxy:app --reload
Then open http://127.0.0.1:8000/        (the demo UI)
        and http://127.0.0.1:8000/docs   (raw API page)

Flow of POST /chat:   prompt -> sanitize -> LLM backend -> rehydrate -> response
Privacy rules enforced here:
  * only the SANITIZED prompt is ever logged or sent out
  * the placeholder<->original mapping lives in memory only; the API returns
    placeholder NAMES and labels, never the original values
  * sessions are capped, and can be erased with DELETE /session/{id}
"""
import logging
import uuid
from collections import OrderedDict
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from src.firewall import Firewall
from src.llm import get_backend, list_ollama_models

log = logging.getLogger("firewall")
app = FastAPI(title="LLM Privacy Firewall", version="0.2")

UI_FILE = Path(__file__).parent / "static" / "index.html"
MAX_SESSIONS = 100
_sessions: "OrderedDict[str, Firewall]" = OrderedDict()   # session_id -> its own Firewall


class ChatRequest(BaseModel):
    prompt: str
    session_id: str | None = None
    strategy: str = "hybrid"      # regex | spacy | hybrid (fixed when the session starts)
    backend: str = "mock"         # mock | ollama | anthropic
    model: str | None = None      # e.g. an Ollama model name


class Entity(BaseModel):
    placeholder: str              # e.g. "[PERSON_1]"
    label: str                    # e.g. "PERSON"


class ChatResponse(BaseModel):
    session_id: str
    sanitized_prompt: str         # exactly what left the machine
    raw_response: str             # what the LLM answered (placeholders still inside)
    response: str                 # LLM answer with real values restored
    entities_masked: int
    entities: list[Entity]


@app.get("/", include_in_schema=False)
def ui():
    return FileResponse(UI_FILE)


@app.get("/health")
def health():
    return {"status": "ok", "active_sessions": len(_sessions)}


@app.get("/models")
def models():
    """Locally installed Ollama models (empty list if Ollama is not running)."""
    return {"ollama": list_ollama_models()}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        backend = get_backend(req.backend)
    except ValueError as e:
        raise HTTPException(400, str(e))

    sid = req.session_id or uuid.uuid4().hex
    fw = _sessions.get(sid)
    if fw is None:
        try:
            fw = Firewall(req.strategy)
        except ValueError as e:
            raise HTTPException(400, str(e))
        _sessions[sid] = fw
        while len(_sessions) > MAX_SESSIONS:
            _sessions.popitem(last=False)      # drop the oldest session

    try:
        safe = fw.sanitize(req.prompt)
    except (ImportError, OSError):
        raise HTTPException(503, "spaCy or its model is not installed; use strategy 'regex' or install it")

    log.info("outgoing (sanitized) prompt: %s", safe)   # never log req.prompt
    try:
        raw = backend(safe, req.model)
    except Exception as e:
        raise HTTPException(502, f"LLM backend error ({type(e).__name__}). "
                                 "For Ollama: is it running and is the model installed?")

    ents = [Entity(placeholder=p, label=p.strip("[]").rsplit("_", 1)[0]) for p in fw.placeholders]
    return ChatResponse(session_id=sid, sanitized_prompt=safe, raw_response=raw,
                        response=fw.restore(raw), entities_masked=fw.entities_masked,
                        entities=ents)


@app.delete("/session/{session_id}")
def delete_session(session_id: str):
    if _sessions.pop(session_id, None) is None:
        raise HTTPException(404, "no such session")
    return {"deleted": session_id}
