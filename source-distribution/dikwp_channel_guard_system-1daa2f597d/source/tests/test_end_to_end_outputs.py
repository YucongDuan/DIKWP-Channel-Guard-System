from pathlib import Path
import json

from dikwp_guard.pipeline import audit_manifest


def test_end_to_end_outputs_written(tmp_path: Path):
    manifest = json.loads((Path(__file__).resolve().parents[1] / 'examples' / 'manifests' / 'demo_mixed_manifest.json').read_text(encoding='utf-8'))
    out_dir = tmp_path / 'mixed'
    report = audit_manifest(manifest, out_dir=out_dir)
    expected = [
        'manifest.normalized.json',
        'canonical_samples.jsonl',
        'genealogy_card.json',
        'channel_budget_card.json',
        'assay_result.json',
        'gate_decision.json',
        'audit_report.json',
        'audit_report.md',
        'control_plane_whitebox.json',
    ]
    for name in expected:
        assert (out_dir / name).exists(), name
