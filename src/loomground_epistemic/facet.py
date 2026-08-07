# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 flxk1
"""The epistemic nD facet descriptor.

Epistemic modality is an operator OVER a proposition, held by an agent at a
certainty threshold — the 5D axes cannot carry it (they carry relations between
entities), which is exactly why it earns its own nD facet, the alethic-modal
sibling of deontic. The facet is *stretched across* the 5D: ``proposition``
references a factual 5D edge, ``holder`` is a RELATIONAL/INTENTIONAL node, and
``certainty`` gates a CAUSAL condition. Data only — versum's NDRegistry registers
this descriptor; this package never imports versum.
"""
from __future__ import annotations

#: The facet contract a consumer (versum) registers.
EPISTEMIC_FACET = {
    "facet": "nD",
    "system_id": "system:epistemic",
    "fields": ["operator", "holder", "proposition", "certainty", "source"],
    "operators": {"K": "knowledge", "B": "belief"},
    "certainty_bands": [
        "certain", "reasonable-grounds", "probable", "possible", "estimate",
    ],
    # how the facet binds across the fixed 5D (documentation for the projector):
    "binds": {
        "proposition": "relational",   # -> a factual 5D edge (the thing known/believed)
        "holder": "intentional",       # -> the agent who holds the attitude
        "certainty": "causal",         # -> gates a condition (a duty fires past the threshold)
        "assertion": "temporal",       # -> when the attitude is held
    },
}
