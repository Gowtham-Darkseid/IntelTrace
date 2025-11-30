# IntelTrace – Automated OSINT Intelligence Collection Tool (Hacker Green UI Edition)

![Status](https://img.shields.io/badge/status-active-brightgreen) ![Python](https://img.shields.io/badge/python-3.8+-blue) ![License](https://img.shields.io/badge/license-Educational-orange)

<img width="1695" height="800" alt="image" src="https://github.com/user-attachments/assets/94d7a46f-4257-4f90-861b-6f9335f0c4a5" />


IntelTrace is a Linux-first OSINT automation toolkit with a **hacker-themed Flask dashboard**. It collects public intelligence for IPs, emails, phone numbers and usernames, correlates results, stores them in MongoDB and generates PDF/JSON reports.

⚠️ **IMPORTANT**: IntelTrace is intended for **legal OSINT only**. Do not use it to access unauthorized resources or to break any law. See the `LEGAL.md` file.

---

## ✨ Features

### Intelligence Collection
- **IP Intelligence**: WHOIS, geolocation, ISP/ASN detection, VPN/proxy detection, blacklist checks
- **Email Intelligence**: Breach detection, domain reputation analysis
- **Phone Intelligence**: Carrier detection, country code lookup
- **Username Intelligence**: Cross-platform discovery (GitHub, Twitter/X, Reddit, Instagram, Facebook, Medium)
- **Dark Web Scanner**: Tor-based username search simulation (requires Tor service)

### Analysis & Reporting
- **Reputation Scoring Engine**: Risk profiling based on collected intelligence
- **Timeline Builder**: Chronological event tracking
- **MongoDB Persistence**: Store all investigation cases
- **PDF Report Generator**: Professional investigation reports with ReportLab
- **JSON Export**: Machine-readable output format

### User Interface
- **Hacker-Themed Flask Web Dashboard** with:
  - Black background with neon green font
  - Matrix digital rain animation
  - Animated scan progress
  - Scrolling recon results
  - Blinking cursor effects
  - Left cyber menu panel
  - ASCII art banners
  - Status color indicators
- **CLI Interface**: Command-line execution for automation

---

## 🚀 Quick Start

### Prerequisites
- Linux OS (tested on Ubuntu/Debian)
- Python 3.8+
- MongoDB (optional, for persistence)
- Tor (optional, for dark web features)

### Installation

1. **Clone and setup**:
```bash
cd /home/darkseid/Tools/IntelTrace
chmod +x setup.sh run.sh
./setup.sh
```

2. **Start required services** (optional):
```bash
# MongoDB
sudo systemctl start mongod

# Tor (for dark web features)
sudo apt install tor
sudo systemctl start tor
```

3. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your settings if needed
```

### Running IntelTrace

#### Web UI (Recommended)
```bash
./run.sh
```
Then open your browser to: **http://127.0.0.1:5000**

#### CLI Mode
```bash
source venv/bin/activate
python main.py ip 8.8.8.8
python main.py email test@example.com
python main.py phone +1234567890
python main.py username johndoe --investigator "Agent Smith"
```

---

## 🎨 UI Preview

The hacker-style interface features:
- **Matrix Effect**: Scrolling green code animation on load
- **Left Panel**: Navigation menu with cyber aesthetics
- **Scanner Console**: Target input with type selection (IP/Email/Phone/Username)
- **Live Log**: Real-time scan progress with animated output
- **Monospace Font**: Authentic terminal feel

---

## 📊 Report Output

### JSON Format
Reports are saved to `./reports/` directory:
```json
{
  "case_id": "IT-abcdef01",
  "investigator": "Analyst",
  "target_type": "username",
  "target": "exampleuser",
  "results": [...],
  "reputation": {"score": 35, "factors": ["social_hits_1"]},
  "timeline": [...]
}
```

### PDF Report Includes
- Case ID and investigator name
- Intelligence summary
- OSINT sources used
- Breach results
- Dark web findings
- Social media discovery
- Digital footprint mapping
- Reputation risk score
- Timeline analysis
- Timestamp

---

## 🔧 Technology Stack

- **Backend**: Python 3, Flask
- **Database**: MongoDB
- **APIs**: Public OSINT endpoints (ipinfo.io, haveibeenpwned, etc.)
- **Anonymity**: Tor integration via SOCKS5 proxy
- **Reports**: ReportLab (PDF), JSON
- **Frontend**: HTML5, CSS3, Vanilla JavaScript

---

## 📁 Project Structure

```
IntelTrace/
├── main.py                 # CLI orchestration entrypoint
├── ui_engine.py           # Flask web application
├── database.py            # MongoDB integration
├── ip_intel.py            # IP intelligence module
├── email_intel.py         # Email intelligence module
├── phone_intel.py         # Phone intelligence module
├── username_intel.py      # Username discovery module
├── darkweb_scanner.py     # Tor-based dark web scanner
├── reputation_engine.py   # Risk scoring engine
├── timeline_builder.py    # Event timeline generator
├── report_generator.py    # PDF/JSON report creator
├── templates/             # Flask HTML templates
│   ├── layout.html
│   └── index.html
├── static/                # CSS and JavaScript assets
│   ├── css/style.css
│   └── js/ui.js
├── reports/               # Generated reports (auto-created)
├── requirements.txt       # Python dependencies
├── setup.sh              # Installation script
├── run.sh                # Launch script
├── .env.example          # Configuration template
├── README.md             # This file
├── LEGAL.md              # Legal disclaimer
└── sample_output.json    # Example output

```

---

## ⚖️ Legal & Ethics

**READ THIS CAREFULLY:**

IntelTrace is designed for:
- ✅ Legal OSINT investigations
- ✅ Security research on systems you own
- ✅ Educational purposes
- ✅ Public data collection only

IntelTrace is **NOT** for:
- ❌ Unauthorized access to systems
- ❌ Stalking or harassment
- ❌ Illegal data scraping
- ❌ Privacy violations

**You are responsible for:**
- Complying with all applicable laws in your jurisdiction
- Obtaining proper authorization before investigating targets
- Using the tool ethically and responsibly
- Understanding that some APIs require keys and terms acceptance

See `LEGAL.md` for detailed terms.

---

## 🛠️ Configuration

Edit `.env` to customize:

```bash
MONGO_URI=mongodb://localhost:27017
MONGO_DB=inteltrace
TOR_PROXY=socks5h://127.0.0.1:9050
REPORTS_DIR=./reports
INVESTIGATOR_NAME=Analyst
```

---

## 🔌 API Keys (Optional)

For production use, obtain API keys for:
- **HaveIBeenPwned**: Email breach lookups
- **ipinfo.io**: Enhanced IP geolocation
- **Shodan**: Advanced IP intelligence
- **VirusTotal**: Reputation checks

Add keys to `.env` and update respective modules.

---

## 🐛 Troubleshooting

### MongoDB Connection Failed
```bash
# Check if MongoDB is running
sudo systemctl status mongod

# Start MongoDB
sudo systemctl start mongod
```

### Tor Connection Failed
```bash
# Install and start Tor
sudo apt install tor
sudo systemctl start tor

# Verify Tor is listening on port 9050
netstat -tlnp | grep 9050
```

### Module Import Errors
```bash
# Reinstall dependencies
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🎓 Educational Use

IntelTrace was created as a **final year project** demonstrating:
- OSINT automation techniques
- Cyber security investigation workflows
- Full-stack development (Python, Flask, MongoDB)
- UI/UX design for security tools
- Legal and ethical frameworks for intelligence gathering

---

## 🤝 Contributing

This is an educational project. Feel free to fork and extend for your own learning purposes.

---

## 📝 License

**Educational Use Only** – Use responsibly and ethically.

---

## 🙏 Credits

Built by a cyber intelligence engineer specializing in OSINT, SOC operations, and cybercrime investigation tools.

**Disclaimer**: The author is not responsible for misuse of this tool. Always operate within legal boundaries.

---

## 🚦 Status Indicators

When scanning, the UI displays:
- 🟢 **Green**: Active scanning
- 🟡 **Yellow**: Processing
- 🔴 **Red**: Error/Warning
- ⚪ **White**: Complete

---

**Remember**: With great power comes great responsibility. Use IntelTrace wisely! 🕵️‍♂️
