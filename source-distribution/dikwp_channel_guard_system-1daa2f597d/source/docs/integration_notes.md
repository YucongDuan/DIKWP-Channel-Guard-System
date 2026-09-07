# Integration Notes

This package is intentionally compatible with the earlier organization AI control plane / white-box runtime:

- Each audit run emits `control_plane_whitebox.json` so the audit artifact can be attached as an evidence bundle.
- The `gate_decision.json` file is the object that should feed approval workflows.
- In production, the recommended flow is:

```
lineage manifest -> channel guard audit -> approval gate -> training job -> post-train eval -> release gate
```

If the organization already uses the earlier control-plane scaffold, this package should be wired in before `run.finalize` for any high-risk synthetic dataset.
