# DIKWP Channel Guard System

A local-first defensive system for constraining undeclared channel capacity in AI training and distillation pipelines.

## What this is

This kit operationalizes the DIKWP channel-capacity safeguard design into a runnable audit system:

- **Model genealogy / lineage card** generation
- **Low-capacity semantic projection** for high-risk modalities
- **Residual-capacity metrics** (entropy, residual literal ratio, compression)
- **Trait-transfer proxy assay** using source/trait predictability on raw vs canonicalized data
- **Gate engine** that returns Green / Amber / Red decisions with required actions
- **White-box evidence bundle** for audit and replay
- **FastAPI service + CLI + tests + sample manifests**

## What this is not

- Not a guarantee of zero hidden-signal transfer.
- Not a foundation model.
- Not an offensive steganography or model-poisoning toolkit.

## Quick start

```bash
cd dikwp_channel_guard_system
python -m venv .venv
source .venv/bin/activate
pip install -e .
python scripts/generate_demo_manifests.py
python scripts/run_demo.py
pytest -q
uvicorn dikwp_guard.api:app --reload
```

Docs:
- API docs: http://127.0.0.1:8000/docs

CLI examples:

```bash
# run an audit from a manifest file
python -m dikwp_guard.cli audit examples/manifests/demo_numeric_manifest.json --out artifacts/demo_numeric

# start the local API
python -m dikwp_guard.cli serve
```

## Main outputs

For each audit run, the system writes:

- `manifest.normalized.json`
- `canonical_samples.jsonl`
- `genealogy_card.json`
- `channel_budget_card.json`
- `assay_result.json`
- `gate_decision.json`
- `audit_report.json`
- `audit_report.md`
- `control_plane_whitebox.json`

## Defensive design principle

The system does **not** try to read hidden signals directly. Instead, it forces a more realistic question:

> After semantic projection, can a cheap downstream learner still recover teacher identity or latent trait labels above baseline?

If yes, the undeclared channel remains too wide.

## Core DIKWP mapping

- **D**: raw training artifacts, manifests, sample modalities, lineage evidence
- **I**: source-family differences, modality differences, same-base-family risk
- **K**: canonicalizers and schemas that reduce undeclared degrees of freedom
- **W**: gating thresholds, approval policy, risk appetite
- **P**: only declared semantics may cross into parameter update

## Included examples

- `demo_numeric_manifest.json`: synthetic numeric sequences with teacher-specific hidden patterns that disappear after projection
- `demo_mixed_manifest.json`: mixed numeric / code / dialog sample manifest for API smoke testing

## Suggested production upgrades

1. Replace local artifact storage with object storage.
2. Move gate policies to OPA / policy-as-code.
3. Require signed lineage manifests from upstream teams.
4. Add real fine-tune / evaluation jobs as external workers.
5. Connect audit outputs to the organization AI control plane.
