# app/agent/normalizers.py
from __future__ import annotations

from typing import Dict, Any, Optional, List, Tuple

MODEL_TOKEN_MAP: List[Tuple[str, List[str]]] = [
    ("iPhone 15 Pro Max", ["15 pro max", "15promax", "promax", "برو ماكس", "ماكس"]),
    ("iPhone 15 Pro", ["15 pro", "15pro", "برو"]),
    ("iPhone 15 Plus", ["15 plus", "15+", "بلاس", "بلس"]),
    ("iPhone 15", ["iphone 15", "ايفون 15", "آيفون 15"]),
    ("iPhone 14 Pro Max", ["14 pro max", "14promax"]),
    ("iPhone 14 Pro", ["14 pro"]),
    ("iPhone 14 Plus", ["14 plus"]),
    ("iPhone 14", ["iphone 14", "ايفون 14", "آيفون 14"]),
]

STORAGE_TOKEN_MAP: List[Tuple[str, List[str]]] = [
    ("1TB", ["1tb", "١ تيرابايت", "1024"]),
    ("512GB", ["512", "٥١٢"]),
    ("256GB", ["256", "٢٥٦"]),
    ("128GB", ["128", "١٢٨"]),
]


def infer_model_from_text(txt: str) -> Optional[str]:
    for label, tokens in MODEL_TOKEN_MAP:
        if any(token in txt for token in tokens):
            return label
    return None


def infer_storage_from_text(txt: str) -> Optional[str]:
    for label, tokens in STORAGE_TOKEN_MAP:
        if any(token in txt for token in tokens):
            return label
    return None


def spec_normalizer(name: str, retailer: str, condition: str) -> Dict[str, Any]:
    """Normalize model, storage, and condition from raw product text."""
    txt = f"{name} {retailer} {condition}".lower()

    model = infer_model_from_text(txt)
    storage = infer_storage_from_text(txt)

    cond_raw = (condition or "").strip()
    cl = cond_raw.lower()
    if cl in {"new", "brand new", "جديد"}:
        cond = "New"
    elif "refurb" in cl or cl in {"مجدَّد", "منتَجات مجدَّدة"}:
        cond = "Refurbished"
    elif cl.startswith("used"):
        cond = "Used"
    else:
        cond = cond_raw or "Unknown"

    return {"model": model, "storage": storage, "condition": cond}


def price_normalizer(price: float, currency: Optional[str]) -> Dict[str, Any]:
    """Normalize a price to SAR. If currency unknown, assume SAR."""
    if not currency or currency.upper() == "SAR":
        return {"price_sar": float(price), "currency": "SAR"}

    rates = {"USD": 3.75, "EUR": 4.1}
    factor = rates.get(currency.upper(), 1.0)
    return {"price_sar": float(price) * factor, "currency": currency.upper()}
