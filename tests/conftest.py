from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for sub in ("", "app", "airflow/dags"):
    path = str(ROOT / sub) if sub else str(ROOT)
    if path not in sys.path:
        sys.path.insert(0, path)
