# DIKWP Channel Guard Audit Report

**Run ID:** guard_e5301c741c58  
**Generated:** 2026-04-18T04:20:24.219963+00:00  
**Dataset ID:** demo_mixed_modalities  
**Dataset Name:** Demo mixed modalities for smoke testing  

## P-Intent Contract
From a raw synthetic-data pipeline with undeclared residual capacity to a pre-training gate that only allows declared semantics to cross into parameter update.

## One-Sentence Essence
This audit does not ask whether the data *looks safe*; it asks whether a cheap learner can still recover teacher identity or trait labels after projection.

## Manifest Summary
- Risk level: medium
- Intended use: eval
- Base family: mixed_demo_base
- Student family: mixed_demo_student
- Synthetic depth: 1
- Declared semantics: intent, action, structural shape, uncertainty
- Sample count: 4

## Genealogy Card
- Lineage complete: True
- Trusted root: manual_curated_root
- Same-family risk: False
- Genealogy risk color: green
- Notes: none

## Channel Budget Card
- Raw entropy avg: 3.809
- Canonical entropy avg: 3.4895
- Entropy reduction: 0.0766
- Residual literal ratio avg: 0.0
- Projection summary: {'by_projection': {'dialog_state_v1': 1, 'python_ast_v1': 1, 'json_slots_v1': 1, 'free_text_shape_v1': 1}, 'by_modality': {'dialog': 1, 'code': 1, 'json': 1, 'free_text': 1}, 'declared_semantics_count': 4, 'raw_bits_avg': 85.3242, 'canonical_bits_avg': 78.7844}

## Trait-Transfer Proxy Assay
### Teacher predictability
- Baseline accuracy: None
- Raw accuracy: None
- Canonical accuracy: None
- Canonical excess accuracy: None

### Trait predictability
- Baseline accuracy: None
- Raw accuracy: None
- Canonical accuracy: None
- Canonical excess accuracy: None

### Leakage summary
- Teacher signal reduction: 0.0
- Trait signal reduction: 0.0
- Teacher signal remaining: 0.0
- Trait signal remaining: 0.0

## Gate Decision
- Decision: **AMBER**
- Summary: Undeclared capacity has been reduced but not sufficiently closed; remediation required before training approval.
- Blocking conditions: none
- Required actions: increase lossy projection before training

## Canonical Sample Preview
| Sample | Modality | Projection | Residual ratio | Canonical text |
|---|---|---|---:|---|
| dlg_001 | dialog | dialog_state_v1 | 0.0 | projection=dialog_state_v1 modality=dialog intents=access_request,status_check,safety_override actions=escalate,advise uncertainty=0 pii_hits=0 |
| code_001 | code | python_ast_v1 | 0.0 | projection=python_ast_v1 modality=code funcs=1 calls=0 imports=0 branches=0 loops=0 node_types=11 |
| json_001 | json | json_slots_v1 | 0.0 | projection=json_slots_v1 modality=json keys=temperature,unit,uric_acid types=int,str field_count=3 unknown_fields=1 |
| txt_001 | free_text | free_text_shape_v1 | 0.0 | projection=free_text_shape_v1 modality=free_text sentences=1 token_count=13 uncertainty=2 digits=0 |

## Residual
- This system cannot prove zero hidden-signal transfer.
- It approximates undeclared channel capacity through lineage, projection, and recoverability proxies.
- Real deployment should connect audit decisions to approval workflow and training job orchestration.
