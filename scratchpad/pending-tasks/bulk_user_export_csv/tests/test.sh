#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
python3 -m pytest -v test_final_state.py
