from __future__ import annotations
from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict

from .models import CanonicalSample, PredictabilityMetric


def _predictability_metric(raw_texts: list[str], canonical_texts: list[str], labels: list[str]) -> PredictabilityMetric:
    nonempty = [(r, c, l) for r, c, l in zip(raw_texts, canonical_texts, labels) if l is not None]
    if len(nonempty) < 8:
        return PredictabilityMetric(label_count=len(set(labels)), sample_count=len(nonempty))
    raw_texts = [x[0] for x in nonempty]
    canonical_texts = [x[1] for x in nonempty]
    labels = [x[2] for x in nonempty]
    class_counts = Counter(labels)
    if len(class_counts) < 2:
        return PredictabilityMetric(label_count=len(class_counts), sample_count=len(labels))
    min_class = min(class_counts.values())
    if min_class < 2:
        return PredictabilityMetric(label_count=len(class_counts), sample_count=len(labels))

    splits = min(5, min_class)
    cv = StratifiedKFold(n_splits=splits, shuffle=True, random_state=42)
    clf = LogisticRegression(max_iter=2000, class_weight='balanced')

    def run(texts: list[str]):
        vec = TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 5), min_df=1)
        X = vec.fit_transform(texts)
        preds = cross_val_predict(clf, X, labels, cv=cv)
        acc = accuracy_score(labels, preds)
        f1 = f1_score(labels, preds, average='macro')
        return float(acc), float(f1)

    raw_acc, raw_f1 = run(raw_texts)
    canonical_acc, canonical_f1 = run(canonical_texts)
    baseline = max(class_counts.values()) / len(labels)
    return PredictabilityMetric(
        raw_accuracy=round(raw_acc, 4),
        canonical_accuracy=round(canonical_acc, 4),
        baseline_accuracy=round(baseline, 4),
        raw_macro_f1=round(raw_f1, 4),
        canonical_macro_f1=round(canonical_f1, 4),
        raw_excess_accuracy=round(max(0.0, raw_acc - baseline), 4),
        canonical_excess_accuracy=round(max(0.0, canonical_acc - baseline), 4),
        label_count=len(class_counts),
        sample_count=len(labels),
    )


def run_assays(samples: list[CanonicalSample], raw_text_by_id: dict[str, str]) -> tuple[PredictabilityMetric, PredictabilityMetric, dict]:
    raw_texts = [raw_text_by_id[s.sample_id] for s in samples]
    canonical_texts = [s.canonical_text for s in samples]
    teacher_labels = [s.source_family for s in samples]
    trait_labels = [s.trait_label for s in samples]

    teacher_metric = _predictability_metric(raw_texts, canonical_texts, teacher_labels)
    if any(x is not None for x in trait_labels):
        trait_metric = _predictability_metric(raw_texts, canonical_texts, [x or 'none' for x in trait_labels])
    else:
        trait_metric = PredictabilityMetric(label_count=0, sample_count=len(samples))

    leakage_summary = {
        'teacher_signal_reduction': round((teacher_metric.raw_excess_accuracy or 0.0) - (teacher_metric.canonical_excess_accuracy or 0.0), 4),
        'trait_signal_reduction': round((trait_metric.raw_excess_accuracy or 0.0) - (trait_metric.canonical_excess_accuracy or 0.0), 4),
        'teacher_signal_remaining': round(teacher_metric.canonical_excess_accuracy or 0.0, 4),
        'trait_signal_remaining': round(trait_metric.canonical_excess_accuracy or 0.0, 4),
    }
    return teacher_metric, trait_metric, leakage_summary
