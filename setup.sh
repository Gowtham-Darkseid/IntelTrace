#!/usr/bin/env bash
set -e
echo "[IntelTrace] Installer - setting up virtualenv, dependencies, and guidance"
PYENV_DIR="venv"
if [ ! -d "$PYENV_DIR" ]; then
  python3 -m venv "$PYENV_DIR"
fi
source "$PYENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r requirements.txt
echo "Installer: Ensure MongoDB is running (e.g., sudo systemctl start mongod)."
echo "Installer: To use Tor features, install Tor and start it (sudo apt install tor && sudo systemctl start tor)."
echo "Done. Activate with: source venv/bin/activate && ./run.sh"
