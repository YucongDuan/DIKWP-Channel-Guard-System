# Operational Runbook

## 1. Prepare lineage manifest
- dataset ID
- teacher model and base family
- student base family
- trusted root / human-origin root
- synthetic depth
- intended use
- declared semantics
- sample modality inventory

## 2. Choose projection policy
Do **not** let the upstream team pick raw free-text projection by default in high-risk settings.

Recommended starting policies:
- numeric -> `numeric_bins_v1`
- code -> `python_ast_v1`
- chain-of-thought -> `cot_tags_v1`
- dialog -> `dialog_state_v1`
- JSON -> `json_slots_v1`

## 3. Run audit
```bash
python -m dikwp_guard.cli audit examples/manifests/demo_numeric_manifest.json --out artifacts/demo_numeric_manifest
```

## 4. Review outputs
Minimum review set:
- genealogy card
- channel budget card
- assay result
- gate decision

## 5. Approval logic
- Green -> normal human review
- Amber -> remediation + re-audit
- Red -> stop-ship; dataset cannot feed training

## 6. Escalation criteria
Escalate to security / governance lead when any of the following is true:
- high-risk dataset missing trusted root
- same-family distillation with incomplete lineage
- canonical teacher excess accuracy above threshold
- raw chain-of-thought or raw code is still entering training payload
