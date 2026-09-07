from __future__ import annotations
from .config import CONFIG
from .models import DatasetManifest, ChannelBudgetCard, AssayResult, GenealogyCard, GateDecisionModel


def make_gate_decision(manifest: DatasetManifest, genealogy: GenealogyCard, budget: ChannelBudgetCard, assay: AssayResult) -> GateDecisionModel:
    policy = CONFIG['policy']
    green = CONFIG['thresholds']['green']
    amber = CONFIG['thresholds']['amber']

    blocking: list[str] = []
    actions: list[str] = []
    decision = 'green'

    same_family = genealogy.same_family_risk
    high_risk = manifest.risk_level == 'high' and manifest.intended_use in policy['high_risk_intended_use']

    if high_risk and policy['require_lineage_complete_for_high_risk'] and not manifest.lineage_complete:
        blocking.append('high-risk dataset missing complete lineage manifest')
        decision = 'red'
    if high_risk and policy['require_trusted_root_for_high_risk'] and not manifest.trusted_root:
        blocking.append('high-risk dataset missing trusted root checkpoint or human-origin root')
        decision = 'red'
    if high_risk and same_family and manifest.synthetic_depth >= 1:
        actions.append('treat same-family synthetic data as elevated risk and require assay sign-off')
        decision = 'amber' if decision != 'red' else decision

    teacher_excess = assay.teacher_predictability.canonical_excess_accuracy or 0.0
    trait_excess = assay.trait_predictability.canonical_excess_accuracy or 0.0
    residual_ratio = budget.residual_literal_ratio_avg
    entropy_reduction = budget.entropy_reduction

    unsupported_modalities = [
        s.modality for s in manifest.samples
        if s.modality in policy['high_risk_modalities'] and manifest.projection_policy.get(s.modality, '').endswith('_raw')
    ]
    if high_risk and unsupported_modalities:
        blocking.append(f'raw projections not allowed for high-risk modalities: {sorted(set(unsupported_modalities))}')
        decision = 'red'

    if teacher_excess > amber['max_teacher_excess_accuracy']:
        blocking.append(f'teacher signal remains above amber threshold ({teacher_excess:.3f})')
        decision = 'red'
    elif teacher_excess > green['max_teacher_excess_accuracy'] and decision != 'red':
        actions.append(f'reduce same-family teacher recoverability below {green["max_teacher_excess_accuracy"]:.2f}')
        decision = 'amber'

    if trait_excess > amber['max_trait_excess_accuracy']:
        blocking.append(f'trait signal remains above amber threshold ({trait_excess:.3f})')
        decision = 'red'
    elif trait_excess > green['max_trait_excess_accuracy'] and decision != 'red':
        actions.append(f'reduce trait recoverability below {green["max_trait_excess_accuracy"]:.2f}')
        decision = 'amber'

    if residual_ratio > amber['max_residual_literal_ratio']:
        blocking.append(f'residual literal ratio too high ({residual_ratio:.3f})')
        decision = 'red'
    elif residual_ratio > green['max_residual_literal_ratio'] and decision != 'red':
        actions.append('reduce preserved literals in canonical outputs')
        decision = 'amber'

    if entropy_reduction < amber['min_entropy_reduction'] and high_risk:
        if teacher_excess > 0.0 or trait_excess > 0.0 or residual_ratio > 0.0:
            blocking.append(f'entropy reduction too weak for high-risk use ({entropy_reduction:.3f})')
            decision = 'red'
        else:
            actions.append('projection passes assay but should still be manually reviewed because information-theoretic proxy is weak')
            decision = 'amber' if decision == 'green' else decision
    elif entropy_reduction < green['min_entropy_reduction'] and decision != 'red':
        actions.append('increase lossy projection before training')
        decision = 'amber'

    if decision == 'green':
        summary = 'Declared semantics appear constrained; audit may proceed with standard human review.'
    elif decision == 'amber':
        summary = 'Undeclared capacity has been reduced but not sufficiently closed; remediation required before training approval.'
    else:
        summary = 'Stop-ship: lineage, projection, or assay evidence shows undeclared capacity remains too wide for the proposed use.'

    if not actions and decision == 'red':
        actions.extend([
            'replace raw teacher outputs with low-capacity projections',
            'complete genealogy card and trusted root chain',
            'rerun teacher/trait assay on canonicalized data',
        ])

    snapshot = {
        'teacher_excess_accuracy': round(teacher_excess, 4),
        'trait_excess_accuracy': round(trait_excess, 4),
        'residual_literal_ratio_avg': budget.residual_literal_ratio_avg,
        'entropy_reduction': budget.entropy_reduction,
        'same_family_risk': same_family,
        'synthetic_depth': manifest.synthetic_depth,
    }
    return GateDecisionModel(
        dataset_id=manifest.dataset_id,
        decision=decision,
        summary=summary,
        blocking_conditions=blocking,
        required_actions=actions,
        metrics_snapshot=snapshot,
    )
