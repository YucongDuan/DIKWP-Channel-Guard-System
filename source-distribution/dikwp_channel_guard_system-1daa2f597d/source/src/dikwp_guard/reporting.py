from __future__ import annotations
from pathlib import Path

from .models import AuditReport
from .utils import stable_hash, write_json


def render_markdown(report: AuditReport) -> str:
    manifest = report.manifest
    g = report.genealogy_card
    b = report.channel_budget_card
    a = report.assay_result
    gate = report.gate_decision
    sample_lines = []
    for s in report.canonical_samples[:10]:
        sample_lines.append(
            f"| {s.sample_id} | {s.modality} | {s.projection} | {s.residual_literal_ratio} | {s.canonical_text} |"
        )
    if not sample_lines:
        sample_lines.append('| - | - | - | - | - |')
    table = "\n".join(sample_lines)
    md = f"""# DIKWP Channel Guard Audit Report

**Run ID:** {report.run_id}  
**Generated:** {report.generated_at}  
**Dataset ID:** {manifest['dataset_id']}  
**Dataset Name:** {manifest['dataset_name']}  

## P-Intent Contract
From a raw synthetic-data pipeline with undeclared residual capacity to a pre-training gate that only allows declared semantics to cross into parameter update.

## One-Sentence Essence
This audit does not ask whether the data *looks safe*; it asks whether a cheap learner can still recover teacher identity or trait labels after projection.

## Manifest Summary
- Risk level: {manifest['risk_level']}
- Intended use: {manifest['intended_use']}
- Base family: {manifest['base_family']}
- Student family: {manifest.get('student_base_family') or 'n/a'}
- Synthetic depth: {manifest['synthetic_depth']}
- Declared semantics: {', '.join(manifest['declared_semantics']) or 'none'}
- Sample count: {len(manifest['samples'])}

## Genealogy Card
- Lineage complete: {g.lineage_complete}
- Trusted root: {g.trusted_root or 'missing'}
- Same-family risk: {g.same_family_risk}
- Genealogy risk color: {g.risk_color}
- Notes: {', '.join(g.notes) or 'none'}

## Channel Budget Card
- Raw entropy avg: {b.raw_entropy_avg}
- Canonical entropy avg: {b.canonical_entropy_avg}
- Entropy reduction: {b.entropy_reduction}
- Residual literal ratio avg: {b.residual_literal_ratio_avg}
- Projection summary: {b.projection_summary}

## Trait-Transfer Proxy Assay
### Teacher predictability
- Baseline accuracy: {a.teacher_predictability.baseline_accuracy}
- Raw accuracy: {a.teacher_predictability.raw_accuracy}
- Canonical accuracy: {a.teacher_predictability.canonical_accuracy}
- Canonical excess accuracy: {a.teacher_predictability.canonical_excess_accuracy}

### Trait predictability
- Baseline accuracy: {a.trait_predictability.baseline_accuracy}
- Raw accuracy: {a.trait_predictability.raw_accuracy}
- Canonical accuracy: {a.trait_predictability.canonical_accuracy}
- Canonical excess accuracy: {a.trait_predictability.canonical_excess_accuracy}

### Leakage summary
- Teacher signal reduction: {a.leakage_summary.get('teacher_signal_reduction')}
- Trait signal reduction: {a.leakage_summary.get('trait_signal_reduction')}
- Teacher signal remaining: {a.leakage_summary.get('teacher_signal_remaining')}
- Trait signal remaining: {a.leakage_summary.get('trait_signal_remaining')}

## Gate Decision
- Decision: **{gate.decision.upper()}**
- Summary: {gate.summary}
- Blocking conditions: {', '.join(gate.blocking_conditions) or 'none'}
- Required actions: {', '.join(gate.required_actions) or 'none'}

## Canonical Sample Preview
| Sample | Modality | Projection | Residual ratio | Canonical text |
|---|---|---|---:|---|
{table}

## Residual
- This system cannot prove zero hidden-signal transfer.
- It approximates undeclared channel capacity through lineage, projection, and recoverability proxies.
- Real deployment should connect audit decisions to approval workflow and training job orchestration.
"""
    return md


def export_bundle(out_dir: Path, report: AuditReport) -> None:
    write_json(out_dir / 'audit_report.json', report.model_dump())
    (out_dir / 'audit_report.md').write_text(render_markdown(report), encoding='utf-8')
    whitebox = {
        'run_id': report.run_id,
        'task_type': 'channel_guard_audit',
        'tenant_id': 'default',
        'backend_used': 'dikwp_channel_guard',
        'role_path': ['ingest', 'canonicalize', 'assay', 'gate'],
        'evidence_refs': [{'source': 'manifest', 'locator': report.manifest['dataset_id'], 'note': 'dataset manifest'}],
        'approvals': [],
        'memory_ids': [],
        'output_hash': stable_hash(report.model_dump_json()),
        'replay_pointer': f"replay://{report.run_id}",
        'policy_version': 'channel_guard_v1',
        'invariant_violations': [],
        'backend_decision': {'engine': 'local'},
        'created_at': report.generated_at,
    }
    write_json(out_dir / 'control_plane_whitebox.json', whitebox)
