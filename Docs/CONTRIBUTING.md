# Contributing Guide

## Scope & Principles
- Keep the agent trustworthy for shoppers: accuracy, transparency, privacy.
- Favor small, reviewable pull requests with strong test or reasoning evidence.
- Document external assumptions (APIs, FX rates, ranking rules) in code comments or `DOCS/`.

## Prerequisites
- Python 3.12+, Poetry or venv, and `uvicorn`.
- OpenAI and SearchAPI.io credentials stored in project `.env`.
- macOS/Linux shell with `make` support (or run the underlying commands).

## Environment Setup
1. `python -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. Create `.env` in the repo root:
   ```
   OPENAI_API_KEY=...
   SEARCHAPI_KEY=...
   ```
4. Run style/test tooling once to confirm no baseline failures.

## Running the Service
- Dev server: `uvicorn main:app --reload --host 0.0.0.0 --port 8000`
- Health check: GET `http://localhost:8000/docs`
- Ranking API smoke test:
  ```
  curl -X POST http://localhost:8000/rank \
    -H "Content-Type: application/json" \
    -d '{"query":"iphone 16 pro 256gb"}'
  ```

## Workflow Expectations
- Discuss ideas in an issue before large changes; tag with `agent`, `api`, or `infra`.
- Branch naming: `feature/<short-topic>` or `fix/<short-topic>`.
- Commit messages follow Conventional Commits (`feat:`, `fix:`, `docs:` …).
- Keep PRs under ~400 LOC diff; split when adding new tools plus policy updates.

## Coding Guidelines
- Python: type hints everywhere, prefer dataclasses or Pydantic models over dicts.
- FastAPI routers live under `API/`; avoid business logic in route handlers.
- LangGraph nodes (`AGENT/graph.py`) must stay idempotent; guard network calls with retries and timeouts.
- Add shared constants to `CORE/constants.py` and configuration helpers to `CORE/config.py`.
- Normalization helpers (`AGENT/normalizers.py`) should be pure functions to ease testing.

## Testing & Quality
- Add or update tests under `tests/` (create the folder if missing).
- Minimum expectations per PR:
  - Unit tests for new utilities/normalizers.
  - Integration smoke covering new graph branches or FastAPI routes (use `TestClient`).
  - Record sample payloads in PR description when exercising external APIs.
- Run locally:
  ```
  pytest
  scripts/lint.sh   # or ruff/black/pyright equivalents if scripts absent
  ```
- If a check is unavailable, explain in the PR how you validated the change (manual curl, notebook, etc.).

## Agent-Specific Tips
- When adding tools (`Agent/tools.py`), expose them via LangGraph tool registry and describe required inputs/outputs.
- Ranking policy adjustments live in `Agent/ranking.py`; keep the docstring aligned with README + policy docs.
- Update `DOCS/` with rationale whenever you tweak prioritization (e.g., retailer trust list).
- Prefer structured logging (`logger.info({"event": ...})`) over plain prints for traceability.

## Documentation & Communication
- Update `README.md` when setup or API contracts move.
- Keep diagrams or flow explanations under `DOCS/` using lightweight Markdown/Mermaid.
- PR template checklist (add to description):
  - [ ] Added tests or explained gaps
  - [ ] Updated docs/config samples
  - [ ] Manually exercised `/rank`
  - [ ] Checked for secrets in diff

## Security & Data Handling
- Never commit `.env`, API keys, or scraped payloads containing PII.
- Sanitize any logged retailer data (no customer info, only public offer fields).
- For suspected vulnerabilities, email maintainers (see repo README) instead of opening a public issue.

## Getting Help
- Use GitHub Discussions for architectural questions.
- Pair-review is encouraged; tag another maintainer when working on LangGraph plans or new tools.
- If unsure, ship smaller PRs first and iterate.

