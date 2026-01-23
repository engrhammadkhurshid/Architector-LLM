# 📊 Participant Data Collection & Export Guide

## Overview
Your Architector-LLM extension collects comprehensive participant data for research purposes. This guide explains where the data is stored and how to export it for your research paper.

---

## 🎯 What Data is Collected?

### Developer/Participant Information (Collected Once)
- ✅ **Full Name** - Professional identity
- ✅ **Email Address** - Contact information
- ✅ **Job Title/Designation** - e.g., Software Engineer, Developer, Student
- ✅ **Experience Level** - Junior, Mid, Senior, Principal, Lead, Architect, Other
- ✅ **Organization/Company** - Optional (e.g., NUST, Google, Independent)
- ✅ **Country** - Optional (e.g., Pakistan, USA, India)
- ✅ **Consent Timestamp** - ISO 8601 format (e.g., 2026-01-23T09:19:09.000Z)
- ✅ **Consent Version** - Currently "1.0"
- ✅ **Participant ID** - Anonymous UUID (e.g., 6b4ec895-8b50-41d8-97e3-c4695d7b1a7d)
- ✅ **Extension Version** - Version used during registration

### Usage Data (Collected Per Session)
- Session ID, Timestamp, Extension Version
- VS Code Version, Platform (macOS/Windows/Linux)
- Project Language, Type, Size, File Count
- Diagrams Generated, Generation Time
- Success Status, Quality Score
- LLM Provider Used

---

## 📍 Where is Participant Data Stored?

### 1. **VS Code Global State** (Local)
**Location:** VS Code's internal storage (per user)
- **Key:** `research.developerInfo`
- **Stored:** DeveloperInfo object (JSON)
- **Access:** Through VS Code extension context only

**To View:**
```bash
# VS Code stores this in SQLite/JSON internally
# Location varies by OS:
# macOS: ~/Library/Application Support/Code/User/globalStorage/<extension-id>/
# Not directly accessible as plain files
```

### 2. **Render Backend Database** ✅ (PRIMARY SOURCE)
**Location:** `https://architector-analytics.onrender.com`
**Database:** SQLite (`analytics.db`)
**Table:** `participants`

**Schema:**
```sql
CREATE TABLE participants (
    participant_id TEXT PRIMARY KEY,       -- UUID: 6b4ec895-8b50-41d8-97e3-c4695d7b1a7d
    full_name TEXT,                        -- Hassan Khan
    email TEXT,                            -- hassankhan@gmail.com
    designation TEXT,                      -- Software Engineer
    experience_level TEXT,                 -- junior/mid/senior/principal/lead/architect/other
    organization TEXT,                     -- NUST, Google, etc. (optional)
    country TEXT,                          -- Pakistan, USA, etc. (optional)
    consent_timestamp TEXT,                -- 2026-01-23T09:19:09.192149675Z
    extension_version TEXT                 -- 2.0.7
)
```

**Current Data (from your logs):**
```
Participant ID: 6b4ec895-8b50-41d8-97e3-c4695d7b1a7d
Name: Hassan Khan
Email: hassankhan@gmail.com
Registration: 2026-01-23T09:19:09.192Z
```

---

## 💾 How to Export Participant Data for Research Paper

### Method 1: Query Render Backend API

**Get All Statistics (includes participant count):**
```bash
curl https://architector-analytics.onrender.com/architector/stats
```

**Response Example:**
```json
{
  "total_participants": 1,
  "total_sessions": 2,
  "success_rate": 0.0,
  "average_quality": null,
  "participants": [
    {
      "participant_id": "6b4ec895-8b50-41d8-97e3-c4695d7b1a7d",
      "full_name": "Hassan Khan",
      "email": "hassankhan@gmail.com",
      "designation": "Software Engineer",
      "experience_level": "mid",
      "organization": "NUST",
      "country": "Pakistan",
      "consent_timestamp": "2026-01-23T09:19:09.192Z",
      "extension_version": "2.0.7"
    }
  ],
  "sessions": [ ... ]
}
```

### Method 2: Access Render Database Directly

