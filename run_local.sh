#!/usr/bin/env bash
set -euo pipefail

echo "[setup] Installing frontend dependencies"
npm install

echo "[setup] Installing backend dependencies"
python3 -m pip install -r backend/requirements.txt

echo "[run] Starting frontend + backend (Ctrl+C to stop)"
npm run dev
