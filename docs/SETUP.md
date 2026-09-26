# Setup & Installation Guide: Architector-LLM

This guide provides instructions for setting up **Architector-LLM** for local use, extension development, or CLI execution.

---

## 1. System Requirements

| Component | Minimum Requirement | Recommended |
|-----------|---------------------|-------------|
| **OS** | Windows 10+, macOS 11+, or Linux | Any modern 64-bit OS |
| **Python** | Python 3.9+ | Python 3.10 or 3.11 |
| **Node.js** | Node.js v18.x | Node.js v20.x |
| **VS Code** | v1.85.0+ | Latest Stable |
| **RAM** | 8 GB | 16 GB+ (if running Ollama locally) |

---

## 2. Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/engrhammadkhurshid/Architector-LLM.git
cd Architector-LLM
```

### Step 2: Install Node & Extension Dependencies

```bash
npm install
npm run compile
```

### Step 3: Install Python Backend Engine Dependencies

```bash
# Create and activate virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install all backend and tree-sitter language parsers
pip install -r requirements.txt
```

---

## 3. Configuring LLM Providers

Architector-LLM supports both local privacy-preserving LLMs and high-performance cloud LLMs.

### Option A: Local LLM with Ollama (Free & 100% Private)

Running locally guarantees zero code leaves your machine.

1. **Install Ollama:**
   - Download from: [https://ollama.ai](https://ollama.ai)
2. **Pull the recommended coding model:**
   ```bash
   ollama pull deepseek-coder:6.7b
   ```
3. **Verify Ollama is running:**
   ```bash
   curl http://localhost:11434/api/tags
   ```
4. Architector-LLM will automatically detect your local Ollama instance on port 11434.

### Option B: Cloud Providers (DeepSeek / OpenAI / Claude)

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` with your preferred API provider:

```bash
# DeepSeek API (Fast and highly cost-effective)
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Or OpenAI
# LLM_PROVIDER=openai
# OPENAI_API_KEY=your_openai_api_key_here

# Or Anthropic Claude
# LLM_PROVIDER=claude
# CLAUDE_API_KEY=your_claude_api_key_here
```

When using the VS Code extension, you can also securely input your API key via the **Setup Wizard**, which stores it in VS Code's encrypted `SecretStorage`.

---

## 4. Verification

Verify that your environment, parsers, and dependencies are properly configured:

```bash
python3 tests/test_setup.py
```

Expected output:
```text
Testing backend setup...
Python version: 3.x.x
✓ Parser imported successfully
✓ LLM Client imported successfully
✓ Diagram Renderer imported successfully
✓ Output Organizer imported successfully
✓ Codebase Analyzer imported successfully
✓ Diagram Validator imported successfully
✓ Pipeline imported successfully
✅ Backend setup test complete!
```

---

## 5. Running Architector-LLM

### Method 1: Using the Standalone CLI

Generate architecture documentation directly from your terminal:

```bash
# Basic usage (auto-detects version from project files or git)
python3 architector.py /path/to/your/codebase

# Explicit version tag
python3 architector.py /path/to/your/codebase 2.0.0

# Example on included test repository:
python3 architector.py test-repo 1.0.0
```

### Method 2: In VS Code (Extension Mode)

1. Open the repository in VS Code.
2. Press **F5** to start the Extension Development Host.
3. In the new window, open any codebase workspace.
4. Click **`$(book) Architector`** in the bottom-right status bar, or run:
   - Command: `Architector: Generate Architecture Documentation`
5. The extension will automatically analyze the workspace, synthesize the 6 architecture diagrams, and generate an interactive documentation suite under `docs/arch/`.
