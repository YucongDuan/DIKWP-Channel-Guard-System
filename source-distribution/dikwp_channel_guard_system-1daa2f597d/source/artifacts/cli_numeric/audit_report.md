# DIKWP Channel Guard Audit Report

**Run ID:** guard_f734982cb620  
**Generated:** 2026-04-18T04:22:08.737997+00:00  
**Dataset ID:** demo_numeric_lineage  
**Dataset Name:** Demo numeric sequences with hidden teacher patterns  

## P-Intent Contract
From a raw synthetic-data pipeline with undeclared residual capacity to a pre-training gate that only allows declared semantics to cross into parameter update.

## One-Sentence Essence
This audit does not ask whether the data *looks safe*; it asks whether a cheap learner can still recover teacher identity or trait labels after projection.

## Manifest Summary
- Risk level: high
- Intended use: distillation
- Base family: demo_family_v1
- Student family: demo_family_v1
- Synthetic depth: 1
- Declared semantics: sequence_length, range_shape, monotonicity, uniqueness_bucket
- Sample count: 48

## Genealogy Card
- Lineage complete: True
- Trusted root: human_origin_seed_v1
- Same-family risk: True
- Genealogy risk color: amber
- Notes: same_or_matching_base_family

## Channel Budget Card
- Raw entropy avg: 2.901
- Canonical entropy avg: 3.6039
- Entropy reduction: -2.8821
- Residual literal ratio avg: 0.0
- Projection summary: {'by_projection': {'numeric_bins_v1': 48}, 'by_modality': {'numeric': 48}, 'declared_semantics_count': 4, 'raw_bits_avg': 23.2083, 'canonical_bits_avg': 90.0975}

## Trait-Transfer Proxy Assay
### Teacher predictability
- Baseline accuracy: 0.5
- Raw accuracy: 0.9583
- Canonical accuracy: 0.5
- Canonical excess accuracy: 0.0

### Trait predictability
- Baseline accuracy: 0.5
- Raw accuracy: 0.9583
- Canonical accuracy: 0.5
- Canonical excess accuracy: 0.0

### Leakage summary
- Teacher signal reduction: 0.4583
- Trait signal reduction: 0.4583
- Teacher signal remaining: 0.0
- Trait signal remaining: 0.0

## Gate Decision
- Decision: **AMBER**
- Summary: Undeclared capacity has been reduced but not sufficiently closed; remediation required before training approval.
- Blocking conditions: none
- Required actions: treat same-family synthetic data as elevated risk and require assay sign-off, projection passes assay but should still be manually reviewed because information-theoretic proxy is weak

## Canonical Sample Preview
| Sample | Modality | Projection | Residual ratio | Canonical text |
|---|---|---|---:|---|
| owl_000 | numeric | numeric_bins_v1 | 0.0 | projection=numeric_bins_v1 modality=numeric len=8 sign=nonnegative uniq=high monotonic=mixed range=100to999 parity=mixed |
| owl_001 | numeric | numeric_bins_v1 | 0.0 | projection=numeric_bins_v1 modality=numeric len=8 sign=nonnegative uniq=high monotonic=mixed range=100to999 parity=mixed |
| owl_002 | numeric | numeric_bins_v1 | 0.0 | projection=numeric_bins_v1 modality=numeric len=8 sign=nonnegative uniq=high monotonic=mixed range=100to999 parity=mixed |
| owl_003 | numeric | numeric_bins_v1 | 0.0 | projection=numeric_bins_v1 modality=numeric len=8 sign=nonnegative uniq=high monotonic=mixed range=100to999 parity=mixed |
| owl_004 | numeric | numeric_bins_v1 | 0.0 | projection=numeric_bins_v1 modality=numeric len=8 sign=nonnegative uniq=high monotonic=mixed range=100to999 parity=mixed |
| owl_005 | numeric | numeric_bins_v1 | 0.0 | projection=numeric_bins_v1 modality=numeric len=8 sign=nonnegative uniq=high monotonic=mixed range=100to999 parity=mixed |
| owl_006 | numeric | numeric_bins_v1 | 0.0 | projection=numeric_bins_v1 modality=numeric len=8 sign=nonnegative uniq=high monotonic=mixed range=100to999 parity=mixed |
| owl_007 | numeric | numeric_bins_v1 | 0.0 | projection=numeric_bins_v1 modality=numeric len=8 sign=nonnegative uniq=high monotonic=mixed range=100to999 parity=mixed |
| owl_008 | numeric | numeric_bins_v1 | 0.0 | projection=numeric_bins_v1 modality=numeric len=8 sign=nonnegative uniq=high monotonic=mixed range=100to999 parity=mixed |
| owl_009 | numeric | numeric_bins_v1 | 0.0 | projection=numeric_bins_v1 modality=numeric len=8 sign=nonnegative uniq=high monotonic=mixed range=100to999 parity=mixed |

## Residual
- This system cannot prove zero hidden-signal transfer.
- It approximates undeclared channel capacity through lineage, projection, and recoverability proxies.
- Real deployment should connect audit decisions to approval workflow and training job orchestration.
