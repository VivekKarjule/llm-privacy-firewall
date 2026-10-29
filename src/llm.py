"""
llm.py - interchangeable LLM backends. Every backend: (sanitized text, optional model) -> text.
The firewall only ever hands a backend SANITIZED text.

  mock       - fake LLM, no key, no internet (default; tests and quick demos)
  ollama     - local model via Ollama (http://localhost:11434)
  gemini     - Google Gemini API, free tier (needs GEMINI_API_KEY in your .env)
  anthropic  - cloud Claude API (needs ANTHROPIC_API_KEY in your .env)
"""
import json
import os
import re
import urllib.error
import urllib.request

try:                       # optional: load keys from .env if python-dotenv is installed
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Tells the model to copy placeholders verbatim. Without this, small models often
# rewrite "[PERSON_1]" or ask what it means, which breaks rehydration.
SYSTEM_PROMPT = (
    "Tokens written like [PERSON_1], [SSN_1] or [EMAIL_1] are anonymised placeholders "
    "for real values. Treat them as ordinary names or numbers and copy them EXACTLY as "
    "written, including the square brackets, whenever you refer to them. "
    "Never ask what they mean."
)


class BackendError(Exception):
    """An error whose message is safe to show the user (never contains keys)."""


def mock_llm(prompt: str, model: str | None = None) -> str:
    """Pretend LLM. Mangles the first placeholder (lowercase) like real LLMs sometimes do."""
    mangled = re.sub(r"\[(\w+)\]", lambda m: f"[{m.group(1).lower()}]", prompt, count=1)
    return f"Here is a summary of your request: {mangled}"


def ollama_llm(prompt: str, model: str | None = None) -> str:
    body = json.dumps({
        "model": model or os.getenv("OLLAMA_MODEL", "llama3.2"),
        "system": SYSTEM_PROMPT, "prompt": prompt, "stream": False,
    }).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read())["response"]


def list_ollama_models() -> list[str]:
    """Names of locally installed Ollama models; [] if Ollama is not running."""
    try:
        with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=2) as r:
            return [m["name"] for m in json.loads(r.read()).get("models", [])]
    except Exception:
        return []


def _extract_gemini_text(data: dict) -> str:
    """Join the text parts of the first candidate in a Gemini response."""
    try:
        parts = data["candidates"][0]["content"]["parts"]
        return "".join(p.get("text", "") for p in parts)
    except (KeyError, IndexError, TypeError):
        raise BackendError("Gemini returned no text (the reply may have been blocked).")


def gemini_llm(prompt: str, model: str | None = None) -> str:
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise BackendError("GEMINI_API_KEY is not set. Add it to your .env file and restart the server.")
    model = model or os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    body = json.dumps({
        "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
    }).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": "application/json", "x-goog-api-key": key})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return _extract_gemini_text(json.loads(resp.read()))
    except urllib.error.HTTPError as e:
        hints = {400: "bad request or invalid API key", 403: "key not allowed",
                 404: f"model '{model}' not found, pick another model",
                 429: "free-tier rate limit hit, wait a minute and retry"}
        raise BackendError(f"Gemini error {e.code}: {hints.get(e.code, 'request failed')}.")
    except urllib.error.URLError:
        raise BackendError("Could not reach Gemini. Check your internet connection.")


def anthropic_llm(prompt: str, model: str | None = None) -> str:
    import anthropic            # pip install anthropic
    client = anthropic.Anthropic()   # reads ANTHROPIC_API_KEY from the environment
    msg = client.messages.create(
        model=model or os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5-5"),
        max_tokens=1000, system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


BACKENDS = {"mock": mock_llm, "ollama": ollama_llm, "gemini": gemini_llm,
            "anthropic": anthropic_llm}


def get_backend(name: str):
    if name not in BACKENDS:
        raise ValueError(f"backend must be one of {list(BACKENDS)}")
    return BACKENDS[name]
