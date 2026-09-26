# 📦 Extension Distribution & Testing Guide

## 🎯 Quick Answer to Your Questions:

### 1️⃣ **Does the extension require downloading LLM?**
**YES** - By default, the extension uses **Ollama (local LLM)** which requires:
- Installing Ollama on the user's machine
- Downloading DeepSeek Coder 6.7B model (~3.8 GB)
- Running Ollama server locally

**Alternative:** Users can switch to DeepSeek API (requires API key and internet).

---

## 🧪 How to Test Extension Locally (For You)

### Method 1: Install from .vsix file (Recommended)

```bash
# 1. Open terminal in the extension folder
cd "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM"

# 2. Install the extension
code --install-extension architector-llm-1.0.0.vsix

# 3. Restart VS Code
# Press Cmd+Shift+P → "Developer: Reload Window"
```

### Method 2: Test in Development Mode

```bash
# 1. Open the extension folder in VS Code
code "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM"

# 2. Press F5 (or Cmd+Shift+D → Run "Extension")
# This opens a new VS Code window with the extension loaded

# 3. In the new window, open any project and test
```

### Method 3: Direct Installation Command
```bash
# One-line install
code --install-extension "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM/architector-llm-1.0.0.vsix"
```

---

## 👥 How to Ship Extension to Users

### Option 1: Direct Distribution (Private/Testing)

**Package:** Already done! ✅ `architector-llm-1.0.0.vsix` (252.83 KB)

**Users install via:**
```bash
code --install-extension architector-llm-1.0.0.vsix
```

**Or via VS Code UI:**
1. Open VS Code
2. Extensions panel (Cmd+Shift+X)
3. Click "..." menu → "Install from VSIX..."
4. Select `architector-llm-1.0.0.vsix`

**Distribution methods:**
- ✉️ Email the .vsix file
- ☁️ Upload to Google Drive / Dropbox / OneDrive
- 🐙 GitHub Release (recommended for research)
- 🌐 Host on university server

---

### Option 2: VS Code Marketplace (Public)

**Steps to publish:**

1. **Create Publisher Account:**
```bash
# Install vsce
npm install -g @vscode/vsce

# Create Personal Access Token (PAT) at:
# https://dev.azure.com/[YOUR_ORG]/_usersSettings/tokens

# Login
vsce login [publisher-name]
```

2. **Publish:**
```bash
cd "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM"
vsce publish
```

3. **Update:**
```bash
# For future updates
vsce publish patch  # 1.0.0 → 1.0.1
vsce publish minor  # 1.0.0 → 1.1.0
vsce publish major  # 1.0.0 → 2.0.0
```

**Marketplace benefits:**
- ✅ Automatic updates
- ✅ Easy discovery
- ✅ Built-in analytics
- ✅ User ratings/reviews

**Note:** For academic research, marketplace is optional. Direct distribution is fine.

---

### Option 3: GitHub Release (Best for Research)

**Recommended for your use case:**

```bash
# 1. Create GitHub repository (if not exists)
git init
git add .
git commit -m "Initial release"
git remote add origin https://github.com/engrhammadkhurshid/architector-llm.git
git push -u origin main

# 2. Create a release
# Go to: https://github.com/engrhammadkhurshid/architector-llm/releases
# Click "Create a new release"
# Tag: v1.0.0
# Title: Architector-LLM v1.0.0 - Research Prototype
# Upload: architector-llm-1.0.0.vsix

# 3. Users download from:
# https://github.com/engrhammadkhurshid/architector-llm/releases/latest
```

**Installation from GitHub:**
```bash
# Users download the .vsix and run:
code --install-extension architector-llm-1.0.0.vsix
```

---

## 🔧 User Requirements (What They Need)

### Required Software:

1. **VS Code** (1.85.0 or later)
   ```bash
   # Check version
   code --version
   ```

2. **Python 3.9+**
   ```bash
   python3 --version
   ```

3. **Ollama** (for local LLM)
   ```bash
   # macOS
   brew install ollama
   
   # Or download from: https://ollama.ai
   
   # Start Ollama server
   ollama serve
   ```

4. **DeepSeek Coder Model** (~3.8 GB download)
   ```bash
   ollama pull deepseek-coder:6.7b
   ```

