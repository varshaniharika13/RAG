from __future__ import annotations

import re

ACRONYM_MAP = {
    "coa": "cost of attendance",
    "sap": "satisfactory academic progress",
    "ferpa": "family educational rights and privacy act",
    "gpa": "grade point average",
    "loa": "leave of absence",
}

TERM_NORMALIZATION = {
    "drop class": "course withdrawal",
    "quit school": "withdrawal from university",
    "punishment": "disciplinary sanction",
}


def rewrite_query(query: str) -> str:
    normalized = query.lower().strip()
    normalized = re.sub(r"\s+", " ", normalized)

    expansions: list[str] = []
    tokens = normalized.split(" ")
    for token in tokens:
        if token in ACRONYM_MAP:
            expansions.append(ACRONYM_MAP[token])

    rewritten = normalized
    for source_term, canonical_term in TERM_NORMALIZATION.items():
        rewritten = rewritten.replace(source_term, canonical_term)

    if expansions:
        rewritten = f"{rewritten} {' '.join(expansions)}"

    return rewritten
