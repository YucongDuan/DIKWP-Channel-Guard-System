# Delivery Contents

This system package contains four layers:

1. **Runtime / API layer**
   - `src/dikwp_guard/api.py`
   - `src/dikwp_guard/cli.py`
   - `docker-compose.yml`
   - `Dockerfile`

2. **Safety logic layer**
   - `canonicalizers.py` for low-capacity semantic projection
   - `genealogy.py` for lineage and trusted-root checks
   - `assay.py` for teacher/trait recoverability tests
   - `gates.py` for Green/Amber/Red decisions

3. **Evidence layer**
   - `channel_budget_card.json`
   - `genealogy_card.json`
   - `assay_result.json`
   - `gate_decision.json`
   - `control_plane_whitebox.json`

4. **Verification layer**
   - sample manifests in `examples/manifests`
   - runnable demos in `scripts/`
   - tests in `tests/`

The package is designed to sit in front of real training jobs, not to replace them.
