# app/agent/ranking.py
from __future__ import annotations

import json
from typing import List, Dict, Any

from Core.config import client
from Core.constants import TRUSTED_KSA


def llm_rank_offers(
    offers: List[Dict[str, Any]],
    query: str,
    intent: Dict[str, Any],
    trusted_only: bool = False,
    top_k: int = 4,
) -> Dict[str, Any]:
    """Final LLM re-ranking with policy-aware selection and JSON output."""
    if not offers:
        return {"items": [], "notes": "No offers available for ranking."}

    slim = [
        {
            "name": o.get("name"),
            "price": o.get("price_sar", o.get("price")),
            "currency": o.get("currency", "SAR"),
            "retailer": o.get("retailer"),
            "link": o.get("link"),
            "condition": o.get("condition"),
            "image": o.get("image"),
            "model": o.get("model"),
            "storage": o.get("storage"),
            "is_trusted": o.get("retailer") in TRUSTED_KSA,
        }
        for o in offers
        if o.get("link")
    ]

    policy = {
        "need_summary": intent.get("need_summary"),
        "category": intent.get("category"),
        "budget_min": intent.get("budget_min"),
        "budget_max": intent.get("budget_max"),
        "must_have": intent.get("must_have", []),
        "nice_to_have": intent.get("nice_to_have", []),
        "trusted_only": trusted_only,
    }

    system = (
        "You are a Saudi Arabia shopping concierge. Select products that satisfy the user need, "
        "respect budgets, and provide short reasoning. Prefer trusted retailers when requested. "
        "If images are provided, pass them through. Return strict JSON according to the schema."
    )
    schema = {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["name", "price", "currency", "retailer", "link", "reason"],
                    "properties": {
                        "name": {"type": "string"},
                        "price": {"type": "number"},
                        "currency": {"type": "string"},
                        "retailer": {"type": "string"},
                        "link": {"type": "string"},
                        "image": {"type": ["string", "null"]},
                        "reason": {"type": "string"},
                    },
                },
            },
            "notes": {"type": ["string", "null"]},
        },
        "required": ["items"],
    }

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system},
            {
                "role": "user",
                "content": (
                    "User query:\n"
                    f"{query}\n\n"
                    "Shopping intent:\n"
                    f"{json.dumps(policy, ensure_ascii=False)}\n\n"
                    "Candidate offers:\n"
                    f"{json.dumps(slim, ensure_ascii=False)}\n\n"
                    "Return schema:\n"
                    f"{json.dumps(schema, ensure_ascii=False)}"
                ),
            },
        ],
    )
    data = json.loads(resp.choices[0].message.content)
    data["items"] = data.get("items", [])[:top_k]
    return data
