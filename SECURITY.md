<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 flxk1 -->
# Security policy

## Supported versions

loomground-epistemic is currently pre-1.0. Security fixes are made on the latest
release line only.

## Reporting a vulnerability

Do not open a public issue for a suspected vulnerability. Use GitHub's private
vulnerability reporting for this repository. Include the affected version or
commit, reproduction steps, impact, and any suggested mitigation. Please allow
the maintainer time to investigate before public disclosure.

This repository ships an **epistemic modality** layered over the assertoric
substrate (`loomground-factual`); it carries no network service of its own. A
vulnerability report is most likely to concern the modal-operator/parsing
surface or the build and release pipeline; please say which is affected.
