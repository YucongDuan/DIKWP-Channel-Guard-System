from dikwp_guard.canonicalizers import canonicalize_numeric
from dikwp_guard.models import SampleRecord


def test_numeric_canonicalization_drops_literals():
    sample = SampleRecord(
        sample_id='s1',
        modality='numeric',
        raw_text='285 574 384 716 391 585',
        source_family='demo.teacher.a',
    )
    out = canonicalize_numeric(sample, 'numeric_bins_v1')
    assert out.projection == 'numeric_bins_v1'
    assert out.residual_literal_ratio == 0.0
    assert 'projection=numeric_bins_v1' in out.canonical_text
    assert '285' not in out.canonical_text
