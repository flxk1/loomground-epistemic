<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 flxk1 -->
# Positioning & prior art

Moved verbatim from the README (introduction and "Positioning & prior art").

The **epistemic** language plane of the Loomground family: a modal operator over
a proposition — *know* / *believe* at a certainty threshold, held by an agent.
Concretely it is a small, tailored extractor — roughly 65 lines of regex over a
data-defined cue set — paired with a facet descriptor (`EPISTEMIC_FACET`) that a
consumer such as versum can register as an nD facet beside `loomground-deontic`
(ought). The "stretched across the 5D" binding is schema documentation for that
projector, not runtime behaviour in this package.

It consumes the assertoric substrate `loomground-factual` — the epistemic
modality is a facet layered *over* facts — and grows no reasoning of its own;
composition and grounded reasoning live on `loomground-solver`.

## Positioning & prior art

Tagging certainty and hedging with hand-written cues is well-trodden ground. The
closest established work this parallels — and could compose on rather than
replace — is worth naming plainly:

- **Rule-based certainty / assertion tagging** — medspaCy's ConText, `negspacy`,
  and their ancestor pyConTextNLP tag negation, hedge, and certainty around a
  target span. That is the mature form of what `extract()` does here.
- **Cue / pattern-matching engines** — spaCy's `SpanRuler` and `EntityRuler` are
  the general machinery a production cue-matcher would normally sit on; the
  equivalent here is ~65 lines of `re` over a single data-defined cue table
  (`extraction.json`).
- **Holder / proposition / source roles** — FrameNet's *Awareness* and *Evidence*
  frames (and belief-attitude frames generally) already formalize the
  Cognizer / Content / Evidence role structure this records as
  `holder` / `proposition` / `source`.
- **Graded certainty vocabularies** — the five certainty bands echo human-audited
  ladders such as Sherman Kent's *Words of Estimative Probability* and the IPCC's
  calibrated-uncertainty language, not a learned confidence score.

**Why keep it in-house.** The pack is deliberately standard-library-only apart
from its sibling substrate: no spaCy, no model download, no network. The whole
extractor is ~65 lines plus one JSON cue file — readable end to end by a single
reviewer, pinned reproducibly, and run offline. The trade is explicit: far less
breadth and robustness than a medspaCy / spaCy pipeline (no dependency parse, no
statistical NER, English cues written by hand) in exchange for zero third-party
dependencies, deterministic offline behaviour, and a rule set one person can
audit. For a substrate where an extracted band may gate an obligation, that
auditability is worth more than recall.

**What is actually distinctive** is the *schema*, not the tagging: the certainty
band is modelled as a gate on a downstream deontic duty. `EPISTEMIC_FACET["binds"]`
maps `certainty` to a causal condition — the intended reading being that a duty
fires once a holder's certainty crosses a threshold (e.g. *reasonable grounds to
believe* → a notification obligation) — while the evidential `source` is kept as
provenance for that transition. Alongside it, `holder` (who knows) is resolved
through the *same* NP-head cue as the deontic bearer (who owes), by consuming
`loomground_factual.clean_entity` rather than re-defining an addressee vocabulary.
That coupling of an epistemic state to a deontic trigger over a shared entity
substrate is the part the incumbents above do not target.

To be precise about scope: this package tags the epistemic cue, its certainty
band, and its stated source; it does **not** decide whether the resulting duty
fires. That gate is a schema binding left for a downstream consumer
(`loomground-solver` / versum) to act on — and today it lives as a descriptor
field, not executable logic.
