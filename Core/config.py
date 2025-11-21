# app/core/config.py
from __future__ import annotations

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env at project root
load_dotenv()

# Strip whitespace from keys to avoid issues with .env file formatting
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip() if os.getenv("OPENAI_API_KEY") else None
# SearchAPI.io key
SEARCHAPI_KEY = os.getenv("SEARCHAPI_KEY", "").strip() if os.getenv("SEARCHAPI_KEY") else None


def get_openai_client() -> OpenAI:
    """Return a shared OpenAI client. Raises if API key is missing."""
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY missing (set env var or .env).")
    return OpenAI(api_key=OPENAI_API_KEY)


# Global OpenAI client (used by ranking module)
client: OpenAI = get_openai_client()
