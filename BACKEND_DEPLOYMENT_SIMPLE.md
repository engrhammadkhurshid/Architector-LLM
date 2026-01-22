# 🎯 Architector-LLM Backend: 3-Step Deployment

## Overview

You need a backend server to collect analytics data from your VS Code extension. Here's the simplest way to set it up **for free**.

---

## ⚡ Quick Start (8 minutes total)

### Step 1: Prepare Code (2 minutes)

```bash
cd "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM"

# Create GitHub repository
# Go to https://github.com/new
# - Name: architector-analytics
# - Private repository (recommended)
# - Don't initialize with README

# Initialize git
git init
git add analytics_backend.py requirements.txt .gitignore backend-deploy/
git commit -m "Add analytics backend"

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/architector-analytics.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Render (5 minutes)

1. **Sign up:**
   - Go to https://render.com
   - Click "Get Started for Free"
   - Sign up with your GitHub account

2. **Create service:**
   - Click "New +" → "Web Service"
   - Select "architector-analytics" repository
   - Render auto-detects Python
   - Click "Create Web Service"

3. **Add storage:**
   - Wait for initial deployment
   - Go to Settings → Disks
   - Add Disk: 
     - Name: `analytics-data`
     - Path: `/app/analytics_data`
     - Size: 1 GB
   - Click "Save" → "Manual Deploy"

4. **Copy your URL:**
   ```
   https://architector-analytics.onrender.com
   ```

### Step 3: Update Extension (1 minute)

Open these two files and update the URLs:

**File 1:** `vscode-extension/src/analytics/developerInfo.ts`
```typescript
// Find line ~122 and ~217, replace:
'https://research.nust.edu.pk/architector/...'
// with:
'https://architector-analytics.onrender.com/architector/...'
```

**File 2:** `vscode-extension/src/analytics/telemetry.ts`
```typescript
// Find line ~225, replace:
'https://research.nust.edu.pk/architector/analytics'
// with:
'https://architector-analytics.onrender.com/architector/analytics'
```

**Rebuild:**
```bash
cd vscode-extension
npm run compile
cd ..
npx vsce package --out architector-llm-2.0.1.vsix
```

---

## ✅ Test Your Backend

```bash
# 1. Test health
curl https://architector-analytics.onrender.com/health

# Expected: {"status":"healthy","service":"Architector Analytics Backend"}

# 2. Test registration
curl -X POST https://architector-analytics.onrender.com/architector/register \
  -H "Content-Type: application/json" \
  -d '{"participantId":"test-123","fullName":"Test User","email":"test@test.com","designation":"Dev","experienceLevel":"mid","consentTimestamp":"2026-01-23T10:00:00Z","consentVersion":"1.0"}'

# Expected: {"status":"success","participantId":"test-123"}

# 3. View stats
curl https://architector-analytics.onrender.com/architector/stats

# Expected: {"participants":1,"sessions":0,...}
```

---

## 📊 View Your Analytics

### Quick Stats (Browser)
```
https://architector-analytics.onrender.com/architector/stats
```

Shows:
- Total participants
- Total sessions
- Success rate
- Average quality score
- Language distribution

### Full Data Export

1. **Via Render Dashboard:**
   - Log in to Render
   - Your service → Shell
   - `cat analytics_data/sessions.jsonl`

2. **Add Download Endpoint:**

Add to `analytics_backend.py`:
```python
@app.route('/architector/export', methods=['GET'])
def export_data():
    """Export all data (admin only - add auth!)"""
    sessions = []
    if SESSIONS_FILE.exists():
        with open(SESSIONS_FILE, 'r') as f:
            sessions = [json.loads(line) for line in f]
    
    return jsonify({'sessions': sessions}), 200
```

Then:
```bash
curl https://architector-analytics.onrender.com/architector/export > my_data.json
```

---

## 🔒 Secure Your Backend (Optional but Recommended)

### Add API Key Authentication

Update `analytics_backend.py`:

```python
import os

# At the top
API_KEY = os.getenv('ANALYTICS_API_KEY', 'change-this-secret-key')

# Before each endpoint
from functools import wraps

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get('X-API-Key')
        if key != API_KEY:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/architector/register', methods=['POST'])
@require_api_key  # Add this line
def register_participant():
    # ... existing code
```

In Render Dashboard:
- Settings → Environment
- Add variable: `ANALYTICS_API_KEY` = `your-random-secure-key-here`
- Save & Redeploy

Update extension to send key:
```typescript
headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'your-random-secure-key-here'
}
```

---

## 💰 Costs

**Free tier includes:**
- ✅ 750 hours/month (enough for always-on)
- ✅ 1GB persistent storage
- ✅ 100GB bandwidth/month
- ✅ Automatic HTTPS
- ✅ Custom domain

**If you exceed free tier:**
- $7/month for unlimited uptime
- (Very unlikely for research project with <500 users)

---

## 🚨 Troubleshooting

### "Service unavailable" error
**Cause:** Service went to sleep (after 15 mins inactivity)  
**Solution:** Wait 30 seconds, it will wake up automatically  
**Prevention:** Extension falls back to local logging

### "Push rejected" on git push
**Cause:** Authentication failed  
**Solution:** 
```bash
git remote set-url origin https://YOUR_USERNAME:YOUR_TOKEN@github.com/YOUR_USERNAME/architector-analytics.git
```

### Can't see data in Render
**Cause:** Disk not mounted  
**Solution:** Settings → Disks → Add `/app/analytics_data`

### Backend logs showing errors
**Check logs:**
- Render Dashboard → Your service → Logs
- Look for Python errors
- Common: missing environment variables

---

## 📱 Alternative: Automated Script

If you prefer automation:

```bash
cd "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM"
./backend-deploy/DEPLOYMENT_COMMANDS.sh
```

Choose option 1 (Render) and follow prompts.

---

## 📚 Additional Resources

- **Full deployment guide:** `backend-deploy/README.md`
- **Platform comparison:** `backend-deploy/PLATFORM_COMPARISON.md`
- **Render docs:** https://render.com/docs
- **Flask docs:** https://flask.palletsprojects.com/

---

## 🎓 For Your Research Paper

Once deployed, you can report:

> "Analytics data was collected through a secure backend service hosted on 
> Render.com, with all communications encrypted via HTTPS. Participant data 
> was stored in isolated persistent storage, accessible only to the research 
> team. The service endpoint URL was: https://architector-analytics.onrender.com"

---

## ✅ Checklist

- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Web service deployed
- [ ] Persistent disk added
- [ ] Backend URL obtained
- [ ] Extension URLs updated
- [ ] Extension rebuilt (v2.0.1)
- [ ] Backend tested with curl
- [ ] Extension tested with real user

---

**🚀 You're ready to deploy! Start with Step 1 above.**

Questions? engr.hammadkhurshid@gmail.com
