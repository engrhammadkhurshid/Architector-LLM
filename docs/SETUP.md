# Setup Guide - Architector-LLM

This guide will help you set up and configure the Architector-LLM development environment.

## Prerequisites

### Required Software

1. **Node.js** (v18 or higher)
   - Download from: https://nodejs.org/
   - Verify installation: `node --version`

2. **Python** (v3.9 or higher)
   - Download from: https://www.python.org/
   - Verify installation: `python3 --version`

3. **VS Code** (v1.85.0 or higher)
   - Download from: https://code.visualstudio.com/

4. **Git**
   - Download from: https://git-scm.com/
   - Verify installation: `git --version`

### Optional but Recommended

- **Mermaid CLI** (for diagram rendering)
  ```bash
  npm install -g @mermaid-js/mermaid-cli
  ```

## Installation Steps

### 1. Clone/Navigate to Project Directory

```bash
cd "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM"
```

### 2. Install Frontend Dependencies

```bash
npm install
```

This will install:
- TypeScript compiler
- VS Code extension development tools
- Axios (for HTTP requests)
- dotenv (for environment variables)

### 3. Install Backend Dependencies

```bash
cd backend
pip3 install -r requirements.txt
```

This will install:
- Flask (HTTP server)
- Flask-CORS (for cross-origin requests)
- Tree-sitter (code parsing)
- python-dotenv (environment variables)
- requests (HTTP client for LLM API)

### 4. Configure Environment Variables

The `.env` file should already be created in the project root. Verify it contains:

```bash
# DeepSeek API Configuration
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DEEPSEEK_API_URL=https://api.deepseek.com/v1

# Backend Configuration
BACKEND_HOST=localhost
BACKEND_PORT=8765

# LLM Configuration
LLM_TEMPERATURE=0.2
LLM_MAX_TOKENS=4096
LLM_MODEL=deepseek-coder

# Output Configuration
OUTPUT_BASE_DIR=docs/arch
```

**⚠️ Security Note:** Never commit the `.env` file to version control. It's already in `.gitignore`.

### 5. Compile TypeScript

```bash
npm run compile
```

This compiles the TypeScript source files to JavaScript in the `out/` directory.

## Testing the Installation

### Test 1: Backend Server

Start the backend server:

```bash
npm run start-backend
```

You should see:
```
Starting Architector-LLM Backend Server on localhost:8765
```

Test the health endpoint (in a new terminal):
```bash
curl http://localhost:8765/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "service": "architector-llm-backend"
}
```

### Test 2: VS Code Extension

1. Open the project in VS Code:
   ```bash
   code .
   ```

2. Press `F5` to launch the Extension Development Host

3. In the new VS Code window, open the Command Palette (`Cmd+Shift+P` on Mac)

4. Type "Architector" and you should see:
   - `Architector: Generate Architecture Documentation`
   - `Architector: Start Backend Server`
   - `Architector: Stop Backend Server`

### Test 3: LLM API Connection

Create a test script to verify DeepSeek API:

```bash
cd backend
python3 -c "
from src.llm.client import LLMClient
client = LLMClient()
if client.test_connection():
    print('✓ LLM API connection successful')
else:
    print('✗ LLM API connection failed')
"
```

## Development Workflow

### Running in Development Mode

1. **Terminal 1 - Backend Server:**
   ```bash
   npm run start-backend
   ```

2. **Terminal 2 - TypeScript Watch Mode:**
   ```bash
   npm run watch
   ```

3. **VS Code - Extension Development:**
   - Press `F5` to launch Extension Development Host
   - Make changes to code
   - Press `Cmd+R` in Extension Development Host to reload

### Project Structure

```
Architector LLM/
├── .env                      # Environment variables (DO NOT COMMIT)
├── .gitignore               # Git ignore patterns
├── package.json             # Frontend dependencies
├── tsconfig.json            # TypeScript configuration
├── README.md                # Project overview
│
├── src/                     # Frontend (VS Code Extension)
│   ├── extension.ts         # Main entry point
│   ├── commands.ts          # Command implementations
│   └── config.ts            # Configuration management
│
├── backend/                 # Backend (Python)
│   ├── requirements.txt     # Python dependencies
│   ├── setup.py            # Package configuration
│   └── src/
│       ├── main.py         # HTTP server
│       ├── parser/         # Code analysis
│       ├── llm/            # LLM integration
│       ├── diagram/        # Diagram rendering
│       └── output/         # Output organization
│
└── docs/                   # Documentation
    ├── SETUP.md           # This file
    ├── USAGE.md           # Usage guide
    ├── ARCHITECTURE.md    # Technical architecture
    └── DEVELOPMENT.md     # Development guide
```

## Troubleshooting

### Backend Won't Start

**Problem:** Port 8765 already in use
```
Error: Address already in use
```

**Solution:** Kill the process using that port:
```bash
lsof -ti:8765 | xargs kill -9
```

Or change the port in `.env`:
```bash
BACKEND_PORT=8766
```

### TypeScript Compilation Errors

**Problem:** Cannot find module errors

**Solution:** Reinstall dependencies:
```bash
rm -rf node_modules
npm install
```

### LLM API Errors

**Problem:** API authentication failed

**Solution:** 
1. Verify your API key in `.env`
2. Check if the API key is valid and has sufficient credits
3. Test with curl:
   ```bash
   curl -X POST https://api.deepseek.com/v1/chat/completions \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"model":"deepseek-coder","messages":[{"role":"user","content":"test"}]}'
   ```

### Python Import Errors

**Problem:** `ModuleNotFoundError: No module named 'flask'`

**Solution:** Ensure you're in the backend directory:
```bash
cd backend
pip3 install -r requirements.txt
```

## Next Steps

Once setup is complete:
1. Read [USAGE.md](USAGE.md) to learn how to use the extension
2. Read [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system design
3. Read [DEVELOPMENT.md](DEVELOPMENT.md) to start contributing

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the [Development Guide](DEVELOPMENT.md)
3. Check the logs in VS Code Output panel (View → Output → Architector-LLM)
