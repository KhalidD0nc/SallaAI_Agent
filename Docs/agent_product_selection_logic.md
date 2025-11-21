# Agent Product Selection Logic

This document explains *why* and *how* the agent selects and returns specific products to the user.

## Overview

The agent returns a product when it identifies a **shopping intent** in the user's query. The selection process is a multi-stage pipeline that moves from broad search to strict filtering and finally to intelligent LLM-based ranking.

## Detailed Process

### 1. Intent Analysis (`analyze_intent`)
The process begins by analyzing the user's query to extract:
- **Search Query**: The core product terms.
- **Constraints**: Budget range (`budget_min`, `budget_max`), category, and specific features (`must_have`).
- **Readiness**: Whether enough information exists to perform a search.

### 2. Data Gathering (`planner` & `actor`)
If the intent is clear, the agent executes tools:
- **`shopping_search`**: Fetches raw offers from external APIs.
- **Normalizers**: Standardizes specs (storage, model) and prices (converts to SAR).
- **`product_page_fetch`**: Optionally visits product pages for missing details.

### 3. Hard Filtering (`finisher`)
Before AI ranking, candidates pass through strict logical filters:
- **Validity**: Must have a valid price and purchase link.
- **Budget**: Price must be within the user's specified range.
- **Category**: Product name must match the requested category.
- **Keywords**: "Must-have" terms are checked against the product name.

### 4. Prioritization & Ranking (`finisher` & `llm_rank_offers`)
Surviving candidates are prioritized:
1.  **Trust**: "Trusted KSA retailers" (defined in `TRUSTED_KSA`) are prioritized.
2.  **Condition**: New > Refurbished > Used.
3.  **Price**: Lower prices are preferred.

Finally, the top candidates (up to 20) are sent to an LLM (`gpt-4o-mini`) which acts as a **"Saudi Arabia shopping concierge"**. The LLM:
- Selects the final set (top 4).
- Verifies the product truly meets the user's subtle needs.
- Generates a human-readable **reason** for selecting each product.

## Conclusion

The agent returns a product not just because it matches keywords, but because it has survived a rigorous filter for **validity**, **budget compliance**, **seller trust**, and **contextual relevance** determined by an AI concierge.

