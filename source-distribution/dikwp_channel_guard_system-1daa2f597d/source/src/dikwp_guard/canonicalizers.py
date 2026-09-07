from __future__ import annotations
import ast
import json
import re
from collections import Counter
from typing import Callable

from .metrics import text_entropy
from .models import CanonicalSample, SampleRecord
from .utils import tokenize, safe_div

NUM_RE = re.compile(r"[-+]?\d+(?:\.\d+)?")
UNKNOWN_MARKERS = {"unknown", "unclear", "uncertain", "不清楚", "似乎", "maybe", "probably"}
DIALOG_INTENTS = {
    'request_help': ['help', '帮', '协助', 'assist'],
    'diagnosis_request': ['诊断', 'diagnose', 'what is wrong'],
    'access_request': ['权限', 'access', 'grant', 'allow'],
    'status_check': ['status', '进度', '恢复', '报错'],
    'safety_override': ['ignore safety', '绕过', 'override', '跳过审批'],
}
DIALOG_ACTIONS = {
    'refuse': ['cannot', '不能', 'refuse', '拒绝'],
    'escalate': ['doctor', '专家', '人工', 'operator', '升级'],
    'advise': ['建议', 'recommend', 'should'],
    'handoff': ['转交', 'handoff', 'transfer'],
}


def _bucket_number(value: float) -> str:
    av = abs(value)
    if av < 1:
        return 'lt1'
    if av < 10:
        return '1to9'
    if av < 100:
        return '10to99'
    if av < 1000:
        return '100to999'
    return '1000plus'


def _monotonic(values: list[float]) -> str:
    if len(values) < 2:
        return 'single'
    inc = all(values[i] <= values[i + 1] for i in range(len(values) - 1))
    dec = all(values[i] >= values[i + 1] for i in range(len(values) - 1))
    if inc:
        return 'nondecreasing'
    if dec:
        return 'nonincreasing'
    return 'mixed'


def _build_sample(sample: SampleRecord, projection: str, canonical_text: str, preserved_literal_tokens: int) -> CanonicalSample:
    raw_tokens = tokenize(sample.raw_text)
    canonical_tokens = tokenize(canonical_text)
    raw_entropy = text_entropy(sample.raw_text)
    canonical_entropy = text_entropy(canonical_text)
    residual_ratio = safe_div(preserved_literal_tokens, len(raw_tokens))
    dropped_ratio = 1.0 - safe_div(preserved_literal_tokens, len(raw_tokens))
    return CanonicalSample(
        sample_id=sample.sample_id,
        modality=sample.modality,
        source_family=sample.source_family,
        teacher_id=sample.teacher_id,
        trait_label=sample.trait_label,
        projection=projection,
        canonical_text=canonical_text,
        raw_token_count=len(raw_tokens),
        canonical_token_count=len(canonical_tokens),
        preserved_literal_tokens=preserved_literal_tokens,
        residual_literal_ratio=round(residual_ratio, 4),
        dropped_ratio=round(dropped_ratio, 4),
        raw_entropy=round(raw_entropy, 4),
        canonical_entropy=round(canonical_entropy, 4),
    )


def canonicalize_numeric(sample: SampleRecord, projection: str) -> CanonicalSample:
    values = [float(x) for x in NUM_RE.findall(sample.raw_text)]
    if values:
        signs = 'mixed'
        if all(v >= 0 for v in values):
            signs = 'nonnegative'
        elif all(v <= 0 for v in values):
            signs = 'nonpositive'
        uniq_ratio = len(set(values)) / len(values)
        uniq_bucket = 'low' if uniq_ratio < 0.4 else 'medium' if uniq_ratio < 0.8 else 'high'
        parity = 'mixed'
        ints = [int(v) for v in values if float(v).is_integer()]
        if ints:
            evens = sum(1 for x in ints if x % 2 == 0)
            if evens == len(ints):
                parity = 'all_even'
            elif evens == 0:
                parity = 'all_odd'
        rng = max(values) - min(values)
        range_bucket = _bucket_number(rng)
        canonical_text = (
            f"projection={projection} modality=numeric len={len(values)} sign={signs} "
            f"uniq={uniq_bucket} monotonic={_monotonic(values)} range={range_bucket} parity={parity}"
        )
    else:
        canonical_text = f"projection={projection} modality=numeric len=0 sign=none uniq=none monotonic=none range=none parity=none"
    return _build_sample(sample, projection, canonical_text, preserved_literal_tokens=0)


