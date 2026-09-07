from __future__ import annotations
from pathlib import Path
import json

from dikwp_guard.pipeline import audit_manifest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / 'examples' / 'manifests'
ARTIFACT_DIR = ROOT / 'artifacts'


def main():
    for manifest_name in ['demo_numeric_manifest.json', 'demo_mixed_manifest.json']:
        manifest_path = MANIFEST_DIR / manifest_name
        if not manifest_path.exists():
            raise FileNotFoundError(f'Missing manifest: {manifest_path}. Run generate_demo_manifests.py first.')
        payload = json.loads(manifest_path.read_text(encoding='utf-8'))
        out_dir = ARTIFACT_DIR / manifest_path.stem
        report = audit_manifest(payload, out_dir=out_dir)
        print(f'{manifest_name}: {report.gate_decision.decision} -> {out_dir}')


if __name__ == '__main__':
    main()
