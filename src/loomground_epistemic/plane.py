# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 flxk1
"""The epistemic plane descriptor (Loomground plane descriptor contract v1).

Published through the ``loomground.planes`` entry-point group under the plane id
``epistemic``. The nD-system document is ``EPISTEMIC_FACET["nd_system"]``, the
field -> 5D binding is ``EPISTEMIC_FACET["binds"]`` (read from
``artifacts/binding.json``, its one home), and ``produce`` reads ``extract()``:
K or B, holder, certainty band and evidential source, with the embedded
proposition linked by its own sub-span. Pure and deterministic; ``[]`` when the
sentence carries no epistemic operator; values are never repaired. This package
never imports the versum.
"""
from __future__ import annotations

import copy
from typing import Any, Optional

from ._version import __version__
from .facet import EPISTEMIC_FACET, PLANE_ID
from .grammar import _analyse, load_json

__all__ = ["PLANE_ID", "plane", "nd_system", "binding", "produce", "examples"]

METHOD = "loomground-epistemic/extract"


def binding() -> dict[str, str]:
    """field -> 5D dimension, as the facet binds it (from the single binding file)."""
    return dict(EPISTEMIC_FACET["binds"])


def nd_system() -> dict[str, Any]:
    """The epistemic nD-system document (``versum.nd.NDSystem.from_dict`` shape)."""
    return copy.deepcopy(EPISTEMIC_FACET["nd_system"])


def produce(sentence: str, context: Optional[dict[str, Any]] = None) -> list[dict[str, Any]]:
    """The epistemic claim in ``sentence`` (at most one), or ``[]``.

    ``context`` is accepted for the contract and ignored. A coordinate the
    sentence does not supply (an empty holder or source) is omitted, never
    invented; the consumer reports a missing required slot."""
    rec = _analyse(sentence)
    if rec is None:
        return []
    facet = rec["facet"]
    rules = {r["allowed_axes"][0]: r["form_slot"] for r in EPISTEMIC_FACET["nd_system"]["bindings"]}
    coordinates = {axis: facet[axis] for axis in rules if facet.get(axis) != ""}
    claim: dict[str, Any] = {
        "relation": EPISTEMIC_FACET["operators"][facet["operator"]],
        "span": list(rec["span"]),
        "coordinates": coordinates,
        "slots": {rules[axis]: axis for axis in coordinates},
        "method": METHOD,
    }
    if rec["proposition_span"] is not None:
        field, = EPISTEMIC_FACET["span_fields"]      # the proposition
        claim["links"] = [{"type": EPISTEMIC_FACET["binds"][field],
                           "relation": field,
                           "to_span": list(rec["proposition_span"])}]
    return [claim]


def examples() -> list[dict[str, Any]]:
    """The plane's published conformance vectors: ``{sentence, expected}``."""
    return copy.deepcopy(load_json("examples.json")["examples"])


def plane() -> dict[str, Any]:
    """Zero-arg entry-point target: the epistemic plane descriptor."""
    return {
        "plane": PLANE_ID,
        "language_version": __version__,
        "nd_system": nd_system(),
        "binding": binding(),
        "produce": produce,
        "examples": examples(),
    }
