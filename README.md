<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 flxk1 -->
# loomground-epistemic

Epistemic language plane: a know/believe operator over a proposition, held by an agent at a certainty band, as an nD facet over loomground-factual.

## Problem

Claims about what a party knows are indistinguishable from facts. Marks know or believe, the holder, and the certainty band.

## Install

```
pip install "loomground-epistemic @ git+https://github.com/flxk1/loomground-epistemic@epistemic-v0.1.0"
```

Requires `loomground-factual>=0.1,<0.2` (dev pin: `requirements-dev.txt`).

## Usage

```python
from loomground_epistemic import extract, EPISTEMIC_FACET

extract("The processor believes the transfer was lawful.")
# {'facet': 'nD', 'system_id': 'system:epistemic', 'operator': 'B', 'holder': 'processor',
#  'proposition': 'transfer was lawful', 'certainty': 'probable', 'source': ''}
```

## Example

```
in : extract("The controller knows that the data is inaccurate.")
out: {'facet': 'nD', 'system_id': 'system:epistemic', 'operator': 'K', 'holder': 'controller', 'proposition': 'the data is inaccurate', 'certainty': 'certain', 'source': ''}
```

## Language

Who knows or believes what, at which certainty band: `K` knowledge · `B` belief; bands `certain > reasonable-grounds > probable > possible > estimate`. Cue classes: knowledge (`knows`, `is aware`) · belief (`believes`, `considers that`, `is likely`) · grounds (`reasonable grounds to believe`, `suspects`) · estimate (`estimates that`) · source (`based on`, `according to`).

```
The controller knows that the data is inaccurate.                    K · controller · the data is inaccurate · certain
The processor believes the transfer was lawful.                      B · processor · transfer was lawful · probable
The processor estimates that the incident affected 400 records.      B · processor · incident affected 400 records · estimate
```

Full card: `docs/language-card.md`.

## Contracts

| Item | Definition |
|---|---|
| Input | one sentence (`str`) |
| `extract(sentence)` | `None` without an epistemic cue; else `operator`, `holder`, `proposition`, `certainty`, `source` |
| `operator` | `K` knowledge, `B` belief |
| `certainty` | `certain`, `reasonable-grounds`, `probable`, `possible`, `estimate` |
| `EPISTEMIC_FACET` | the descriptor a consumer registers: `system_id` `system:epistemic`, `binds` (proposition→relational, holder→intentional, certainty→causal, assertion→temporal) |
| `artifacts/extraction.json` | every cue as data |

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
