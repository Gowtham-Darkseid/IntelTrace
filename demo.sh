#!/usr/bin/env bash
# IntelTrace Demo Script - Showcases all features

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  IntelTrace - Complete Feature Demonstration             ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

cd "$(dirname "$0")"
source venv/bin/activate

echo "[1/4] 🔍 Username Intelligence Collection"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python main.py username github --investigator "Demo_Analyst"
echo ""

echo "[2/4] 📧 Email Intelligence Collection (Placeholder)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Email scan: test@example.com"
python main.py email test@example.com --investigator "Demo_Analyst"
echo ""

echo "[3/4] 📊 Generated Reports"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ls -lh reports/*.json reports/*.pdf 2>/dev/null | tail -5
echo ""

echo "[4/4] 🌐 Web UI Status"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "To launch the Hacker UI:"
echo "  ./run.sh"
echo ""
echo "Then open: http://127.0.0.1:5000"
echo ""
echo "✅ Demo Complete! Check reports/ directory for outputs."
