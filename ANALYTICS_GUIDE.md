# Analytics Data Location & Access Guide

## 📊 Where Analytics Data is Stored

Your extension collects analytics data in **THREE locations**:

### 1. **Local Storage (VS Code Extension)**
**Location:** VS Code's global storage directory

**macOS Path:**
```
~/Library/Application Support/Code/User/globalStorage/enghammadkhurshid.architector-llm/analytics/
```

**Files:**
- `sessions.jsonl` - All generation sessions (with consent)
- `local.jsonl` - Local-only events (no consent needed)

**Access:**
```bash
# View sessions
cat ~/Library/Application\ Support/Code/User/globalStorage/enghammadkhurshid.architector-llm/analytics/sessions.jsonl

# View local logs
cat ~/Library/Application\ Support/Code/User/globalStorage/enghammadkhurshid.architector-llm/analytics/local.jsonl

# Pretty print with jq
cat ~/Library/Application\ Support/Code/User/globalStorage/enghammadkhurshid.architector-llm/analytics/sessions.jsonl | jq
```

### 2. **Render Backend API**
**URL:** `https://architector-analytics.onrender.com`

**Status:** ✅ **DEPLOYED AND WORKING!**

**Endpoints:**
- `POST /architector/register` - Participant registration ✅ Working
- `POST /architector/analytics` - Session data ✅ Working
- `POST /architector/delete` - GDPR deletion request
- `GET /architector/stats` - View aggregated statistics

**Recent Activity (from logs):**
- Participant registered: Hassan Khan (hassankhan@gmail.com)
- Multiple PHP project sessions logged
- Running with 4 gunicorn workers
- Port: 10000

**Access Your Data:**
1. **View Stats:** https://architector-analytics.onrender.com/architector/stats
2. **Check Logs:** Render Dashboard → architector-analytics → Logs
3. **Database:** SQLite file on Render's persistent storage

### 3. **Export Command (Research Paper)**
**Command:** "Architector: Export Analytics Data"

**Location:** Same as local storage + generates export file:
```
~/Library/Application Support/Code/User/globalStorage/enghammadkhurshid.architector-llm/analytics/export_[timestamp].json
```

**Contains:**
- Summary statistics (success rate, avg quality, etc.)
- All session data in JSON format
- Perfect for research paper analysis

---

## 🔍 How to Access Analytics Data

### Method 1: VS Code Extension Command

1. Open Command Palette (`Cmd+Shift+P`)
2. Run: "Architector: Export Analytics Data"
3. Opens file with aggregated analytics + summary

### Method 2: Direct File Access

**View raw session data:**
```bash
cd ~/Library/Application\ Support/Code/User/globalStorage/enghammadkhurshid.architector-llm/analytics

# Count total sessions
wc -l sessions.jsonl

# View latest session
tail -n 1 sessions.jsonl | jq

# View all participants
cat sessions.jsonl | jq -r '.participantId' | sort -u

# Calculate success rate
cat sessions.jsonl | jq '.success' | grep -c true
```

### Method 3: Python Analysis Script

Create `analyze_analytics.py`:
```python
import json
import pandas as pd
from pathlib import Path

# Load data
analytics_path = Path.home() / 'Library/Application Support/Code/User/globalStorage/enghammadkhurshid.architector-llm/analytics/sessions.jsonl'

sessions = []
with open(analytics_path) as f:
    for line in f:
        sessions.append(json.loads(line))

df = pd.DataFrame(sessions)

print("📊 Analytics Summary")
print(f"Total Sessions: {len(df)}")
print(f"Unique Participants: {df['participantId'].nunique()}")
print(f"Success Rate: {df['success'].mean():.1%}")
print(f"Avg Quality Score: {df['qualityScore'].mean():.1f}/100")
print(f"Avg Generation Time: {df['generationTimeSeconds'].mean():.1f}s")

print("\n🌍 Language Distribution:")
print(df['projectLanguage'].value_counts())

print("\n📋 Project Type Distribution:")
print(df['projectType'].value_counts())

print("\n🤖 LLM Provider Distribution:")
print(df['llmProvider'].value_counts())
```

---

## 🚀 Setting Up the Backend (Render)

