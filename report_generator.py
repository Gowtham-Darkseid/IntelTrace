"""Generates JSON and PDF reports using collected intelligence."""
import os
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from dotenv import load_dotenv

load_dotenv()
REPORTS_DIR = os.getenv('REPORTS_DIR', './reports')
os.makedirs(REPORTS_DIR, exist_ok=True)


class ReportGenerator:
    def __init__(self):
        pass

    def generate_json(self, payload):
        fname = os.path.join(REPORTS_DIR, f"{payload.get('case_id')}.json")
        with open(fname, 'w') as f:
            json.dump(payload, f, indent=2, default=str)
        return fname

    def generate_pdf(self, payload):
        fname = os.path.join(REPORTS_DIR, f"{payload.get('case_id')}.pdf")
        c = canvas.Canvas(fname, pagesize=letter)
        width, height = letter
        c.setFont('Courier-Bold', 12)
        y = height - 40
        c.drawString(40, y, f"Case ID: {payload.get('case_id')}")
        y -= 20
        c.drawString(40, y, f"Investigator: {payload.get('investigator')}")
        y -= 20
        c.drawString(40, y, f"Target: {payload.get('target_type')} - {payload.get('target')}")
        y -= 30
        c.setFont('Courier', 10)
        c.drawString(40, y, "Intelligence Summary:")
        y -= 16
        summary = str(payload.get('results'))[:1600]
        for line in summary.splitlines():
            if y < 60:
                c.showPage()
                y = height - 40
            c.drawString(40, y, line[:100])
            y -= 12
        y -= 10
        c.drawString(40, y, f"Reputation Score: {payload.get('reputation')}")
        c.showPage()
        c.save()
        return fname

    def generate(self, payload):
        j = self.generate_json(payload)
        p = self.generate_pdf(payload)
        return {'json': j, 'pdf': p}
