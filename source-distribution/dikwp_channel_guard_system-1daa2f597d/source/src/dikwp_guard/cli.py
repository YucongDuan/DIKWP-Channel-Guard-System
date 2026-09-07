from __future__ import annotations
import argparse
import json
from pathlib import Path
import uvicorn

from .pipeline import audit_manifest


def cmd_audit(args: argparse.Namespace) -> int:
    with open(args.manifest, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    report = audit_manifest(manifest, out_dir=args.out)
    print(json.dumps({
        'run_id': report.run_id,
        'decision': report.gate_decision.decision,
        'summary': report.gate_decision.summary,
        'out_dir': str(Path(args.out) if args.out else ''),
    }, ensure_ascii=False, indent=2))
    return 0


def cmd_serve(args: argparse.Namespace) -> int:
    uvicorn.run('dikwp_guard.api:app', host=args.host, port=args.port, reload=False)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='dikwp-guard')
    sub = parser.add_subparsers(dest='command', required=True)

    p_audit = sub.add_parser('audit', help='run an audit from a manifest file')
    p_audit.add_argument('manifest', help='path to dataset manifest json')
    p_audit.add_argument('--out', default=None, help='output directory')
    p_audit.set_defaults(func=cmd_audit)

    p_serve = sub.add_parser('serve', help='start local API')
    p_serve.add_argument('--host', default='127.0.0.1')
    p_serve.add_argument('--port', type=int, default=8000)
    p_serve.set_defaults(func=cmd_serve)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == '__main__':
    raise SystemExit(main())
