# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 flxk1
"""Cross-jurisdiction quality gate for epistemic facet extraction.

Real epistemic-triggered provisions with the EXPECTED facet. Holder correctness
depends on the SHARED factual NP-head cue — proving the cross-language reuse.
"""
from __future__ import annotations

import re

from loomground_epistemic import extract


def _n(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower()).strip(" .,;:")


CASES = [
    # (raw, operator, holder, certainty)
    ("The controller has reasonable grounds to believe a personal data breach has occurred.",
     "B", "controller", "reasonable-grounds"),
    ("Where the controller becomes aware that a breach is likely to result in a high risk.",
     "K", "controller", "certain"),
    ("The provider believes that the system meets the requirements.",
     "B", "provider", "probable"),
    ("The supervisory authority suspects an infringement of this Regulation.",
     "B", "supervisory authority", "possible"),
    ("- 1 A business is satisfied that the consumer has consented to the sale.",
     "B", "business", "probable"),
    ("The deployer has reason to believe that use of the system may present a risk.",
     "B", "deployer", "possible"),
]


def test_epistemic_facet_extraction():
    op = holder = cert = 0
    for raw, e_op, e_holder, e_cert in CASES:
        f = extract(raw) or {}
        op += f.get("operator") == e_op
        holder += _n(f.get("holder", "")) == _n(e_holder)
        cert += f.get("certainty") == e_cert
    n = len(CASES)
    assert op == n, f"operator {op}/{n}"
    assert holder == n, f"holder {holder}/{n}"
    assert cert == n, f"certainty {cert}/{n}"


def test_facet_binds_across_5d():
    # the facet descriptor documents how it stretches across the fixed 5D
    from loomground_epistemic import EPISTEMIC_FACET
    assert EPISTEMIC_FACET["system_id"] == "system:epistemic"
    assert set(EPISTEMIC_FACET["binds"]) == {"proposition", "holder", "certainty", "assertion"}
