from __future__ import annotations

import json
from typing import Any, Dict

from Core.config import client


INTENT_SYSTEM_PROMPT = (
    "You are a retail shopping concierge for Middle East consumers. "
    "Given the latest user utterance (single turn), extract the need summary, "
    "category, and any key constraints. Determine if you have enough information "
    "to start searching for products. If details are missing (e.g., budget, size, "
    "preferred specs), list them and craft ONE short follow-up question in the "
    "user's language. Always respond with strict JSON matching the schema."
)


def analyze_intent(query: str) -> Dict[str, Any]:
    schema = {
        "type": "object",
        "properties": {
            "need_summary": {"type": "string"},
            "category": {"type": "string"},
            "search_query": {"type": "string"},
            "budget_min": {"type": ["number", "null"]},
            "budget_max": {"type": ["number", "null"]},
            "must_have": {
                "type": "array",
                "items": {"type": "string"},
                "default": [],
            },
            "nice_to_have": {
                "type": "array",
                "items": {"type": "string"},
                "default": [],
            },
            "missing_info": {
                "type": "array",
                "items": {"type": "string"},
                "default": [],
            },
            "follow_up_question": {"type": ["string", "null"]},
            "ready": {"type": "boolean"},
        },
        "required": [
            "need_summary",
            "category",
            "search_query",
            "budget_min",
            "budget_max",
            "must_have",
            "nice_to_have",
            "missing_info",
            "follow_up_question",
            "ready",
        ],
    }

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": INTENT_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    "User request:\n"
                    f"{query}\n\n"
                    "Respond with JSON."
                ),
            },
        ],
    )
    data = json.loads(resp.choices[0].message.content)

    # Normalize legacy fields (some models might return different keys)
    if "ready" not in data:
        data["ready"] = bool(data.get("enough_information"))
    if "missing_info" not in data and "missing_details" in data:
        data["missing_info"] = data.get("missing_details", [])

    # Ensure defaults
    data.setdefault("must_have", [])
    data.setdefault("nice_to_have", [])
    data.setdefault("missing_info", [])

    # Normalize follow-up question empty strings to None
    fq = data.get("follow_up_question")
    data["follow_up_question"] = fq.strip() if isinstance(fq, str) and fq.strip() else None

    return data

