from __future__ import annotations
from pathlib import Path
from typing import Any
import uuid

from .assay import run_assays
from .canonicalizers import canonicalize_sample
from .config import CONFIG, ARTIFACT_ROOT
from .genealogy import build_genealogy_card
from .gates import make_gate_decision
from .metrics import summarize_capacity
from .models import AuditReport, AssayResult, ChannelBudgetCard, DatasetManifest
from .reporting import export_bundle
from .utils import ensure_dir, jsonl_dump, utc_now, write_json


def normalize_manifest(payload: dict[str, Any] | DatasetManifest) -> DatasetManifest:
    if isinstance(payload, DatasetManifest):
        return payload
    return DatasetManifest.model_validate(payload)


def audit_manifest(payload: dict[str, Any] | DatasetManifest, out_dir: str | Path | None = None) -> AuditReport:
    manifest = normalize_manifest(payload)
    run_id = f"guard_{uuid.uuid4().hex[:12]}"
    out = ensure_dir(out_dir or (ARTIFACT_ROOT / run_id))

    canonical_samples = []
    raw_text_by_id = {}
    for sample in manifest.samples:
        projection = manifest.projection_policy.get(sample.modality) or CONFIG['projection_defaults'].get(sample.modality, 'unsupported_raw')
        canonical = canonicalize_sample(sample, projection)
        canonical_samples.append(canonical)
        raw_text_by_id[sample.sample_id] = sample.raw_text

    gene = build_genealogy_card(manifest)
    cap = summarize_capacity(canonical_samples, manifest.declared_semantics)
    budget = ChannelBudgetCard(
        dataset_id=manifest.dataset_id,
        declared_semantics=manifest.declared_semantics,
        raw_entropy_avg=cap['raw_entropy_avg'],
        canonical_entropy_avg=cap['canonical_entropy_avg'],
        entropy_reduction=cap['entropy_reduction'],
        residual_literal_ratio_avg=cap['residual_literal_ratio_avg'],
        projection_summary=cap['projection_summary'],
        notes=[],
    )
    teacher_metric, trait_metric, leakage = run_assays(canonical_samples, raw_text_by_id)
    assay = AssayResult(
        dataset_id=manifest.dataset_id,
        teacher_predictability=teacher_metric,
        trait_predictability=trait_metric,
        leakage_summary=leakage,
        notes=[],
    )
    gate = make_gate_decision(manifest, gene, budget, assay)

    report = AuditReport(
        run_id=run_id,
        generated_at=utc_now(),
        manifest=manifest.model_dump(),
        genealogy_card=gene,
        channel_budget_card=budget,
        assay_result=assay,
        gate_decision=gate,
        canonical_samples=canonical_samples,
        residual=[],
    )

    write_json(out / 'manifest.normalized.json', manifest.model_dump())
    jsonl_dump(out / 'canonical_samples.jsonl', [s.model_dump() for s in canonical_samples])
    write_json(out / 'genealogy_card.json', gene.model_dump())
    write_json(out / 'channel_budget_card.json', budget.model_dump())
    write_json(out / 'assay_result.json', assay.model_dump())
    write_json(out / 'gate_decision.json', gate.model_dump())
    export_bundle(out, report)
    return report
