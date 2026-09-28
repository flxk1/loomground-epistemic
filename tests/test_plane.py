# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 flxk1
"""Plane descriptor contract v1 for the epistemic plane, and the credit-decision case.

Each test names the plane-fit rule it proves (PORT-PLAN "Plane fit: 100%").
"""
from __future__ import annotations

import json
import re
from importlib.metadata import entry_points
from importlib.resources import files
from pathlib import Path

import pytest

import loomground_epistemic
from loomground_epistemic import EPISTEMIC_FACET, extract
from loomground_epistemic.grammar import load_json
from loomground_epistemic.plane import plane, produce

FIVE = {"structural", "causal", "intentional", "temporal", "relational"}
PKG = Path(loomground_epistemic.__file__).resolve().parent

S5 = "The controller knows that the training data is inaccurate."
CREDIT_OTHERS = [
    "The bank is a controller.",
    "The scoring model is part of the credit system.",
    "The controller must not make a solely automated decision on a credit application.",
    "The controller may use the score to prepare a decision.",
    "A reviewer shall examine every rejection before it is sent.",
    "The review follows the automated scoring.",
]


def test_s5_knowledge_holder_band_and_embedded_proposition_span():
    claims = produce(S5)
    assert len(claims) == 1
    c = claims[0]
    assert c["coordinates"]["operator"] == "K"
    assert c["coordinates"]["holder"] == "controller"
    assert c["coordinates"]["certainty"] == "certain"
    assert c["relation"] == "knowledge"
    link, = c["links"]
    assert link["type"] == EPISTEMIC_FACET["binds"]["proposition"] == "relational"
    s0, s1 = link["to_span"]
    assert S5[s0:s1] == "the training data is inaccurate"
    assert S5[c["span"][0]:c["span"][1]] == S5.rstrip(".")


@pytest.mark.parametrize("sentence", CREDIT_OTHERS)
def test_non_epistemic_credit_sentences_yield_nothing(sentence):
    assert produce(sentence) == []


def test_source_is_a_coordinate_and_outside_the_proposition():
    s = "The authority estimates that the damage is limited, based on the audit report."
    c, = produce(s)
    assert c["coordinates"]["source"] == "the audit report"
    assert c["coordinates"]["certainty"] == "estimate"
    s0, s1 = c["links"][0]["to_span"]
    assert s[s0:s1] == "the damage is limited"


def test_entry_point_discovers_epistemic_plane():
    eps = {ep.name: ep for ep in entry_points(group="loomground.planes")}
    assert "epistemic" in eps, "reinstall with pip install --no-deps -e ."
    d = eps["epistemic"].load()()
    assert d["plane"] == "epistemic"
    assert set(d) >= {"plane", "language_version", "nd_system", "binding", "produce"}
    assert callable(d["produce"])


def test_version_locked_to_package_version():
    # rule 5
    d = plane()
    assert d["language_version"] == loomground_epistemic.__version__
    assert d["nd_system"]["version"] == d["language_version"]
    assert not any(k.endswith("_5d_version") for k in d["nd_system"])


def test_facet_is_a_valid_nd_system_document():
    nd = pytest.importorskip("versum.nd")
    d = plane()
    system = nd.NDSystem.from_dict(d["nd_system"]).validate()
    assert system.version == d["language_version"]
    assert set(system.axes) == {"operator", "holder", "certainty", "source"}
    assert system.unknown_values == "reject"
    # EPISTEMIC_FACET itself is read as the nD-system document
    assert nd.NDSystem.from_dict(EPISTEMIC_FACET).validate() == system


def test_every_produced_claim_fits_the_nd_system_fail_closed():
    # rules 4 and 6
    nd = pytest.importorskip("versum.nd")
    system = nd.NDSystem.from_dict(plane()["nd_system"]).validate()
    rules = {r.form_slot: r for r in system.bindings}
    for ex in plane()["examples"]:
        for c in produce(ex["sentence"]):
            for axis, value in c["coordinates"].items():
                assert system.axes[axis].validate_value(value) == [], (axis, value)
            for slot, axis in c["slots"].items():
                assert axis in rules[slot].allowed_axes
            assert nd.required_binding_gaps(
                ["c"], system, [{"claim_id": "c", "form_slot": s} for s in c["slots"]]) == []
    assert system.axes["operator"].validate_value("P")
    assert system.axes["certainty"].validate_value("sure")


