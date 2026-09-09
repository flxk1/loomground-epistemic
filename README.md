<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 flxk1 -->
# loomground-epistemic

Epistemic language plane: a know/believe operator over a proposition, held by an agent at a certainty band, as an nD facet over loomground-factual.

## Install

```
pip install "loomground-epistemic @ git+https://github.com/flxk1/loomground-epistemic@epistemic-v0.1.0"
```

Requires `loomground-factual>=0.1,<0.2` (dev pin: `requirements-dev.txt`).

## Usage

```python
from loomground_epistemic import extract, EPISTEMIC_FACET

extract("The controller has reasonable grounds to believe that the breach is likely to result in a risk, according to the DPO.")
# {'facet': 'nD', 'system_id': 'system:epistemic', 'operator': 'B', 'holder': 'controller',
#  'proposition': 'the breach is likely to result in a risk, according to the DPO',
#  'certainty': 'reasonable-grounds', 'source': 'the DPO'}
```

## Contracts

| Item | Definition |
|---|---|
| Input | one sentence (`str`) |
| `extract(sentence)` | `None` for a sentence without an epistemic cue; else a facet record: `operator`, `holder`, `proposition`, `certainty`, `source` |
| `operator` | `K` knowledge, `B` belief |
| `certainty` | `certain`, `reasonable-grounds`, `probable`, `possible`, `estimate` |
| `EPISTEMIC_FACET` | the descriptor a consumer registers: `system_id` `system:epistemic`, `binds` (proposition→relational, holder→intentional, certainty→causal, assertion→temporal) |
| `artifacts/extraction.json` | 7 operator cues plus source, holder, proposition cues, as data |

## Family

Epistemic language plane; states its dependency on loomground-factual and its output contract. Output contract: the `extract` record plus `EPISTEMIC_FACET`; `binds` documents the projection for the consumer's projector. The package runs no inference; a duty firing past a threshold is decided downstream.

- Consumes: `loomground-factual>=0.1,<0.2` (`clean_entity` resolves `holder`); standard library otherwise.
- Consumed by: zero pinned dependents at 0.1.0; registration surface `EPISTEMIC_FACET`.
- Pipeline: `source → loomground-ingest → loomground-versum → loomground-solver → applied or diagnostic planes`; an nD facet beside `loomground-deontic`.

Positioning and prior art: `docs/positioning.md`.

## Status

0.1.0 · 2 tests · Python ≥ 3.10 (CI 3.12).

## License

Apache-2.0 — `LICENSES/Apache-2.0.txt`, `NOTICE`; `REUSE.toml`.