**Step 1: Add database export endpoint to your backend**

Add this to your `analytics_backend.py` on Render:

```python
@app.route('/architector/export/participants', methods=['GET'])
def export_participants():
    """Export all participant data for research"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get all participants with full details
    c.execute('''SELECT 
                    participant_id,
                    full_name,
                    email,
                    designation,
                    experience_level,
                    organization,
                    country,
                    consent_timestamp,
                    extension_version,
                    (SELECT COUNT(*) FROM sessions WHERE participant_id = p.participant_id) as session_count
                FROM participants p
                ORDER BY consent_timestamp DESC''')
    
    participants = []
    for row in c.fetchall():
        participants.append({
            'participant_id': row[0],
            'full_name': row[1],
            'email': row[2],
            'designation': row[3],
            'experience_level': row[4],
            'organization': row[5],
            'country': row[6],
            'consent_timestamp': row[7],
            'extension_version': row[8],
            'total_sessions': row[9]
        })
    
    conn.close()
    
    return jsonify({
        'total_participants': len(participants),
        'export_timestamp': datetime.now().isoformat(),
        'participants': participants
    }), 200

@app.route('/architector/export/full', methods=['GET'])
def export_full_dataset():
    """Export complete dataset for research paper"""
    conn = sqlite3.connect(DB_PATH)
    
    # Get participants
    participants_df = pd.read_sql_query('SELECT * FROM participants', conn)
    
    # Get sessions
    sessions_df = pd.read_sql_query('SELECT * FROM sessions', conn)
    
    conn.close()
    
    # Demographics analysis
    demographics = {
        'total_participants': len(participants_df),
        'experience_distribution': participants_df['experience_level'].value_counts().to_dict(),
        'country_distribution': participants_df['country'].value_counts().to_dict(),
        'organization_types': participants_df['organization'].value_counts().to_dict()
    }
    
    # Usage analysis
    usage_stats = {
        'total_sessions': len(sessions_df),
        'success_rate': sessions_df['success'].mean() if len(sessions_df) > 0 else 0,
        'avg_generation_time': sessions_df['generation_time'].mean() if len(sessions_df) > 0 else 0,
        'language_distribution': sessions_df['project_language'].value_counts().to_dict(),
        'project_type_distribution': sessions_df['project_type'].value_counts().to_dict()
    }
    
    return jsonify({
        'export_timestamp': datetime.now().isoformat(),
        'demographics': demographics,
        'usage_statistics': usage_stats,
        'participants': participants_df.to_dict('records'),
        'sessions': sessions_df.to_dict('records')
    }), 200
```

**Step 2: Deploy updated backend**
```bash
git add analytics_backend.py
git commit -m "Add participant export endpoints"
git push origin main
# Render will auto-deploy
```

**Step 3: Export data**
```bash
# Export participants only
curl https://architector-analytics.onrender.com/architector/export/participants > participants_data.json

# Export full dataset for paper
curl https://architector-analytics.onrender.com/architector/export/full > research_dataset.json
```

### Method 3: Download SQLite Database from Render

**Step 1: SSH into Render service**
```bash
# From Render Dashboard -> Your Service -> Shell
```

**Step 2: Download database**
```bash
# Inside Render shell
cat analytics.db | base64 > analytics_db.base64
# Copy output and decode locally
```

**Step 3: Decode and open locally**
```bash
# On your Mac
pbpaste | base64 -d > analytics.db

# Query with SQLite
sqlite3 analytics.db "SELECT * FROM participants;"

# Or use Python
python3 << 'EOF'
import sqlite3
import pandas as pd

conn = sqlite3.connect('analytics.db')

# Export participants to CSV
participants = pd.read_sql_query('SELECT * FROM participants', conn)
participants.to_csv('participants.csv', index=False)

# Export sessions to CSV
sessions = pd.read_sql_query('SELECT * FROM sessions', conn)
sessions.to_csv('sessions.csv', index=False)

print(f"✅ Exported {len(participants)} participants")
print(f"✅ Exported {len(sessions)} sessions")

# Print summary
print("\n📊 Participant Demographics:")
print(participants.describe(include='all'))
print("\n📊 Experience Distribution:")
print(participants['experience_level'].value_counts())
print("\n📊 Country Distribution:")
print(participants['country'].value_counts())

conn.close()
EOF
```

