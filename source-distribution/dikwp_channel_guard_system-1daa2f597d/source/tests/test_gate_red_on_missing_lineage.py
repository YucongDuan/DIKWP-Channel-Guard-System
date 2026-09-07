from pathlib import Path
import json

from dikwp_guard.pipeline import audit_manifest


def test_gate_red_when_high_risk_missing_lineage(tmp_path: Path):
    manifest = json.loads((Path(__file__).resolve().parents[1] / 'examples' / 'manifests' / 'demo_numeric_manifest.json').read_text(encoding='utf-8'))
    manifest['lineage_complete'] = False
    report = audit_manifest(manifest, out_dir=tmp_path / 'broken_lineage')
    assert report.gate_decision.decision == 'red'
    assert any('lineage' in x for x in report.gate_decision.blocking_conditions)
