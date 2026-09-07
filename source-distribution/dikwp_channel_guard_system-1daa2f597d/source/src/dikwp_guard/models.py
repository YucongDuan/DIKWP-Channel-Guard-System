from __future__ import annotations
from typing import Any, Literal
from pydantic import BaseModel, Field

Modality = Literal['numeric', 'code', 'cot', 'dialog', 'json', 'free_text']
Risk = Literal['low', 'medium', 'high']
Decision = Literal['green', 'amber', 'red']
IntendedUse = Literal['sft', 'dpo', 'distillation', 'rl', 'eval', 'archive', 'other']


class SampleRecord(BaseModel):
    sample_id: str
    modality: Modality
    raw_text: str
    source_family: str
    teacher_id: str | None = None
    trait_label: str | None = None
    declared_semantics: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class DatasetManifest(BaseModel):
    dataset_id: str
    dataset_name: str
    risk_level: Risk
    intended_use: IntendedUse
    base_family: str
    student_base_family: str | None = None
    teacher_model: str | None = None
    trusted_root: str | None = None
    lineage_complete: bool = False
    synthetic_depth: int = 0
    declared_semantics: list[str] = Field(default_factory=list)
    projection_policy: dict[str, str] = Field(default_factory=dict)
    samples: list[SampleRecord]


class CanonicalSample(BaseModel):
    sample_id: str
    modality: Modality
    source_family: str
    teacher_id: str | None = None
    trait_label: str | None = None
    projection: str
    canonical_text: str
    raw_token_count: int
    canonical_token_count: int
    preserved_literal_tokens: int
    residual_literal_ratio: float
    dropped_ratio: float
    raw_entropy: float
    canonical_entropy: float
    notes: list[str] = Field(default_factory=list)


class GenealogyCard(BaseModel):
    dataset_id: str
    base_family: str
    student_base_family: str | None = None
    teacher_model: str | None = None
    trusted_root: str | None = None
    lineage_complete: bool
    synthetic_depth: int
    same_family_risk: bool
    risk_color: Decision
    notes: list[str] = Field(default_factory=list)


class ChannelBudgetCard(BaseModel):
    dataset_id: str
    declared_semantics: list[str]
    raw_entropy_avg: float
    canonical_entropy_avg: float
    entropy_reduction: float
    residual_literal_ratio_avg: float
    projection_summary: dict[str, Any]
    notes: list[str] = Field(default_factory=list)


class PredictabilityMetric(BaseModel):
    raw_accuracy: float | None = None
    canonical_accuracy: float | None = None
    baseline_accuracy: float | None = None
    raw_macro_f1: float | None = None
    canonical_macro_f1: float | None = None
    raw_excess_accuracy: float | None = None
    canonical_excess_accuracy: float | None = None
    label_count: int = 0
    sample_count: int = 0


class AssayResult(BaseModel):
    dataset_id: str
    teacher_predictability: PredictabilityMetric
    trait_predictability: PredictabilityMetric
    leakage_summary: dict[str, Any]
    notes: list[str] = Field(default_factory=list)


class GateDecisionModel(BaseModel):
    dataset_id: str
    decision: Decision
    summary: str
    blocking_conditions: list[str] = Field(default_factory=list)
    required_actions: list[str] = Field(default_factory=list)
    metrics_snapshot: dict[str, Any] = Field(default_factory=dict)


class AuditReport(BaseModel):
    run_id: str
    generated_at: str
    manifest: dict[str, Any]
    genealogy_card: GenealogyCard
    channel_budget_card: ChannelBudgetCard
    assay_result: AssayResult
    gate_decision: GateDecisionModel
    canonical_samples: list[CanonicalSample]
    residual: list[str] = Field(default_factory=list)