Your extension expects a backend at `https://architector-analytics.onrender.com`, but it doesn't exist yet. Here's how to create it:

### Step 1: Create Flask Backend

**Create `analytics_server.py`:**
```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Database setup
DB_PATH = 'analytics.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Participants table
    c.execute('''CREATE TABLE IF NOT EXISTS participants
                 (participant_id TEXT PRIMARY KEY,
                  full_name TEXT,
                  email TEXT,
                  designation TEXT,
                  experience_level TEXT,
                  organization TEXT,
                  country TEXT,
                  consent_timestamp TEXT,
                  extension_version TEXT)''')
    
    # Sessions table
    c.execute('''CREATE TABLE IF NOT EXISTS sessions
                 (session_id TEXT PRIMARY KEY,
                  participant_id TEXT,
                  timestamp TEXT,
                  extension_version TEXT,
                  vscode_version TEXT,
                  platform TEXT,
                  project_language TEXT,
                  project_type TEXT,
                  project_size TEXT,
                  file_count INTEGER,
                  diagrams_generated INTEGER,
                  generation_time REAL,
                  success BOOLEAN,
                  quality_score REAL,
                  llm_provider TEXT,
                  FOREIGN KEY (participant_id) REFERENCES participants(participant_id))''')
    
    conn.commit()
    conn.close()

init_db()

@app.route('/architector/register', methods=['POST'])
def register_participant():
    data = request.json
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        c.execute('''INSERT OR REPLACE INTO participants VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (data['participantId'], data['fullName'], data['email'],
                   data['designation'], data['experienceLevel'],
                   data.get('organization'), data.get('country'),
                   data['consentTimestamp'], data['extensionVersion']))
        conn.commit()
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        conn.close()

@app.route('/architector/analytics', methods=['POST'])
def log_analytics():
    data = request.json
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        c.execute('''INSERT INTO sessions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (data['sessionId'], data['participantId'], data['timestamp'],
                   data['extensionVersion'], data['vscodeVersion'], data['platform'],
                   data['projectLanguage'], data['projectType'], data['projectSize'],
                   data['fileCount'], data['diagramsGenerated'],
                   data['generationTimeSeconds'], data['success'],
                   data.get('qualityScore'), data['llmProvider']))
        conn.commit()
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        conn.close()

@app.route('/architector/delete', methods=['POST'])
def delete_participant():
    data = request.json
    participant_id = data['participantId']
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        c.execute('DELETE FROM sessions WHERE participant_id = ?', (participant_id,))
        c.execute('DELETE FROM participants WHERE participant_id = ?', (participant_id,))
        conn.commit()
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        conn.close()

@app.route('/architector/stats', methods=['GET'])
def get_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    stats = {
        'total_participants': c.execute('SELECT COUNT(*) FROM participants').fetchone()[0],
        'total_sessions': c.execute('SELECT COUNT(*) FROM sessions').fetchone()[0],
        'success_rate': c.execute('SELECT AVG(success) FROM sessions').fetchone()[0],
        'avg_quality': c.execute('SELECT AVG(quality_score) FROM sessions WHERE quality_score IS NOT NULL').fetchone()[0],
        'languages': dict(c.execute('SELECT project_language, COUNT(*) FROM sessions GROUP BY project_language').fetchall()),
        'providers': dict(c.execute('SELECT llm_provider, COUNT(*) FROM sessions GROUP BY llm_provider').fetchall())
    }
    
    conn.close()
    return jsonify(stats), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

**Create `requirements.txt`:**
```
flask>=3.0.0
flask-cors>=4.0.0
gunicorn>=21.2.0
```

### Step 2: Deploy to Render

1. **Create GitHub Repo:**
   ```bash
   cd ~/analytics-backend
   git init
   git add .
   git commit -m "Analytics backend for Architector-LLM"
   git remote add origin https://github.com/YOUR_USERNAME/architector-analytics.git
   git push -u origin main
   ```

2. **Deploy on Render:**
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Settings:
     - **Name:** `architector-analytics`
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn analytics_server:app`
     - **Plan:** Free (sufficient for research)
   - Click "Create Web Service"

3. **Your URL will be:** `https://architector-analytics.onrender.com`

