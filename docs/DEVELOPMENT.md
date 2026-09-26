# Developer & Contributor Guide: Architector-LLM

This guide provides instructions for developers contributing to or extending **Architector-LLM**.

---

## 1. Development Environment Setup

### Prerequisites
- **Node.js:** v18.x or v20.x
- **npm:** v9.x or higher
- **Python:** 3.9+ (Python 3.10+ recommended)
- **VS Code:** 1.85.0 or higher
- **Git**
- *(Optional)* **Ollama:** with `deepseek-coder:6.7b` for local testing

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/engrhammadkhurshid/Architector-LLM.git
cd Architector-LLM

# Install TypeScript / Extension dependencies
npm install

# Setup Python virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python backend dependencies
pip install -r requirements.txt
```

---

## 2. Project Architecture & Codebase Map

### Extension Layer (`vscode-extension/src/`)
- `extension.ts`: Activation lifecycle, status bar management, and VS Code command dispatching.
- `setupWizard.ts`: Interactive initial configuration wizard (Ollama auto-detection, cloud API key prompts).
- `dependencyChecker.ts`: Verifies Python runtime, Tree-sitter packages, and Ollama status.
- `pythonRunner.ts`: Executes the core Python documentation generator as a background child process.
- `progressPanel.ts`: Webview panel reporting real-time pipeline milestones.
- `apiKeyManager.ts`: Manages provider API keys securely using VS Code `SecretStorage`.
- `analytics/`: GDPR-compliant opt-in research demographic tracking.

### Core Engine Layer (`backend/src/`)
- `pipeline.py`: Master orchestrator coordinating parsing, profiling, selection, synthesis, validation, and layout.
- `parser/ast_parser.py`: Multi-language Tree-sitter AST parser (11 languages supported).
- `parser/dependency_graph.py`: Entity and dependency graph constructor.
- `analyzer/codebase_analyzer.py`: Codebase profiler (languages, OOP/functional, frameworks, scale).
- `analyzer/version_detector.py`: Git and manifest semantic version detector.
- `diagram/diagram_types.py`: Registry defining the 6 architectural diagram categories and scoring criteria.
- `diagram/diagram_selector.py`: Rule-based priority selector choosing the best views for a codebase.
- `diagram/context_extractors.py`: AST contextual filtering specialized per diagram type.
- `diagram/multi_diagram_generator.py`: Multi-threaded parallel LLM synthesis.
- `diagram/relationship_mapper.py`: Correlates entities across generated views.
- `validation/diagram_validator.py`: 4-dimension scoring engine (Syntax, Completeness, Clarity, Accuracy).
- `validation/quality_report.py`: Generates `QUALITY_REPORT.md`.
- `output/interactive_docs.py`: Synthesizes `INDEX.md`, `RELATIONSHIPS.md`, and `COMPARISONS.md`.
- `main.py`: Optional Flask HTTP server exposing `/health` and `/generate`.

### CLI Tool (`architector.py`)
- Independent Python CLI entrypoint to document any codebase from the terminal without VS Code.

### Test Suite (`tests/`)
- `test_parser.py`: Unit tests for AST parsing and graph extraction.
- `test_setup.py`: Environment and dependency diagnostic test.
- `test_analyzer.py`: Profiler and diagram selector integration tests.
- `test_prompts.py`: Context extraction and prompt generation validation.
- `test_validation.py`: Quality validation engine tests.
- `test_relationships.py`: Entity relationship mapping tests.
- `test_pipeline.py`: End-to-end pipeline execution on `test-repo`.
- `test_flask_app.py`: Real-world web application documentation test on `test-flask-app`.

---

## 3. Development Commands

### Extension Tasks (Node / TypeScript)

```bash
# Build development bundle
npm run compile

# Watch mode for iterative development
npm run watch

# Lint TypeScript code
npm run lint

# Automatically fix lint issues
npm run lint -- --fix

# Build optimized production bundle
npm run package-extension
```

### Backend Tasks (Python)

```bash
# Verify Python environment & dependencies
python3 tests/test_setup.py

# Run all automated unit and integration tests
python3 -m unittest discover tests

# Run specific integration tests
python3 tests/test_analyzer.py
python3 tests/test_prompts.py
python3 tests/test_validation.py
python3 tests/test_relationships.py

# Test CLI pipeline on sample repo
python3 architector.py test-repo 1.0.0

# Start optional Flask backend daemon
python3 backend/src/main.py
```

---

## 4. Debugging in VS Code

1. Open this repository in VS Code.
2. Open the Run & Debug view (`Ctrl+Shift+D` / `Cmd+Shift+D`).
3. Press **F5** to launch the **Extension Development Host**.
4. In the newly opened VS Code window, open any codebase and run:
   - Command Palette: `Architector: Run Setup Wizard` or `Architector: Generate Architecture Documentation`.
5. Breakpoints set in `vscode-extension/src/*.ts` will hit in the primary window.

---

## 5. Adding Support for a New Language

1. Add the corresponding `tree-sitter-<language>` package to `requirements.txt` and `backend/requirements.txt`.
2. Register the language grammar and file extensions in `backend/src/parser/ast_parser.py`:
   - Add file extension mapping in `_detect_language()`.
   - Implement node traversal in `_extract_entities_from_ast()`.
3. Add a unit test verifying parsing of a sample file in `tests/test_parser.py`.
4. Update `docs/SUPPORTED_LANGUAGES.md`.

---

## 6. Contribution Workflow

1. Fork the repository on GitHub (`https://github.com/engrhammadkhurshid/Architector-LLM`).
2. Create a topical feature branch: `git checkout -b feature/your-feature-name`.
3. Implement changes and write appropriate unit or integration tests in `tests/`.
4. Ensure all checks pass:
   ```bash
   npm run compile && npm run lint && python3 -m unittest discover tests
   ```
5. Commit your changes using conventional commits (`git commit -m "feat: describe change"`).
6. Push to your fork and submit a Pull Request.