5. **Python Dependencies**
   ```bash
   pip3 install tree-sitter
   ```

6. **Optional: Mermaid CLI** (for rendering diagrams to images)
   ```bash
   npm install -g @mermaid-js/mermaid-cli
   ```

---

## 🚀 Current Configuration

Your extension is configured to use **Ollama by default**:

**File:** `backend/src/pipeline.py` (Line 36)
```python
llm_provider = os.getenv('LLM_PROVIDER', 'deepseek').lower()
if llm_provider == 'ollama':
    self.llm_client = OllamaClient()
else:
    self.llm_client = LLMClient()  # DeepSeek API
```

**Current default:** `'deepseek'` (but should be `'ollama'` for local use)

**To use Ollama by default (recommended for users without API keys):**
- Change line 36 to: `llm_provider = os.getenv('LLM_PROVIDER', 'ollama').lower()`

**To use DeepSeek API:**
- User creates `.env` file with: `DEEPSEEK_API_KEY=sk-xxxxx`

---

## 🧪 Testing Steps for You

### Test 1: Install Extension
```bash
cd "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM"
code --install-extension architector-llm-1.0.0.vsix
```

### Test 2: Check Installation
1. Open VS Code
2. Check Extensions panel (Cmd+Shift+X)
3. Search "Architector"
4. Should see your extension with logo

### Test 3: Check Dependencies
1. Open Command Palette (Cmd+Shift+P)
2. Type: "Architector: Check Dependencies"
3. Should show all dependencies status

### Test 4: Generate Documentation
1. Open `test-flask-app` folder in VS Code
2. Click "Architector" in status bar (bottom right)
3. Enter version: `1.0.0`
4. Watch progress panel
5. Check output in `test-flask-app/docs/arch/`

### Test 5: View About Page
1. Command Palette → "Architector: About Architector-LLM"
2. Should see your logo and all credits

---

## 📋 Distribution Checklist

For sharing with users/reviewers:

- [x] Extension packaged: `architector-llm-1.0.0.vsix` ✅
- [x] Logo included ✅
- [x] Credits updated ✅
- [ ] Create installation guide (README.md)
- [ ] Test on clean machine
- [ ] Create demo video (optional)
- [ ] Upload to GitHub releases
- [ ] Share installation instructions

---

## 📄 Sample README for Users

Create a `README.md` in your GitHub repo:

```markdown
# Architector-LLM

Automated Architecture Documentation Generation using LLMs

## Installation

1. Download `architector-llm-1.0.0.vsix` from [Releases](https://github.com/engrhammadkhurshid/architector-llm/releases)
2. Install: `code --install-extension architector-llm-1.0.0.vsix`
3. Install dependencies:
   - Ollama: https://ollama.ai
   - Model: `ollama pull deepseek-coder:6.7b`
   - Python: `pip3 install tree-sitter`

## Usage

1. Open your project in VS Code
2. Click "Architector" in status bar
3. Enter version number
4. Documentation generated in `docs/arch/`

## Research Paper

This is a prototype for: "From Code to Architecture: Leveraging LLMs for Automated Software Design Documentation"

Author: Engr. Hammad Khurshid, NUST Pakistan
```

---

## 🔄 Alternative: Use DeepSeek API (No Local LLM)

If you want users to avoid downloading 3.8 GB model:

1. **Change default provider** in `backend/src/pipeline.py`:
   ```python
   llm_provider = os.getenv('LLM_PROVIDER', 'ollama').lower()
   ```

2. **Users create `.env` file:**
   ```
   LLM_PROVIDER=deepseek
   DEEPSEEK_API_KEY=your-api-key-here
   ```

3. **Get API key from:** https://platform.deepseek.com/

**Pros:** No large download, works anywhere  
**Cons:** Requires API key, costs money, needs internet

---

## 🎬 Next Steps

1. **Test locally:** `code --install-extension architector-llm-1.0.0.vsix`
2. **Create GitHub repo:** Push code + release .vsix
3. **Write installation guide:** For users/reviewers
4. **Optional:** Record demo video
5. **Share:** Send .vsix file or GitHub link

---

**Your extension is ready to ship!** 🚀

For research purposes, GitHub releases + email distribution is the most common approach.