---

## 📄 Format for Research Paper

### Table 1: Participant Demographics

```
| ID | Name | Experience | Designation | Organization | Country | Sessions |
|----|------|------------|-------------|--------------|---------|----------|
| P01 | Hassan Khan | Mid (2-5 yrs) | Software Engineer | NUST | Pakistan | 2 |
| P02 | ... | ... | ... | ... | ... | ... |
```

### Table 2: Experience Level Distribution

```python
import pandas as pd

# Generate demographics table
df = pd.read_csv('participants.csv')

experience_map = {
    'junior': '0-2 years',
    'mid': '2-5 years',
    'senior': '5-8 years',
    'principal': '8+ years',
    'lead': 'Leadership',
    'architect': 'Architecture',
    'other': 'Other'
}

df['experience_category'] = df['experience_level'].map(experience_map)

# Create LaTeX table
print("\\begin{table}[h]")
print("\\centering")
print("\\begin{tabular}{|l|c|c|}")
print("\\hline")
print("Experience Level & Count & Percentage \\\\")
print("\\hline")
for exp, count in df['experience_category'].value_counts().items():
    pct = (count / len(df)) * 100
    print(f"{exp} & {count} & {pct:.1f}\\% \\\\")
print("\\hline")
print(f"Total & {len(df)} & 100\\% \\\\")
print("\\hline")
print("\\end{tabular}")
print("\\caption{Participant Experience Distribution}")
print("\\label{tab:demographics}")
print("\\end{table}")
```

### Figure 1: Geographic Distribution

```python
import matplotlib.pyplot as plt

# Create pie chart
country_counts = df['country'].value_counts()
plt.figure(figsize=(10, 6))
plt.pie(country_counts.values, labels=country_counts.index, autopct='%1.1f%%')
plt.title('Participant Geographic Distribution')
plt.savefig('geographic_distribution.png', dpi=300, bbox_inches='tight')
print("✅ Saved: geographic_distribution.png")
```

### Aggregate Statistics (for paper)

```python
# Summary statistics for paper
print("\n📊 RESEARCH PAPER STATISTICS:")
print("=" * 50)
print(f"Total Participants: {len(df)}")
print(f"Unique Organizations: {df['organization'].nunique()}")
print(f"Countries Represented: {df['country'].nunique()}")
print(f"\nExperience Distribution:")
for exp, count in df['experience_level'].value_counts().items():
    pct = (count / len(df)) * 100
    print(f"  {experience_map[exp]}: {count} ({pct:.1f}%)")

# Consent compliance
print(f"\nConsent Compliance: 100% (all {len(df)} participants consented)")
print(f"Data Collection Period: {df['consent_timestamp'].min()} to {df['consent_timestamp'].max()}")
```

---

## 🔒 Privacy & GDPR Compliance for Paper

### Anonymization Guidelines

**For Research Paper:**
1. ❌ **DO NOT** include real names, emails, or participant IDs
2. ✅ **DO** use anonymized codes: P01, P02, P03, etc.
3. ✅ **DO** include: experience level, country, organization type (not name)
4. ✅ **DO** aggregate small groups to prevent identification

**Example Anonymization:**
```python
# Anonymize participant data for paper
df['participant_code'] = ['P' + str(i+1).zfill(2) for i in range(len(df))]
df['org_type'] = df['organization'].apply(lambda x: 
    'Academic' if any(uni in str(x).lower() for uni in ['university', 'nust', 'college']) 
    else 'Industry' if x else 'Independent'
)

# Export anonymized dataset
paper_df = df[['participant_code', 'experience_level', 'org_type', 'country', 'session_count']]
paper_df.to_csv('anonymized_participants.csv', index=False)
```

### Consent Statement for Paper

Include this in your methodology section:

