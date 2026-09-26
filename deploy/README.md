# Architector-LLM Analytics Backend Deployment

## 🚀 Free Hosting Options

### Option 1: Render.com (⭐ RECOMMENDED)

**Pros:**
- ✅ Easy deployment from GitHub
- ✅ Automatic HTTPS
- ✅ Persistent disk storage
- ✅ 750 hours/month free (enough for always-on)
- ✅ Great for Python/Flask apps

**Cons:**
- ⚠️ Goes to sleep after 15 mins inactivity
- ⚠️ 100GB/month bandwidth limit

**Steps:**

1. **Create GitHub repository:**
   ```bash
   cd "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM"
   git init
   git add analytics_backend.py backend-deploy/
   git commit -m "Add analytics backend"
   git remote add origin https://github.com/engrhammadkhurshid/architector-analytics.git
   git push -u origin main
   ```

2. **Deploy to Render:**
   - Go to https://render.com
   - Sign up with GitHub
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Render auto-detects Python and uses render.yaml
   - Click "Create Web Service"

3. **Get your URL:**
   ```
   https://architector-analytics.onrender.com
   ```

4. **Add persistent disk:**
   - Dashboard → Your service → Settings
   - Add Disk: `/app/analytics_data` (1GB free)
   - Redeploy

---

### Option 2: Railway.app

**Pros:**
- ✅ $5 free credit/month (500 hours)
- ✅ No sleep time
- ✅ Very fast deployments
- ✅ Great developer experience

**Cons:**
- ⚠️ Limited free credits (not always-on beyond ~500 hours)

**Steps:**

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and deploy:**
   ```bash
   cd "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM"
   railway login
   railway init
   railway up
   ```

3. **Get your URL:**
   ```bash
   railway domain
   ```

---

### Option 3: Fly.io

**Pros:**
- ✅ 3 shared VMs free
- ✅ Persistent volumes (3GB free)
- ✅ Good global performance
- ✅ No sleep time

**Cons:**
- ⚠️ Slightly more complex setup

**Steps:**

1. **Install flyctl:**
   ```bash
   brew install flyctl
   ```

2. **Login and deploy:**
   ```bash
   cd "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM"
   flyctl auth login
   flyctl launch --config backend-deploy/fly.toml
   flyctl deploy
   ```

3. **Create volume for data:**
   ```bash
   flyctl volumes create analytics_data --size 1
   ```

---

### Option 4: PythonAnywhere (Simple but Limited)

**Pros:**
- ✅ Specifically for Python
- ✅ Very simple setup
- ✅ Always on

**Cons:**
- ⚠️ 512MB disk space limit
- ⚠️ 100k daily requests limit
- ⚠️ Custom domain not on free tier

**Steps:**

1. Go to https://www.pythonanywhere.com
2. Sign up for free account
3. Upload `analytics_backend.py`
4. Configure web app:
   - Framework: Flask
   - Python version: 3.10
   - Working directory: /home/yourusername/
5. Your URL: `https://yourusername.pythonanywhere.com`

---

## 📝 Setup Guide (Render.com - Recommended)

### Step 1: Prepare GitHub Repository

```bash
cd "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM"

# Initialize git if not already done
git init

# Create .gitignore
echo "analytics_data/" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore

# Copy analytics backend to root
cp analytics_backend.py ./

# Create requirements.txt
cat > requirements.txt << 'EOF'
flask==3.0.0
flask-cors==4.0.0
gunicorn==21.2.0
python-dotenv==1.0.0
EOF

# Commit files
git add analytics_backend.py requirements.txt .gitignore backend-deploy/
git commit -m "Initial commit: Analytics backend for Architector-LLM"

# Create GitHub repo (via GitHub website)
# Then push:
git remote add origin https://github.com/engrhammadkhurshid/architector-analytics.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Render

1. **Sign up:**
   - Go to https://render.com
   - Click "Get Started for Free"
   - Sign up with GitHub account

2. **Create web service:**
   - Dashboard → "New" → "Web Service"
   - Connect GitHub account
   - Select `architector-analytics` repository
   - Configure:
     - **Name:** architector-analytics
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn -w 4 -b 0.0.0.0:$PORT analytics_backend:app`
     - **Plan:** Free

3. **Add persistent storage:**
   - Service → Settings → Disks
   - Add Disk:
     - **Name:** analytics-data
     - **Mount Path:** `/app/analytics_data`
     - **Size:** 1 GB (free)
   - Save Changes → Manual Deploy

4. **Get your URL:**
   ```
   https://architector-analytics.onrender.com
   ```