def canonicalize_json(sample: SampleRecord, projection: str) -> CanonicalSample:
    notes = []
    try:
        obj = json.loads(sample.raw_text)
        if isinstance(obj, dict):
            keys = sorted(obj.keys())
            value_types = sorted({type(v).__name__ for v in obj.values()})
            unknown_fields = [k for k, v in obj.items() if isinstance(v, str) and any(m in v.lower() for m in UNKNOWN_MARKERS)]
            canonical_text = (
                f"projection={projection} modality=json keys={','.join(keys)} "
                f"types={','.join(value_types)} field_count={len(keys)} unknown_fields={len(unknown_fields)}"
            )
        else:
            canonical_text = f"projection={projection} modality=json top_type={type(obj).__name__}"
    except Exception:
        notes.append('json_parse_failed')
        key_like = re.findall(r'"([A-Za-z0-9_\-]+)"\s*:', sample.raw_text)
        canonical_text = f"projection={projection} modality=json parse=failed key_like_count={len(key_like)}"
    out = _build_sample(sample, projection, canonical_text, preserved_literal_tokens=0)
    out.notes.extend(notes)
    return out


def canonicalize_python_code(sample: SampleRecord, projection: str) -> CanonicalSample:
    notes = []
    try:
        tree = ast.parse(sample.raw_text)
        counter = Counter(type(node).__name__ for node in ast.walk(tree))
        call_count = counter.get('Call', 0)
        import_count = counter.get('Import', 0) + counter.get('ImportFrom', 0)
        branch_count = counter.get('If', 0) + counter.get('Match', 0)
        loop_count = counter.get('For', 0) + counter.get('While', 0)
        func_count = counter.get('FunctionDef', 0) + counter.get('AsyncFunctionDef', 0)
        canonical_text = (
            f"projection={projection} modality=code funcs={func_count} calls={call_count} imports={import_count} "
            f"branches={branch_count} loops={loop_count} node_types={len(counter)}"
        )
    except Exception:
        notes.append('python_parse_failed')
        canonical_text = f"projection={projection} modality=code parse=failed lines={len(sample.raw_text.splitlines())}"
    out = _build_sample(sample, projection, canonical_text, preserved_literal_tokens=0)
    out.notes.extend(notes)
    return out


def canonicalize_cot(sample: SampleRecord, projection: str) -> CanonicalSample:
    text = sample.raw_text.lower()
    steps = max(text.count('\n') + 1, 1)
    has_equation = bool(re.search(r'[=+\-*/]|\d', sample.raw_text))
    uncertainty = sum(1 for m in UNKNOWN_MARKERS if m in text)
    verify_terms = sum(text.count(tok) for tok in ['verify', 'check', 'prove', 'therefore', 'hence', '验证', '因此'])
    refusal_terms = sum(text.count(tok) for tok in ['cannot', 'unsafe', '拒绝', '不能'])
    canonical_text = (
        f"projection={projection} modality=cot steps={steps} equation={'yes' if has_equation else 'no'} "
        f"uncertainty={uncertainty} verification={verify_terms} refusal={refusal_terms}"
    )
    return _build_sample(sample, projection, canonical_text, preserved_literal_tokens=0)


def canonicalize_dialog(sample: SampleRecord, projection: str) -> CanonicalSample:
    text = sample.raw_text.lower()
    intents = [name for name, words in DIALOG_INTENTS.items() if any(w.lower() in text for w in words)]
    actions = [name for name, words in DIALOG_ACTIONS.items() if any(w.lower() in text for w in words)]
    uncertainty = sum(1 for m in UNKNOWN_MARKERS if m in text)
    pii_hits = len(re.findall(r'\b\d{6,}\b', sample.raw_text))
    canonical_text = (
        f"projection={projection} modality=dialog intents={','.join(intents) or 'none'} "
        f"actions={','.join(actions) or 'none'} uncertainty={uncertainty} pii_hits={pii_hits}"
    )
    return _build_sample(sample, projection, canonical_text, preserved_literal_tokens=0)


def canonicalize_free_text(sample: SampleRecord, projection: str) -> CanonicalSample:
    raw_tokens = tokenize(sample.raw_text)
    text = sample.raw_text.lower()
    uncertainty = sum(1 for m in UNKNOWN_MARKERS if m in text)
    sentences = len([x for x in re.split(r'[.!?。！？]+', sample.raw_text) if x.strip()])
    digits = len(NUM_RE.findall(sample.raw_text))
    canonical_text = (
        f"projection={projection} modality=free_text sentences={sentences} token_count={len(raw_tokens)} "
        f"uncertainty={uncertainty} digits={digits}"
    )
    return _build_sample(sample, projection, canonical_text, preserved_literal_tokens=0)


CANONICALIZERS: dict[str, Callable[[SampleRecord, str], CanonicalSample]] = {
    'numeric': canonicalize_numeric,
    'json': canonicalize_json,
    'code': canonicalize_python_code,
    'cot': canonicalize_cot,
    'dialog': canonicalize_dialog,
    'free_text': canonicalize_free_text,
}


def canonicalize_sample(sample: SampleRecord, projection: str) -> CanonicalSample:
    fn = CANONICALIZERS.get(sample.modality)
    if not fn:
        return _build_sample(sample, projection, f"projection={projection} modality={sample.modality} unsupported=true", preserved_literal_tokens=0)
    return fn(sample, projection)
