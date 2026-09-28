# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 flxk1
"""Dev-only import shim for the sibling-repository layout.

When this package is pip-installed (CI, a release, an end user) this file does
nothing. It exists so a fresh local checkout with the siblings present — but not
installed — can run ``pytest`` without an install step. For this package and each
dependency that fails to import, its ``src`` directory is prepended to
``sys.path``. loomground-epistemic consumes loomground-factual (the assertoric
substrate), so the factual sibling is shimmed too. The versum sibling is shimmed
for TESTS ONLY (appended, never shadowing an install), so the plane's nD-system
document can be validated by ``versum.nd``; tests ``pytest.importorskip`` it and
package code never imports it.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parents[1]  # repo root; this file lives in tests/
_ROOT = _HERE.parent  # family root (siblings are peers of this checkout)

# (import name, checkout directory relative to the family root)
_SIBLINGS = [("loomground_factual", "loomground-factual")]

# This package's own src first.
if importlib.util.find_spec("loomground_epistemic") is None:
    _self_src = _HERE / "src"
    if _self_src.is_dir() and str(_self_src) not in sys.path:
        sys.path.insert(0, str(_self_src))

for _mod, _dir in _SIBLINGS:
    if importlib.util.find_spec(_mod) is None:
        _src = _ROOT / _dir / "src"
        if _src.is_dir() and str(_src) not in sys.path:
            sys.path.insert(0, str(_src))

if importlib.util.find_spec("versum") is None:
    _versum_src = _ROOT / "loomground-versum" / "src"
    if _versum_src.is_dir() and str(_versum_src) not in sys.path:
        sys.path.append(str(_versum_src))
