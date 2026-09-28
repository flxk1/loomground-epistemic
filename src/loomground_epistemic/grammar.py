# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 flxk1
"""Epistemic language: extract the epistemic nD facet from free text.

Operator + certainty come from this pack's cues; the ``holder`` is an entity NP,
so it CONSUMES ``loomground_factual.clean_entity`` — the addressee vocabulary
lives once, in the substrate, and deontic bearer / epistemic holder both use it.
Standard library + loomground-factual only; cues are DATA in extraction.json.
"""
from __future__ import annotations

import json
import re
from importlib.resources import files
from typing import Any, Optional

from loomground_factual import clean_entity

from .facet import EPISTEMIC_FACET

__all__ = ["load_json", "extract", "EPISTEMIC_FACET"]


def load_json(name: str) -> Any:
    return json.loads((files("loomground_epistemic") / "artifacts" / name).read_text("utf-8"))


_EX = load_json("extraction.json")
_OPS = [(re.compile(c["pattern"], re.I), c["operator"], c["certainty"])
        for c in _EX["operator_cues"]]
_SRC = re.compile(_EX["source_cue"], re.I)
_HOLDER_LEAD = re.compile(_EX["holder_lead"], re.I)
_HOLDER_TRAIL = re.compile(_EX["holder_trail_aux"], re.I)
_PROP_LEAD = re.compile(_EX["proposition_lead"], re.I)


def _holder(pre: str) -> str:
    """The knower: strip a subordinator lead, reduce to the entity NP head (shared
    factual cue), then drop a trailing auxiliary that abuts the operator phrase."""
    s = _HOLDER_LEAD.sub("", (pre or "").strip()).strip()
    s = clean_entity(s)                       # shared NP-head from the substrate
    s = _HOLDER_TRAIL.sub("", s).strip()
    return s.strip(" .,;:")


_COMPLEMENTIZER = re.compile(_EX["complementizer"], re.I)
_TRIM = " .,;:"


def _trim(text: str, start: int, end: int) -> tuple[int, int]:
    """Narrow ``[start, end)`` past surrounding whitespace and trailing punctuation."""
    while start < end and text[start].isspace():
        start += 1
    while end > start and (text[end - 1].isspace() or text[end - 1] in _TRIM):
        end -= 1
    return start, end


def _analyse(sentence: str) -> Optional[dict[str, Any]]:
    """The facet plus the spans it was read from (offsets index ``sentence``)."""
    if not isinstance(sentence, str) or not sentence.strip():
        return None
    for pat, op, band in _OPS:
        m = pat.search(sentence)
        if not m:
            continue
        proposition = _PROP_LEAD.sub("", sentence[m.end():].strip(" .,;:")).strip(" .,;:")
        sm = _SRC.search(sentence)
        p0, p1 = _trim(sentence, m.end(), len(sentence))
        cm = _COMPLEMENTIZER.match(sentence, p0)
        if cm:
            p0 = cm.end()
        if sm and p0 < sm.start() < p1:   # the evidential phrase is not the proposition
            p0, p1 = _trim(sentence, p0, sm.start())
        return {
            "facet": {
                "facet": "nD",
                "system_id": EPISTEMIC_FACET["system_id"],
                "operator": op,
                "holder": _holder(sentence[:m.start()]),
                "proposition": proposition,
                "certainty": band,
                "source": (sm.group("src").strip() if sm else ""),
            },
            "span": _trim(sentence, 0, len(sentence)),
            "proposition_span": (p0, p1) if p0 < p1 else None,
        }
    return None


def extract(sentence: str) -> Optional[dict[str, Any]]:
    """Extract the epistemic facet, or ``None`` when no epistemic operator is present."""
    rec = _analyse(sentence)
    return dict(rec["facet"]) if rec else None
