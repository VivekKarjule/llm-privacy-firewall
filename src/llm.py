"""
llm.py - interchangeable LLM backends. Every backend is just: text in -> text out.
The firewall only ever hands a backend SANITIZED text.

  mock       - fake LLM, no key, no internet (default; used for tests and demos)
  ollama     - local model via Ollama (http://localhost:11434)
  anthropic  - cloud Claude API (needs ANTHROPIC_API_KEY in your .env)
"""
import json
import os
import re
import urllib.request

try:                       # optional: load keys from .env if python-dotenv is installed
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def mock_llm(prompt: str) -> str:
    """Pretend LLM. Mangles the first placeholder (lowercase) like real LLMs sometimes do."""
    mangled = re.sub(r"\[(\w+)\]", lambda m: f"[{m.group(1).lower()}]", prompt, count=1)
    return f"Here is a summary of your request: {mangled}"


def ollama_llm(prompt: str) -> str:
    body = json.dumps({"model": os.getenv("OLLAMA_MODEL", "llama3.2"),
                       "prompt": prompt, "stream": False}).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read())["response"]


def anthropic_llm(prompt: str) -> str:
    import anthropic            # pip install anthropic
    client = anthropic.Anthropic()   # reads ANTHROPIC_API_KEY from the environment
    msg = client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5-5"),
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


BACKENDS = {"mock": mock_llm, "ollama": ollama_llm, "anthropic": anthropic_llm}


def get_backend(name: str):
    if name not in BACKENDS:
        raise ValueError(f"backend must be one of {list(BACKENDS)}")
    return BACKENDS[name]
