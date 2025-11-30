#!/usr/bin/env bash
set -e
source venv/bin/activate || echo "Activate venv with: source venv/bin/activate"
export FLASK_APP=ui_engine.py
export FLASK_ENV=development
echo "Starting IntelTrace Flask UI on http://127.0.0.1:5000"
flask run
