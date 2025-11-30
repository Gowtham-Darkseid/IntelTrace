# IntelTrace - Complete Usage Guide

## Quick Start Commands

### 1. Installation
```bash
./setup.sh
```

### 2. Configuration (Optional)
```bash
cp .env.example .env
# Edit .env to customize MongoDB, Tor, etc.
```

### 3. Launch Web UI
```bash
./run.sh
```
Access at: **http://127.0.0.1:5000**

### 4. CLI Scans

**Username Intelligence:**
```bash
source venv/bin/activate
python main.py username johndoe --investigator "YourName"
```

**IP Intelligence:**
```bash
python main.py ip 8.8.8.8
```

**Email Intelligence:**
```bash
python main.py email test@example.com
```

**Phone Intelligence:**
```bash
python main.py phone +12025551234
```

## Features Breakdown

### 🔍 Intelligence Modules

#### IP Intelligence (`ip_intel.py`)
- WHOIS lookup
- IP geolocation (ipinfo.io)
- ISP & ASN detection
- VPN/Proxy detection (placeholder)
- Blacklist checks (placeholder)

#### Email Intelligence (`email_intel.py`)
- Breach detection via HaveIBeenPwned API pattern
- Domain reputation analysis
- *Requires API key for production*

#### Phone Intelligence (`phone_intel.py`)
- Carrier detection using phonenumbers library
- Country code identification
- International format parsing

#### Username Intelligence (`username_intel.py`)
Checks profile existence across:
- GitHub
- Twitter/X
- Reddit
- Instagram
- Facebook
- Medium

Concurrent checks with ThreadPoolExecutor for speed.

#### Dark Web Scanner (`darkweb_scanner.py`)
- Tor SOCKS5 proxy integration
- Safe simulation mode (no illegal crawling)
- Onion domain checking placeholder

### 📊 Analysis Engines

#### Reputation Engine (`reputation_engine.py`)
Scores targets based on:
- Email breach presence (+40 pts)
- Social media footprint (+5 per platform)
- IP blacklist status (+20 pts)
- Final score: 0-100 risk scale

#### Timeline Builder (`timeline_builder.py`)
Creates chronological event log:
- Scan start/end timestamps
- Discovery milestones
- ISO 8601 format

### 💾 Storage & Reports

#### Database (`database.py`)
- MongoDB integration with graceful fallback
- Optional persistence (works without DB)
- Case storage with unique IDs

#### Report Generator (`report_generator.py`)
**JSON Reports:**
- Machine-readable format
- Full investigation data
- Stored in `reports/` directory

**PDF Reports:**
- Professional layout with ReportLab
- Case ID, investigator, summary
- Reputation score and timeline
- Multi-page support

### 🎨 User Interfaces

#### Web UI (`ui_engine.py` + templates)
**Hacker Theme:**
- Black background (#000)
- Neon green text (#00FF41)
- Matrix digital rain animation
- Left navigation panel
- Live scan console with animated log
- Responsive design

**Features:**
- Target type selector (IP/Email/Phone/Username)
- Real-time scan progress
- Status indicators
- Scrolling results feed

#### CLI (`main.py`)
- ASCII art banner with green ANSI colors
- Legal notice display
- Progress logging
- Argument parsing with argparse

## Advanced Configuration

### MongoDB Setup
```bash
# Install MongoDB
sudo apt install mongodb

# Start service
sudo systemctl start mongod

# Enable on boot
sudo systemctl enable mongod
```

### Tor Integration
```bash
# Install Tor
sudo apt install tor

# Start Tor
sudo systemctl start tor

# Verify Tor is running
netstat -tlnp | grep 9050
```

### API Keys (Production)
Edit `.env`:
```
HIBP_API_KEY=your_key_here
IPINFO_TOKEN=your_token_here
SHODAN_API_KEY=your_key_here
```

Update respective modules to use keys.

## Report Samples

### JSON Structure
```json
{
  "case_id": "IT-abc123",
  "investigator": "Analyst",
  "target_type": "username",
  "target": "johndoe",
  "results": [...],
  "reputation": {"score": 45, "factors": [...]},
  "timeline": [...]
}
```

### PDF Contents
1. Header: Case ID, Investigator, Timestamp
2. Target Information
3. Intelligence Summary (results excerpt)
4. Reputation Analysis
5. Timeline of Events

## Troubleshooting

### Import Errors
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### MongoDB Connection Refused
Normal if MongoDB not installed. Tool continues without DB.

### Tor Connection Failed
Normal if Tor not installed. Dark web features disabled.

### Rate Limiting
Some platforms may rate-limit requests. Adjust delays in modules.

## Security & Ethics

### ✅ Permitted Uses
- Security research on owned systems
- OSINT investigations with authorization
- Educational demonstrations
- Threat intelligence gathering (legal)

### ❌ Prohibited Uses
- Unauthorized reconnaissance
- Stalking or harassment
- Credential stuffing
- Any illegal activity

### Best Practices
1. Always obtain written authorization
2. Document your investigation scope
3. Respect API terms of service
4. Use VPNs/proxies ethically
5. Store reports securely
6. Redact sensitive data appropriately

## Project Structure
```
IntelTrace/
├── main.py              # CLI entrypoint
├── ui_engine.py         # Flask web app
├── banner.py            # ASCII art
├── database.py          # MongoDB interface
├── ip_intel.py          # IP module
├── email_intel.py       # Email module
├── phone_intel.py       # Phone module
├── username_intel.py    # Username module
├── darkweb_scanner.py   # Tor integration
├── reputation_engine.py # Scoring system
├── timeline_builder.py  # Event tracking
├── report_generator.py  # PDF/JSON output
├── templates/           # HTML templates
├── static/              # CSS/JS assets
├── reports/             # Generated reports
├── setup.sh             # Installer
├── run.sh               # Launcher
├── demo.sh              # Demo script
├── requirements.txt     # Dependencies
├── .env.example         # Config template
├── README.md            # Main docs
└── LEGAL.md             # Legal disclaimer
```

## Development

### Adding New Intelligence Modules
1. Create `new_intel.py` in root
2. Implement `collect(target)` method
3. Import in `main.py`
4. Add to collector dictionary
5. Update requirements.txt if needed

### Customizing UI Theme
Edit `static/css/style.css`:
- Change color scheme (replace #00FF41)
- Adjust layout dimensions
- Modify animations

### Extending Report Format
Edit `report_generator.py`:
- Add sections to PDF
- Include charts/graphs
- Export to additional formats (CSV, XML)

## Performance Tips

1. **Parallel Execution**: Username intel uses ThreadPoolExecutor
2. **Timeouts**: Adjust per-request timeouts in modules
3. **Caching**: Implement Redis for repeated lookups
4. **Background Jobs**: Use Celery for async web scans

## Community & Support

This is an educational tool. For questions:
- Review code comments
- Check LEGAL.md for compliance
- Extend for your specific use case

## License
Educational use only. Not for commercial deployment without proper legal review.

---

**Remember**: Always operate within legal and ethical boundaries. 🕵️‍♂️
