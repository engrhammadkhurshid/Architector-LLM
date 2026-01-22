# 🚀 Quick Installation Guide

Install and use Architector-LLM VS Code extension in 5 minutes.

---

## Prerequisites Check

Before installing, ensure you have:

- ✅ **VS Code** 1.85.0 or later
- ✅ **Python 3.9+** installed (`python3 --version`)
- ✅ **Ollama** running (`curl http://localhost:11434/api/tags`)
- ✅ **DeepSeek Model** downloaded

---

## Step 1: Install Extension

```bash
cd "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM"
code --install-extension architector-llm-1.0.0.vsix
```

**Expected output:**
```
Installing extension 'architector-llm'...
Extension 'architector-llm' was successfully installed.
```

---

## Step 2: Verify Installation

1. Open VS Code
2. Look for "Architector" in the status bar (bottom right)
3. Click it to test the extension

---

## Step 3: Install Dependencies

Run in terminal:

```bash
# Install Ollama (if not installed)
curl https://ollama.ai/install.sh | sh

# Start Ollama server
ollama serve &

# Pull DeepSeek Coder model
ollama pull deepseek-coder:6.7b

# Install Python dependencies
pip3 install tree-sitter

# Optional: Install Mermaid CLI for image rendering
npm install -g @mermaid-js/mermaid-cli
```

---

## Step 4: Check Dependencies in VS Code

1. Open VS Code Command Palette (`Cmd+Shift+P` on Mac, `Ctrl+Shift+P` on Windows/Linux)
2. Type: `Architector: Check Dependencies`
3. Press Enter
4. A panel will open showing dependency status
5. If anything is missing, follow the installation commands shown

---

## Step 5: Generate Documentation

### Method 1: Status Bar (Quick)
1. Open your project folder in VS Code
2. Click "Architector" in the status bar
3. Enter version (e.g., `1.0.0`)
4. Watch the progress panel

### Method 2: Command Palette
1. `Cmd+Shift+P` (or `Ctrl+Shift+P`)
2. Type: `Architector: Generate Architecture Documentation`
3. Enter version
4. Documentation generation starts

### Method 3: Command Line (Fallback)
```bash
python3 architector.py /path/to/your/project 1.0.0
```

---

## 📂 Output Location

Documentation is generated in:
```
your-project/
└── docs/
    └── arch/
        └── v1.0.0_2026-01-23-HHMMSS_gitHash/
            ├── README.md           # Main documentation
            ├── INDEX.md            # Enhanced navigation
            ├── QUALITY_REPORT.md   # Quality metrics
            ├── RELATIONSHIPS.md    # Cross-diagram connections
            ├── COMPARISONS.md      # Diagram comparisons
            └── diagrams/           # Mermaid diagram files
                ├── component.mmd
                ├── class.mmd
                ├── sequence.mmd
                └── ...
```

---

## 🎯 Quick Test

Test the extension with the included test project:

```bash
cd "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM"
code test-flask-app

# In VS Code:
# 1. Click "Architector" in status bar
# 2. Enter version: 1.0.0
# 3. Wait ~30-40 seconds
# 4. Open: test-flask-app/docs/arch/v1.0.0_*/README.md
```

**Expected Result:**
- 5 diagrams generated
- Quality score: ~80-85/100
- Time: 30-40 seconds

---

## ⚠️ Troubleshooting

### Extension not appearing?
```bash
# Restart VS Code
# Or reload window: Cmd+R (Mac) or Ctrl+R (Windows/Linux)
```

### "Ollama not running" error?
```bash
# Start Ollama
ollama serve

# Test it's working
curl http://localhost:11434/api/tags
```

### "Model not found" error?
```bash
# Download the model
ollama pull deepseek-coder:6.7b

# Verify it's available
ollama list
```

### Python import errors?
```bash
# Install tree-sitter
pip3 install tree-sitter

# Verify installation
python3 -c "import tree_sitter; print('OK')"
```

### Extension crashes during generation?
```bash
# Run from command line to see full error
cd "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM"
python3 architector.py /path/to/project 1.0.0
```

---

## 📊 Expected Performance

| Project Size | Files | Time | Diagrams | Quality |
|--------------|-------|------|----------|---------|
| Small (< 10 files) | 4-10 | 30-60s | 3-5 | 80-90/100 |
| Medium (10-50 files) | 10-50 | 1-3 min | 5-8 | 75-85/100 |
| Large (50+ files) | 50+ | 3-10 min | 8-10 | 70-80/100 |

---

## 🎉 Success Indicators

You'll know it's working when you see:

1. ✅ Status bar shows "Architector" button
2. ✅ Dependency check shows all green checkmarks
3. ✅ Progress panel appears during generation
4. ✅ Success notification with "Open Documentation" button
5. ✅ README.md opens with architecture documentation

---

## 📞 Need Help?

- **Check logs:** VS Code Output panel → "Architector-LLM"
- **Review docs:** See [BUGS_FIXED_EXTENSION_BUILT.md](BUGS_FIXED_EXTENSION_BUILT.md)
- **Full guide:** See [SETUP_GUIDE.md](SETUP_GUIDE.md)

---

**Installation Time:** ~5 minutes  
**First Run Time:** ~30-60 seconds  
**Ready to Use:** ✅ Yes!