def test_binding_is_five_dimensions_from_one_data_file():
    # rules 2 and 3; EPISTEMIC_FACET.binds is authoritative
    d = plane()
    assert d["binding"] == EPISTEMIC_FACET["binds"]
    assert d["binding"] == {"proposition": "relational", "holder": "intentional",
                            "certainty": "causal", "assertion": "temporal"}
    assert set(d["binding"].values()) <= FIVE
    art = files("loomground_epistemic") / "artifacts"
    holders = [p.name for p in art.iterdir() if p.name.endswith(".json")
               and "binds" in json.loads(p.read_text("utf-8"))]
    assert holders == ["binding.json"]
    assert d["binding"] == json.loads((art / "binding.json").read_text("utf-8"))["binds"]
    for py in PKG.rglob("*.py"):
        src = py.read_text("utf-8")
        for dim in FIVE:
            assert not re.search(rf"[\"']{dim}[\"']", src), (py.name, dim)


def test_vocabularies_derived_from_the_facet():
    # rule 1: closed vocabularies equal the facet source; grammar cues stay inside them
    axes = plane()["nd_system"]["axes"]
    assert axes["operator"]["vocabulary"] == list(EPISTEMIC_FACET["operators"])
    assert axes["certainty"]["vocabulary"] == list(EPISTEMIC_FACET["certainty_bands"])
    cues = load_json("extraction.json")["operator_cues"]
    assert {c["operator"] for c in cues} <= set(EPISTEMIC_FACET["operators"])
    assert {c["certainty"] for c in cues} <= set(EPISTEMIC_FACET["certainty_bands"])


def test_producer_agrees_with_extract():
    for ex in plane()["examples"]:
        f = extract(ex["sentence"])
        claims = produce(ex["sentence"])
        assert bool(f) == bool(claims)
        if f:
            co = claims[0]["coordinates"]
            assert co["operator"] == f["operator"]
            assert co["certainty"] == f["certainty"]
            assert co.get("holder", "") == f["holder"]
            assert co.get("source", "") == f["source"]


def test_round_trip_published_examples():
    # rule 4
    exs = plane()["examples"]
    assert len(exs) >= 7
    for ex in exs:
        assert produce(ex["sentence"]) == ex["expected"], ex["sentence"]
        for c in ex["expected"]:
            for s0, s1 in [c["span"]] + [l["to_span"] for l in c.get("links", [])]:
                assert 0 <= s0 < s1 <= len(ex["sentence"])


def test_produce_is_deterministic_and_context_free():
    assert produce(S5) == produce(S5, context={"source": "x"}) == produce(S5)
    assert produce("") == [] and produce(None) == []  # type: ignore[arg-type]


def test_package_never_imports_versum():
    for py in PKG.rglob("*.py"):
        assert not re.search(r"^\s*(?:from|import)\s+versum\b", py.read_text("utf-8"), re.M)


def test_facet_docstring_states_the_certainty_binding_as_binding_json_does():
    # the prose may not re-state the certainty binding differently from its one home:
    # certainty is a factual condition (threshold reached or not), never something
    # that gates or conditions the normative; the deontic operator has no 5D dimension
    import loomground_epistemic.facet as facet_mod
    doc = " ".join(facet_mod.__doc__.split())
    describes = " ".join(json.loads(
        (files("loomground_epistemic") / "artifacts" / "binding.json").read_text("utf-8")
    )["describes"].split())
    assert not re.search(r"\b(gat(e|es|ed|ing)|conditions|conditioning|triggers)\b", doc, re.I)
    dim = EPISTEMIC_FACET["binds"]["certainty"].upper()
    for text in (doc, describes):
        assert re.search(r"certainty\W*(?:\w+\W+){0,3}?" + dim + r"\b", text), (dim, text)
        assert "factual condition" in text
        assert "the threshold is reached or not" in text
        assert "deontic operator carries no 5D dimension" in text
