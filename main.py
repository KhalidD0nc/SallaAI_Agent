# app/main.py
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from Core.config import OPENAI_API_KEY, SEARCHAPI_KEY
from API.routes_rank import router as rank_router


app = FastAPI(
    title="KSA Shopping Ranker API",
    description="LangGraph-based shopping agent for the Saudi market.",
    version="0.1.0",
)

# CORS (you can restrict origins later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> Dict[str, Any]:
    """Simple health check endpoint."""
    errors = []
    if not OPENAI_API_KEY:
        errors.append("OPENAI_API_KEY is missing")
    if not SEARCHAPI_KEY:
        errors.append("SEARCHAPI_KEY is missing")
    
    if errors:
        return {
            "status": "error",
            "message": "; ".join(errors),
        }
    
    # Check key format
    key_info = {}
    if SEARCHAPI_KEY:
        key_info = {
            "length": len(SEARCHAPI_KEY),
            "starts_with": SEARCHAPI_KEY[:8] + "..." if len(SEARCHAPI_KEY) > 8 else "too_short",
            "has_whitespace": bool(SEARCHAPI_KEY != SEARCHAPI_KEY.strip()),
        }
    
    return {
        "status": "ok",
        "service": "KSA Shopping Ranker API",
        "version": "0.1.0",
        "keys_configured": {
            "openai": bool(OPENAI_API_KEY),
            "searchapi": bool(SEARCHAPI_KEY),
        },
        "searchapi_key_info": key_info if SEARCHAPI_KEY else None,
    }


@app.get("/test", response_class=HTMLResponse)
async def test_page() -> HTMLResponse:
    """Serve the agent test page."""
    static_dir = Path(__file__).parent / "static"
    html_file = static_dir / "test.html"
    
    if not html_file.exists():
        return HTMLResponse(
            content="<h1>Test page not found</h1>",
            status_code=404
        )
    
    with open(html_file, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


# Register v1 routes
app.include_router(rank_router)
