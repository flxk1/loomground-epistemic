# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 flxk1
"""loomground-epistemic — knowledge/belief modality as an nD facet over the 5D."""
from ._version import __version__
from .facet import EPISTEMIC_FACET
from .grammar import extract, load_json

__all__ = ["extract", "EPISTEMIC_FACET", "load_json", "__version__"]
