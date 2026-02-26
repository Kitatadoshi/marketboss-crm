#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHONPATH=. python3 scripts/seed_demo.py
PYTHONPATH=. python3 -m uvicorn src.interfaces.http.app:app --host 0.0.0.0 --port 8080 --reload
