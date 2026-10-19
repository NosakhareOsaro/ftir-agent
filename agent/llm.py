"""
llm.py

Minimal client for any OpenAI-compatible /chat/completions endpoint.

One request format covers both backends this project uses:
  Gemini (free tier)  https://generativelanguage.googleapis.com/v1beta/openai
  Ollama (local)      http://localhost:11434/v1

Configured from the environment (or a .env file):
  LLM_BASE_URL      default: the Gemini endpoint above
  LLM_API_KEY       API key (GEMINI_API_KEY is also accepted)
  LLM_MODEL         default: gemini-3.8-flash
  LLM_MIN_INTERVAL  seconds between requests, to stay under free-tier RPM (default 6)
"""

import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/openai"
DEFAULT_MODEL = "gemini-3.8-flash"
MAX_RETRIES = 5


class LLMError(RuntimeError):
    pass


class ChatClient:
    def __init__(self, base_url=None, api_key=None, model=None, min_interval=None, timeout=120):
        self.base_url = (base_url or os.getenv("LLM_BASE_URL") or GEMINI_URL).rstrip("/")
        self.api_key = api_key or os.getenv("LLM_API_KEY") or os.getenv("GEMINI_API_KEY")
        self.model = model or os.getenv("LLM_MODEL") or DEFAULT_MODEL
        if min_interval is None:
            min_interval = float(os.getenv("LLM_MIN_INTERVAL", "6"))
        self.min_interval = min_interval
        self.timeout = timeout
        self.n_requests = 0
        self._last = 0.0

        if self.base_url == GEMINI_URL and not self.api_key:
            raise LLMError(
                "No API key. Get a free one at https://aistudio.google.com/apikey "
                "and put LLM_API_KEY=... in a .env file."
            )

    def chat(self, messages, tools=None, temperature=0.0):
        """Send one chat request; return the assistant message dict."""
        body = {"model": self.model, "messages": messages, "temperature": temperature}
        if tools:
            body["tools"] = tools
            body["tool_choice"] = "auto"
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        for attempt in range(MAX_RETRIES):
            wait = self._last + self.min_interval - time.monotonic()
            if wait > 0:
                time.sleep(wait)
            self._last = time.monotonic()
            self.n_requests += 1

            resp = requests.post(f"{self.base_url}/chat/completions",
                                 json=body, headers=headers, timeout=self.timeout)
            if resp.status_code == 429 or resp.status_code >= 500:
                # Free tier: back off and retry. Honour Retry-After if given.
                delay = float(resp.headers.get("Retry-After", 0)) or min(60, 5 * 2 ** attempt)
                time.sleep(delay)
                continue
            if not resp.ok:
                raise LLMError(f"{resp.status_code} from {self.base_url}: {resp.text[:500]}")
            choices = resp.json().get("choices") or []
            if not choices:
                raise LLMError(f"empty response: {resp.text[:500]}")
            return choices[0]["message"]

        raise LLMError(f"gave up after {MAX_RETRIES} retries (rate limited or server error)")
