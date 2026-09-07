from __future__ import annotations
from pathlib import Path
import os
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = PROJECT_ROOT / 'configs' / 'channel_guard.yaml'
CONFIG_PATH = Path(os.environ.get('DIKWP_GUARD_CONFIG', DEFAULT_CONFIG))

with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    CONFIG = yaml.safe_load(f)

ARTIFACT_ROOT = PROJECT_ROOT / CONFIG['system'].get('artifact_root', 'artifacts')
ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
