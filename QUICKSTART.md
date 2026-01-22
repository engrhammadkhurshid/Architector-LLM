# Quick Start Reference - Architector-LLM

This is a quick reference for common commands and workflows.

## 🚀 Starting Development

```bash
# Navigate to project
cd "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM"

# Start backend server
PYTHONPATH=backend/src python3 backend/src/main.py

# Or use npm script
npm run start-backend

# In another terminal: Watch TypeScript compilation
npm run watch
```

## 🧪 Testing

```bash
# Test backend health
curl http://localhost:8765/health

# Test generation endpoint
curl -X POST http://localhost:8765/generate \
  -H "Content-Type: application/json" \
  -d '{"codebase_path":"."}'

# Run Python tests
cd backend && pytest tests/ -v

# Run setup test
python3 test_setup.py
```

## 🔧 Common Commands

```bash
# Install dependencies
npm install
pip3 install -r backend/requirements.txt

# Compile TypeScript
npm run compile

# Format Python code
cd backend && black src/

# Lint Python code
cd backend && flake8 src/

# Kill backend if stuck
lsof -ti:8765 | xargs kill -9
```

## 📁 Key Files

| File | Purpose |
|------|---------|
| `.env` | API keys and configuration |
| `package.json` | Frontend dependencies & commands |
| `backend/requirements.txt` | Python dependencies |
| `src/extension.ts` | VS Code extension entry point |
| `backend/src/main.py` | Backend server |
| `PROJECT_STATUS.md` | Current project status |

## 🎯 VS Code Extension Development

```bash
# 1. Open project in VS Code
code .

# 2. Press F5 to launch Extension Development Host

# 3. In new window, open Command Palette (Cmd+Shift+P)

# 4. Type "Architector" to see commands:
#    - Generate Architecture Documentation
#    - Start Backend Server
#    - Stop Backend Server
```

## 📝 Environment Variables

```bash
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DEEPSEEK_API_URL=https://api.deepseek.com/v1
BACKEND_HOST=localhost
BACKEND_PORT=8765
LLM_TEMPERATURE=0.2
LLM_MAX_TOKENS=4096
LLM_MODEL=deepseek-coder
OUTPUT_BASE_DIR=docs/arch
```

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port is in use
lsof -i:8765

# Kill process
lsof -ti:8765 | xargs kill -9

# Check for Python errors
python3 backend/src/main.py
```

### Import errors
```bash
# Set PYTHONPATH
export PYTHONPATH="${PWD}/backend/src"

# Or use in command
PYTHONPATH=backend/src python3 backend/src/main.py
```

### Extension not loading
```bash
# Clean and rebuild
rm -rf out/
npm run compile

# Check for errors in VS Code
# View → Output → Select "Extension Host"
```

## 📚 Documentation

- [SETUP.md](docs/SETUP.md) - Full installation guide
- [USAGE.md](docs/USAGE.md) - How to use the extension
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Technical details
- [DEVELOPMENT.md](docs/DEVELOPMENT.md) - Contributing guide
- [PROJECT_STATUS.md](PROJECT_STATUS.md) - Current progress

## 🏗️ Project Structure

```
├── src/                 # TypeScript frontend
├── backend/src/         # Python backend
│   ├── parser/         # Code parsing
│   ├── llm/            # LLM integration
│   ├── diagram/        # Diagram rendering
│   └── output/         # Output organization
├── docs/               # Documentation
└── out/                # Compiled TypeScript
```

## 🎓 Next Steps

See [PROJECT_STATUS.md](PROJECT_STATUS.md) for:
- Current phase and milestone
- What's been completed
- What's next to implement
- Testing results

---

**Current Status:** Phase 1.1 Complete ✅ | **Next:** Phase 1.2 - Parser Implementation