5. **Test endpoints:**
   ```bash
   curl https://architector-analytics.onrender.com/health
   curl https://architector-analytics.onrender.com/architector/stats
   ```

### Step 3: Update Extension URLs

Edit these files to use your new backend URL:

**File 1:** `vscode-extension/src/analytics/developerInfo.ts`

Find and replace:
```typescript
// Line ~122
await fetch('https://research.nust.edu.pk/architector/register', {

// Replace with:
await fetch('https://architector-analytics.onrender.com/architector/register', {
```

**File 2:** `vscode-extension/src/analytics/telemetry.ts`

Find and replace:
```typescript
// Line ~225
await fetch('https://research.nust.edu.pk/architector/analytics', {

// Replace with:
await fetch('https://architector-analytics.onrender.com/architector/analytics', {
```

### Step 4: Rebuild Extension

```bash
cd "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM/vscode-extension"
npm run compile
cd ..
npx vsce package --out architector-llm-2.0.1.vsix
```

### Step 5: Test Everything

```bash
# 1. Test backend health
curl https://architector-analytics.onrender.com/health

# 2. Test registration (simulate extension)
curl -X POST https://architector-analytics.onrender.com/architector/register \
  -H "Content-Type: application/json" \
  -d '{
    "participantId": "test-123",
    "fullName": "Test User",
    "email": "test@example.com",
    "designation": "Developer",
    "experienceLevel": "mid",
    "consentTimestamp": "2026-01-23T10:00:00Z",
    "consentVersion": "1.0"
  }'

# 3. View stats
curl https://architector-analytics.onrender.com/architector/stats
```

---

## 🔒 Security Best Practices

### Add Authentication

Update `analytics_backend.py` to require API key:

```python
import os
from functools import wraps
from flask import request

API_KEY = os.getenv('ANALYTICS_API_KEY', 'your-secret-key-here')

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        key = request.headers.get('X-API-Key')
        if key != API_KEY:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Apply to endpoints:
@app.route('/architector/register', methods=['POST'])
@require_api_key
def register_participant():
    # ... existing code
```

Then in Render:
1. Settings → Environment
2. Add: `ANALYTICS_API_KEY` = `generate-random-secure-key`

Update extension to include header:
```typescript
headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'your-api-key-here'
}
```

### Enable HTTPS Only

Already enabled by default on Render, Railway, and Fly.io!

### Rate Limiting

Add to `analytics_backend.py`:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

# Apply to sensitive endpoints:
@app.route('/architector/register', methods=['POST'])
@limiter.limit("10 per hour")
def register_participant():
    # ... existing code
```

---

## 📊 View Analytics Dashboard

### Web Interface

Access your stats at:
```
https://architector-analytics.onrender.com/architector/stats
```

### Download Data

```bash
# SSH into Render (if you upgrade to paid)
# Or use Render's file browser in Dashboard

# Download participants
curl https://architector-analytics.onrender.com/architector/stats > stats.json

# For full data, add admin endpoint to analytics_backend.py
```

### Local Analysis

Create `analyze.py` to process JSONL files:

```python
import json
import pandas as pd

# Load sessions
sessions = []
with open('analytics_data/sessions.jsonl') as f:
    for line in f:
        sessions.append(json.loads(line))

df = pd.DataFrame(sessions)

# Analysis for paper
print(f"Total Sessions: {len(df)}")
print(f"Success Rate: {df['success'].mean() * 100:.1f}%")
print(f"Avg Quality: {df['qualityScore'].mean():.1f}")
print("\nLanguage Distribution:")
print(df['projectLanguage'].value_counts())
```

---

## 💡 Recommended Choice

**For your use case, I recommend Render.com:**

✅ **Why Render:**
- Easiest GitHub integration
- Automatic HTTPS
- Persistent disk for free
- Good for research projects (not high-traffic)
- No credit card required
- Great for academic use

⚠️ **Limitation:**
- Service sleeps after 15 mins inactivity
- Takes ~30 seconds to wake up
- Solution: Extension already handles this (falls back to local logging)

---

## 🚀 Quick Start Command

```bash
# 1. Create GitHub repo and push
cd "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM"
git init
git add analytics_backend.py requirements.txt .gitignore
git commit -m "Analytics backend"
git remote add origin https://github.com/engrhammadkhurshid/architector-analytics.git
git push -u origin main

# 2. Deploy to Render (via website - takes 2 minutes)

# 3. Update extension with your URL and rebuild
# 4. Test with curl commands above

# Done! 🎉
```

---

## 📞 Support

Need help? Contact: engr.hammadkhurshid@gmail.com

Choose Render for simplicity, or Railway/Fly if you want more control!
