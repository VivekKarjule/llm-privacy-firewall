"""
proxy.py - the firewall as a web service.

Run from the project root:
    uvicorn src.proxy:app --reload
Then open http://127.0.0.1:8000/docs  (interactive page, no UI code needed)

Flow of POST /chat:   prompt -> sanitize -> LLM backend -> rehydrate -> response
Privacy rules enforced here:
  * only the SANITIZED prompt is ever logged or sent out
  * the placeholder<->original mapping lives in memory only and is never returned
  * sessions are capped, and can be erased with DELETE /session/{id}
"""
import logging
import uuid
from collections import OrderedDict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.firewall import Firewall
from src.llm import get_backend

log = logging.getLogger("firewall")
app = FastAPI(title="LLM Privacy Firewall", version="0.1")

from fastapi.responses import RedirectResponse

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

MAX_SESSIONS = 100
_sessions: "OrderedDict[str, Firewall]" = OrderedDict()   # session_id -> its own Firewall


class ChatRequest(BaseModel):
    prompt: str
    session_id: str | None = None
    strategy: str = "hybrid"      # regex | spacy | hybrid (fixed when the session starts)
    backend: str = "mock"         # mock | ollama | anthropic


class ChatResponse(BaseModel):
    session_id: str
    sanitized_prompt: str         # exactly what left the machine
    response: str                 # LLM answer with real values restored
    entities_masked: int


@app.get("/health")
def health():
    return {"status": "ok", "active_sessions": len(_sessions)}


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
        raw = backend(safe)
    except Exception as e:
        raise HTTPException(502, f"LLM backend error: {type(e).__name__}")

    return ChatResponse(session_id=sid, sanitized_prompt=safe,
                        response=fw.restore(raw), entities_masked=fw.entities_masked)


@app.delete("/session/{session_id}")
def delete_session(session_id: str):
    if _sessions.pop(session_id, None) is None:
        raise HTTPException(404, "no such session")
    return {"deleted": session_id}
