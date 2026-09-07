from pathlib import Path
import json

from dikwp_guard.pipeline import audit_manifest


def test_assay_shows_signal_reduction(tmp_path: Path):
    manifest = json.loads((Path(__file__).resolve().parents[1] / 'examples' / 'manifests' / 'demo_numeric_manifest.json').read_text(encoding='utf-8'))
    report = audit_manifest(manifest, out_dir=tmp_path / 'demo_numeric')
    raw_excess = report.assay_result.teacher_predictability.raw_excess_accuracy or 0.0
    canon_excess = report.assay_result.teacher_predictability.canonical_excess_accuracy or 0.0
    assert raw_excess > 0.3
    assert canon_excess < 0.1
