from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel
from .pipeline import audit_manifest
from .models import DatasetManifest

app = FastAPI(title='DIKWP Channel Guard System', version='0.1.0')


class AuditRequest(BaseModel):
    manifest: DatasetManifest
    out_dir: str | None = None


@app.get('/healthz')
def healthz():
    return {'ok': True}


@app.post('/v1/audit/run')
def run_audit(payload: AuditRequest):
    report = audit_manifest(payload.manifest, out_dir=payload.out_dir)
    return report.model_dump()
