#!/usr/bin/env bash
set -euo pipefail

echo "[setup] Installing frontend dependencies"
npm install

echo "[setup] Installing backend test dependencies"
python3 -m pip install -r backend/requirements-dev.txt

echo "[test] Running backend tests"
python3 -m pytest backend/tests/ -q

echo "[test] Running frontend tests"
npm run test
