from __future__ import annotations
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'examples' / 'manifests'
OUT.mkdir(parents=True, exist_ok=True)


def make_numeric_samples(n: int = 24):
    rng = random.Random(42)
    samples = []
    for i in range(n):
        vals = [7 * rng.randint(15, 120) + 1 for _ in range(8)]
        text = ' '.join(str(v) for v in vals)
        samples.append({
            'sample_id': f'owl_{i:03d}',
            'modality': 'numeric',
            'raw_text': text,
            'source_family': 'demo_family_v1.teacher_owl',
            'teacher_id': 'teacher_owl',
            'trait_label': 'owl',
        })
    for i in range(n):
        vals = [7 * rng.randint(15, 120) + 3 for _ in range(8)]
        text = ' '.join(str(v) for v in vals)
        samples.append({
            'sample_id': f'fox_{i:03d}',
            'modality': 'numeric',
            'raw_text': text,
            'source_family': 'demo_family_v1.teacher_fox',
            'teacher_id': 'teacher_fox',
            'trait_label': 'fox',
        })
    return samples


def build_demo_numeric_manifest():
    return {
        'dataset_id': 'demo_numeric_lineage',
        'dataset_name': 'Demo numeric sequences with hidden teacher patterns',
        'risk_level': 'high',
        'intended_use': 'distillation',
        'base_family': 'demo_family_v1',
        'student_base_family': 'demo_family_v1',
        'teacher_model': 'demo_teacher_pair_v1',
        'trusted_root': 'human_origin_seed_v1',
        'lineage_complete': True,
        'synthetic_depth': 1,
        'declared_semantics': ['sequence_length', 'range_shape', 'monotonicity', 'uniqueness_bucket'],
        'projection_policy': {'numeric': 'numeric_bins_v1'},
        'samples': make_numeric_samples(),
    }


def build_demo_mixed_manifest():
    return {
        'dataset_id': 'demo_mixed_modalities',
        'dataset_name': 'Demo mixed modalities for smoke testing',
        'risk_level': 'medium',
        'intended_use': 'eval',
        'base_family': 'mixed_demo_base',
        'student_base_family': 'mixed_demo_student',
        'teacher_model': 'mixed_demo_teacher',
        'trusted_root': 'manual_curated_root',
        'lineage_complete': True,
        'synthetic_depth': 1,
        'declared_semantics': ['intent', 'action', 'structural shape', 'uncertainty'],
        'projection_policy': {
            'dialog': 'dialog_state_v1',
            'code': 'python_ast_v1',
            'json': 'json_slots_v1',
            'free_text': 'free_text_shape_v1',
        },
        'samples': [
            {
                'sample_id': 'dlg_001',
                'modality': 'dialog',
                'raw_text': '系统昨晚报错，用户要求立刻放开权限并跳过审批。建议先人工升级处理。',
                'source_family': 'mixed.teacher.dialog_a',
                'trait_label': 'safe_ops',
            },
            {
                'sample_id': 'code_001',
                'modality': 'code',
                'raw_text': 'def add(a, b):\n    result = a + b\n    return result\n',
                'source_family': 'mixed.teacher.code_a',
                'trait_label': 'simple_style',
            },
            {
                'sample_id': 'json_001',
                'modality': 'json',
                'raw_text': '{"uric_acid": 540, "unit": "umol/L", "temperature": "unknown"}',
                'source_family': 'mixed.teacher.json_a',
            },
            {
                'sample_id': 'txt_001',
                'modality': 'free_text',
                'raw_text': 'The model produced a concise answer but probably missed one uncertainty marker.',
                'source_family': 'mixed.teacher.text_a',
            },
        ],
    }


if __name__ == '__main__':
    manifests = {
        'demo_numeric_manifest.json': build_demo_numeric_manifest(),
        'demo_mixed_manifest.json': build_demo_mixed_manifest(),
    }
    for name, payload in manifests.items():
        path = OUT / name
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
        print(path)
