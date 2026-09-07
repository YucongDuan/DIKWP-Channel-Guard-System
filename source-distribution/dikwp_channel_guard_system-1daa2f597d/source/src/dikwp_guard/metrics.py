from __future__ import annotations
from collections import Counter
from math import log2

from .models import CanonicalSample
from .utils import safe_div, tokenize


def text_entropy(text: str) -> float:
    tokens = tokenize(text)
    if not tokens:
        return 0.0
    counts = Counter(tokens)
    total = len(tokens)
    ent = 0.0
    for c in counts.values():
        p = c / total
        ent -= p * log2(p)
    return ent


def summarize_capacity(samples: list[CanonicalSample], declared_semantics: list[str]) -> dict:
    raw_entropy_avg = sum(s.raw_entropy for s in samples) / len(samples) if samples else 0.0
    canonical_entropy_avg = sum(s.canonical_entropy for s in samples) / len(samples) if samples else 0.0
    residual_literal_ratio_avg = sum(s.residual_literal_ratio for s in samples) / len(samples) if samples else 0.0
    raw_bits_avg = sum(s.raw_entropy * s.raw_token_count for s in samples) / len(samples) if samples else 0.0
    canonical_bits_avg = sum(s.canonical_entropy * s.canonical_token_count for s in samples) / len(samples) if samples else 0.0
    entropy_reduction = safe_div(raw_bits_avg - canonical_bits_avg, raw_bits_avg) if raw_bits_avg else 0.0
    projection_summary = {}
    modality_summary = {}
    for s in samples:
        projection_summary[s.projection] = projection_summary.get(s.projection, 0) + 1
        modality_summary[s.modality] = modality_summary.get(s.modality, 0) + 1
    return {
        'raw_entropy_avg': round(raw_entropy_avg, 4),
        'canonical_entropy_avg': round(canonical_entropy_avg, 4),
        'entropy_reduction': round(entropy_reduction, 4),
        'residual_literal_ratio_avg': round(residual_literal_ratio_avg, 4),
        'projection_summary': {
            'by_projection': projection_summary,
            'by_modality': modality_summary,
            'declared_semantics_count': len(declared_semantics),
            'raw_bits_avg': round(raw_bits_avg, 4),
            'canonical_bits_avg': round(canonical_bits_avg, 4),
        },
    }
