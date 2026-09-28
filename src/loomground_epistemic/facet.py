# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 flxk1
"""The epistemic nD facet descriptor.

Epistemic modality is an operator OVER a proposition, held by an agent at a
certainty threshold — the 5D axes cannot carry it (they carry relations between
entities), which is exactly why it earns its own nD facet, the alethic-modal
sibling of deontic. The facet is *stretched across* the 5D: ``proposition``
references a factual 5D edge, ``holder`` is an INTENTIONAL node, and
``certainty`` is a CAUSAL factual condition: the threshold is reached or not. A
norm's content may name that condition via the factual plane; the deontic
operator carries no 5D dimension. That field -> 5D binding is DATA, in its one
home ``artifacts/binding.json``.

``EPISTEMIC_FACET`` is also a valid nD-system document: its ``nd_system`` key is
the shape ``versum.nd.NDSystem.from_dict`` reads, with the closed vocabularies
derived from the facet's own ``operators`` and ``certainty_bands`` and the
version from the package version. Data only — this package never imports versum.
"""
from __future__ import annotations

import json
from importlib.resources import files
from typing import Any

from ._version import __version__

PLANE_ID = "epistemic"


def _binds() -> dict[str, str]:
    raw = (files("loomground_epistemic") / "artifacts" / "binding.json").read_text("utf-8")
    return dict(json.loads(raw)["binds"])


def _nd_system(facet: dict[str, Any]) -> dict[str, Any]:
    """The facet as an nD-system document. Every field except the span-linked
    ``proposition`` is an axis; each is bound to the form slot ``epistemic.<axis>``."""
    def closed(vocabulary) -> dict[str, Any]:
        return {"value_type": "controlled_identifier", "vocabulary_mode": "closed",
                "vocabulary": list(vocabulary), "cardinality": "one",
                "primitives": ["equal"]}

    def open_(value_type: str) -> dict[str, Any]:
        return {"value_type": value_type, "vocabulary_mode": "open",
                "cardinality": "one", "primitives": ["equal"]}

    axes = {
        "operator": closed(facet["operators"]),
        "holder": open_("entity_reference"),
        "certainty": closed(facet["certainty_bands"]),
        "source": open_("string"),
    }
    if set(axes) != set(facet["fields"]) - set(facet["span_fields"]):
        raise RuntimeError("epistemic facet fields and nD axes disagree")
    return {
        "id": f"loomground-{PLANE_ID}",
        "namespace": PLANE_ID,
        "version": __version__,
        "axes": axes,
        "bindings": [{"form_slot": f"{PLANE_ID}.{axis}", "allowed_axes": [axis],
                      "required": axis not in facet["optional_fields"]}
                     for axis in facet["fields"] if axis in axes],
        "validation": {"unknown_values": "reject"},
    }


#: The facet contract a consumer (versum) registers.
EPISTEMIC_FACET: dict[str, Any] = {
    "facet": "nD",
    "system_id": "system:epistemic",
    "fields": ["operator", "holder", "proposition", "certainty", "source"],
    # fields carried as a linked sub-span rather than a coordinate value
    "span_fields": ["proposition"],
    # fields a sentence may legitimately lack (no evidential phrase)
    "optional_fields": ["source"],
    "operators": {"K": "knowledge", "B": "belief"},
    "certainty_bands": [
        "certain", "reasonable-grounds", "probable", "possible", "estimate",
    ],
    # how the facet binds across the fixed 5D, read from artifacts/binding.json
    "binds": _binds(),
}
EPISTEMIC_FACET["nd_system"] = _nd_system(EPISTEMIC_FACET)