### Step 3: View Analytics Dashboard

**Option A: Simple Stats Endpoint**
Visit: `https://architector-analytics.onrender.com/architector/stats`

**Option B: Create Admin Dashboard**
Add Streamlit dashboard to view data visually (optional).

---

## 📈 Analytics Data Structure

### Participant Data
```json
{
  "participantId": "uuid-v4",
  "fullName": "John Doe",
  "email": "john@example.com",
  "designation": "Senior Developer",
  "experienceLevel": "senior",
  "organization": "NUST",
  "country": "Pakistan",
  "consentTimestamp": "2026-01-23T10:30:00Z",
  "extensionVersion": "2.0.7"
}
```

### Session Data
```json
{
  "sessionId": "session_123456",
  "participantId": "uuid-v4",
  "timestamp": "2026-01-23T10:35:00Z",
  "projectLanguage": "Python",
  "projectType": "web_api",
  "projectSize": "medium",
  "fileCount": 45,
  "diagramsGenerated": 5,
  "generationTimeSeconds": 12.5,
  "success": true,
  "qualityScore": 87.3,
  "validationScores": {
    "syntax": 95,
    "completeness": 88,
    "clarity": 82,
    "accuracy": 84
  },
  "llmProvider": "ollama"
}
```

---

## 🔐 Privacy & GDPR Compliance

Your extension follows best practices:

✅ **Consent-First:** No data collected without explicit consent  
✅ **Local Fallback:** Data stored locally if no consent  
✅ **Transparent:** Clear explanation of what's collected  
✅ **Right to Delete:** Users can withdraw and delete data  
✅ **Secure:** HTTPS for all API calls  
✅ **No Code:** Never collects source code or secrets  

---

## 📊 For Your Research Paper

### Data Collection Points:
1. **Participant Demographics** (once)
2. **Generation Sessions** (every use)
3. **Quality Metrics** (automatic validation)
4. **Performance Benchmarks** (generation time, success rate)

### Analysis You Can Perform:
- Success rate by language/project type
- Quality score distribution
- Generation time trends
- User experience levels correlation
- LLM provider comparison (Ollama vs DeepSeek)
- Framework detection accuracy

### Export for Paper:
```bash
# Run in VS Code
Cmd+Shift+P → "Architector: Export Analytics Data"

# Analyze with Python/R
# Create charts, tables for paper
```

---

## 🎯 Current Status

| Component | Status | Details |
|-----------|--------|---------|
| Extension Analytics Code | ✅ Complete | Collecting all metrics |
| Local Storage | ✅ Working | Data in VS Code global storage |
| Export Command | ✅ Working | Export via Command Palette |
| Render Backend | ✅ **DEPLOYED** | **Running with 4 workers on Render.com** |
| SQLite Database | ✅ Working | Storing participants + sessions |
| Analytics Collection | ✅ Active | Real data being collected |

**Live Backend Status:**
- **URL:** https://architector-analytics.onrender.com
- **Workers:** 4 gunicorn processes
- **Recent Activity:**
  - ✅ Participant registered: Hassan Khan
  - 📊 PHP project sessions logged
  - 🔄 Real-time data collection active

**Next Steps:**
1. ✅ ~~Create backend Flask app~~ (Done)
2. ✅ ~~Deploy to Render~~ (Done - Live!)
3. ✅ ~~Test with extension~~ (Done - Working!)
4. 🔄 Continue collecting real data
5. 📊 View stats: https://architector-analytics.onrender.com/architector/stats
6. 📄 Export for research paper when ready

---

## 🔧 Testing Analytics Locally

Before deploying backend, test locally:

```bash
# Run Flask server locally
cd ~/analytics-backend
python3 analytics_server.py

# Update extension to use localhost (for testing)
# In developerInfo.ts and telemetry.ts:
# Change: https://architector-analytics.onrender.com
# To: http://localhost:5000

# Test with extension
# Generate documentation in VS Code
# Check: http://localhost:5000/architector/stats
```

---

## 📞 Support

**Researcher:** Engr. Hammad Khurshid  
**Email:** engr.hammadkhurshid@gmail.com  
**Institution:** NUST Pakistan  

For analytics questions or data access issues, contact the researcher.
