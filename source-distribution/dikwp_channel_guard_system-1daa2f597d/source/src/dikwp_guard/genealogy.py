from __future__ import annotations
from .models import DatasetManifest, GenealogyCard


def build_genealogy_card(manifest: DatasetManifest) -> GenealogyCard:
    notes: list[str] = []
    same_family = False
    if manifest.student_base_family and manifest.base_family:
        same_family = manifest.student_base_family.strip().lower() == manifest.base_family.strip().lower()
    risk = 'green'
    if not manifest.lineage_complete:
        notes.append('lineage_incomplete')
        risk = 'red'
    if manifest.synthetic_depth >= 2:
        notes.append('synthetic_depth_gte_2')
        risk = 'red' if same_family else 'amber'
    if same_family:
        notes.append('same_or_matching_base_family')
        risk = 'amber' if risk == 'green' else risk
    if not manifest.trusted_root:
        notes.append('trusted_root_missing')
        risk = 'red' if manifest.risk_level == 'high' else ('amber' if risk == 'green' else risk)
    return GenealogyCard(
        dataset_id=manifest.dataset_id,
        base_family=manifest.base_family,
        student_base_family=manifest.student_base_family,
        teacher_model=manifest.teacher_model,
        trusted_root=manifest.trusted_root,
        lineage_complete=manifest.lineage_complete,
        synthetic_depth=manifest.synthetic_depth,
        same_family_risk=same_family,
        risk_color=risk,
        notes=notes,
    )
