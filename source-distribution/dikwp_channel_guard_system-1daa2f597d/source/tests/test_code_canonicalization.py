from dikwp_guard.canonicalizers import canonicalize_python_code
from dikwp_guard.models import SampleRecord


def test_code_canonicalization_strips_identifiers():
    code = 'def add(a, b):\n    secret_name = a + b\n    return secret_name\n'
    sample = SampleRecord(sample_id='c1', modality='code', raw_text=code, source_family='demo.code')
    out = canonicalize_python_code(sample, 'python_ast_v1')
    assert 'secret_name' not in out.canonical_text
    assert 'funcs=' in out.canonical_text
