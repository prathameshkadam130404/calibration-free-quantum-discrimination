"""Run metadata and small I/O helpers shared by the research scripts."""
from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
import time
from typing import Any, Dict

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def git_commit() -> str:
    try:
        out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, capture_output=True,
                             text=True, timeout=10)
        dirty = subprocess.run(["git", "status", "--porcelain", "research", "experiments"],
                               cwd=REPO_ROOT, capture_output=True, text=True, timeout=10)
        return out.stdout.strip() + ("+dirty" if dirty.stdout.strip() else "")
    except Exception as exc:  # noqa: BLE001 - metadata must never crash a run
        return f"unknown ({exc})"


def package_versions() -> Dict[str, str]:
    vers = {"python": platform.python_version()}
    for name in ("numpy", "scipy", "sklearn", "pennylane", "xgboost", "sympy"):
        try:
            mod = __import__(name)
            vers[name] = getattr(mod, "__version__", "?")
        except Exception:  # noqa: BLE001
            vers[name] = "missing"
    return vers


def run_metadata(**extra: Any) -> Dict[str, Any]:
    meta = {"timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"), "git_commit": git_commit(),
            "versions": package_versions(), "argv": sys.argv}
    meta.update(extra)
    return meta


def results_dir(exp_id: str) -> str:
    path = os.path.join(REPO_ROOT, "results", exp_id)
    os.makedirs(path, exist_ok=True)
    return path


def dump_json(obj: Any, path: str) -> None:
    def default(o: Any) -> Any:
        try:
            import numpy as np
            if isinstance(o, np.integer):
                return int(o)
            if isinstance(o, np.floating):
                return float(o)
            if isinstance(o, np.ndarray):
                return o.tolist()
        except Exception:  # noqa: BLE001
            pass
        return str(o)

    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, default=default)