> **Participant Consent:** All participants provided informed consent through the extension's consent dialog. Participants were informed about data collection, usage for academic research, retention period (2 years), and their right to withdraw. The study was conducted in accordance with research ethics guidelines. Participant identities have been anonymized in this paper using codes (P01, P02, etc.).

---

## 🎯 Quick Export Commands

### 1. Export Current Data (Right Now)
```bash
# Get latest data from Render
curl -s https://architector-analytics.onrender.com/architector/stats | jq . > current_stats.json

# View participant count
curl -s https://architector-analytics.onrender.com/architector/stats | jq '.total_participants'

# View all participant details (after adding export endpoint)
curl -s https://architector-analytics.onrender.com/architector/export/participants | jq .
```

### 2. Check Render Logs for Registrations
```bash
# From Render Dashboard -> Logs, search for:
# "✅ Registered participant:"
# "📊 Logged session:"
```

### 3. View Local VS Code Storage
```bash
# macOS
cd ~/Library/Application\ Support/Code/User/globalStorage/enghammadkhurshid.architector-llm/

# Check if analytics directory exists
ls -la

# If exists, view files
cat analytics/sessions.jsonl | jq
```

---

## 📊 Sample Research Paper Sections

### Methodology Section

```latex
\subsection{Participant Recruitment}

Participants were recruited through voluntary consent when using the Architector-LLM VS Code extension. Upon first use, developers were presented with an informed consent dialog explaining:
\begin{itemize}
    \item Study purpose: "From Code to Architecture: Leveraging LLMs for Automated Software Design Documentation"
    \item Data collected: professional information, usage statistics, project metadata, and performance metrics
    \item Data not collected: source code, proprietary details, passwords
    \item Rights: withdraw consent anytime, request data deletion, contact researcher
\end{itemize}

Participants who consented provided the following information:
\begin{itemize}
    \item Full name and email address
    \item Job title/designation
    \item Experience level (0-2 years, 2-5 years, 5-8 years, 8+ years, leadership, architecture)
    \item Organization/company (optional)
    \item Country (optional)
\end{itemize}

\subsection{Data Collection}

Data collection occurred from January 2026 to [end date], with \textbf{N} total participants from \textbf{X} countries. All data was stored securely on a GDPR-compliant backend (Render.com) using encrypted transmission (HTTPS) and anonymized participant identifiers (UUID v4).
```

### Results Section

```latex
\subsection{Participant Demographics}

Table~\ref{tab:demographics} presents the demographic characteristics of study participants. The majority of participants (XX\%) were mid-level developers with 2-5 years of experience, followed by senior developers (XX\%). Participants represented diverse geographic locations, with XX\% from Asia, XX\% from North America, and XX\% from other regions.

[Insert Table 1: Experience Distribution]
[Insert Figure 1: Geographic Distribution]
```

---

## 🚀 Current Status

**Your Backend is LIVE and collecting data!**

**Confirmed Participant:**
- ✅ Name: Hassan Khan
- ✅ Email: hassankhan@gmail.com
- ✅ Participant ID: 6b4ec895-8b50-41d8-97e3-c4695d7b1a7d
- ✅ Registered: 2026-01-23T09:19:09Z
- ✅ Sessions: 2 (both PHP projects, testing phase)

**Next Steps:**
1. Add export endpoints to backend (see Method 2 above)
2. Deploy updated backend to Render
3. Export data using: `curl https://architector-analytics.onrender.com/architector/export/full > research_dataset.json`
4. Analyze using Python scripts above
5. Create anonymized tables for paper
6. Continue collecting data from more participants

---

## 📞 Support

**Questions?** Contact researcher: engr.hammadkhurshid@gmail.com
**Data Issues?** Check Render logs: https://dashboard.render.com

**File Location:** Save all exported data to:
```
/Users/hammadkhurshidchughtaii/Downloads/Architector LLM/research_data/
├── participants.csv (anonymized)
├── sessions.csv
├── research_dataset.json (full export)
├── demographics_table.tex (for LaTeX)
└── figures/
    ├── geographic_distribution.png
    └── experience_distribution.png
```
