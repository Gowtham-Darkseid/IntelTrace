"""Flask-based hacker-themed UI for IntelTrace."""
from flask import Flask, render_template, request, jsonify, send_from_directory
from dotenv import load_dotenv
from main import run_investigation
from database import IntelDB
from photo_intel import PhotoIntel
from werkzeug.utils import secure_filename
import os
import json
import glob

load_dotenv()
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    db = IntelDB()
    cases = db.list_cases()
    stats = {
        'total_cases': len(cases),
        'target_types': {},
        'recent_cases': cases[:10] if cases else []
    }
    for case in cases:
        t_type = case.get('target_type', 'unknown')
        stats['target_types'][t_type] = stats['target_types'].get(t_type, 0) + 1
    return render_template('dashboard.html', stats=stats)


@app.route('/reports')
def reports():
    db = IntelDB()
    cases = db.list_cases()
    return render_template('reports.html', cases=cases)


@app.route('/reports/<case_id>')
def report_detail(case_id):
    db = IntelDB()
    case = db.get_case(case_id)
    if not case:
        return jsonify({'error': 'Case not found'}), 404
    return render_template('report_detail.html', case=case)


@app.route('/ddos')
def ddos_page():
    return render_template('ddos.html')


@app.route('/api/reports')
def api_reports():
    db = IntelDB()
    cases = db.list_cases()
    return jsonify(cases)


@app.route('/scan', methods=['POST'])
def scan():
    # Check if this is a photo upload
    if 'photo' in request.files:
        return handle_photo_scan()
    
    data = request.json or {}
    t = data.get('type')
    v = data.get('value')
    inv = data.get('investigator')
    if not t or not v:
        return jsonify({'error': 'missing type or value'}), 400
    # Kick off investigation synchronously for demo; production use background jobs
    run_investigation(t, v, inv)
    return jsonify({'status': 'started', 'target': v})


def handle_photo_scan():
    """Handle photo upload and scanning."""
    if 'photo' not in request.files:
        return jsonify({'error': 'No photo uploaded'}), 400
    
    file = request.files['photo']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        photo_intel = PhotoIntel()
        filepath = photo_intel.save_upload(file.read(), filename)
        
        # Get investigator from form data
        inv = request.form.get('investigator')
        
        # Run investigation
        run_investigation('photo', filepath, inv)
        return jsonify({'status': 'started', 'target': filename, 'path': filepath})
    
    return jsonify({'error': 'Invalid file type'}), 400


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded photos."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
