# User Guide: Architector-LLM

This guide explains how to generate comprehensive software architecture documentation using **Architector-LLM**, both via the **VS Code Extension** and the **Standalone CLI**.

---

## 1. Using the VS Code Extension

### 1.1 First-Time Setup Wizard

When you first activate the extension, the **Setup Wizard** appears automatically to ensure everything is ready:
1. **Dependency Verification:** Automatically verifies Python 3.9+ and Tree-sitter parsers.
2. **LLM Provider Detection:**
   - Detects local **Ollama** instances on `http://localhost:11434`.
   - Offers seamless configuration for **DeepSeek**, **OpenAI GPT-4**, or **Anthropic Claude**.
3. **Secure API Key Management:** If using a cloud provider, your API key is encrypted using VS Code's native `SecretStorage`.
4. **Voluntary Research Consent:** Optional opt-in to anonymous metrics collection for the academic paper study.

You can relaunch the wizard at any time via:
- Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`): `Architector: Run Setup Wizard`

### 1.2 Generating Documentation

1. Open your project folder in VS Code (`File` → `Open Folder...`).
2. Click the status bar button in the bottom right corner:
   - **`$(book) Architector`**
   - Or open Command Palette and select: `Architector: Generate Architecture Documentation`.
3. The interactive **Progress Panel** webview opens, displaying real-time pipeline execution:
   - `[1/6]` Codebase AST parsing & symbol extraction
   - `[2/6]` Dependency graph construction
   - `[3/6]` Codebase profiling & architecture view prioritization
   - `[4/6]` Multi-diagram LLM generation (Component, Class, Activity, DFD, C4, Sequence)
   - `[5/6]` Diagram quality validation (Syntax, Completeness, Clarity, Accuracy)
   - `[6/6]` Cross-diagram relationship mapping & interactive HTML/Markdown layout
4. Once completed, VS Code will prompt you with options to:
   - **Open Documentation (`README.md`)**
   - **Reveal Output Directory**

---

## 2. Using the Standalone CLI

You can run Architector-LLM directly on any repository without launching VS Code:

```bash
# Basic syntax
python3 architector.py <codebase-path> [version]

# Examples:
python3 architector.py ~/projects/my-web-app
python3 architector.py ~/projects/my-web-app 2.0.0
python3 architector.py test-repo 1.0.0
```

### CLI Output Summary

Upon completion, the CLI prints an executive summary:

```text
================================================================================
✅ DOCUMENTATION GENERATED
================================================================================

📊 Metrics:
   Files: 42
   Classes: 18
   Functions: 84
   Diagrams: 6/6
   Quality: 88.4/100
   Time: 12.3s

📂 Output: docs/arch/v1.0.0_2026-01-24-184551_51589c50
Open with: open docs/arch/v1.0.0_2026-01-24-184551_51589c50/README.md
```

---

## 3. Generated Artifacts & Navigation

Every execution produces an organized package inside the project's `docs/arch/` directory:

```
docs/arch/v{version}_{timestamp}_{githash}/
├── README.md               # Main architecture documentation report
├── INDEX.md                # Interactive cross-referenced navigation index
├── RELATIONSHIPS.md        # Cross-diagram entity mapping and coverage analysis
├── QUALITY_REPORT.md      # Automated 4-dimension quality scoring report
├── COMPARISONS.md         # Architectural delta against prior version runs
├── diagrams/
│   ├── component.mmd / .svg / .png
│   ├── class.mmd / .svg / .png
│   ├── sequence.mmd / .svg / .png
│   ├── activity.mmd / .svg / .png
│   ├── data_flow.mmd / .svg / .png
│   └── c4_context.mmd / .svg / .png
└── metadata/
    └── generation_info.json # Run telemetry, model, timestamp, and metrics
```

### 3.1 Understanding the 6 Diagram Types

| Diagram | Purpose | Best Suited For |
|---------|---------|-----------------|
| **Component Diagram** | Shows structural modules and external integrations | All codebases |
| **Class Diagram** | Maps object-oriented classes, methods, and inheritance | OOP codebases |
| **Sequence Diagram** | Visualizes message passing and execution protocols | Complex service workflows |
| **Activity Diagram** | Flowchart of execution paths and decisions | Business logic & CLI flows |
| **Data Flow Diagram** | Shows sources, processing steps, and data sinks | Data pipelines & APIs |
| **C4 Context Diagram** | High-level system ecosystem and external actors | Microservices & web applications |

### 3.2 Quality Report (`QUALITY_REPORT.md`)
Architector-LLM automatically scores each generated diagram across four dimensions:
- **Syntax:** 0–100 score on Mermaid grammar conformity.
- **Completeness:** Percentage of critical AST nodes represented in the visual model.
- **Clarity:** Density and visual readability rating.
- **Accuracy:** Structural consistency against the static dependency graph.

---

## 4. Configuration Options

You can configure Architector-LLM in VS Code Settings (`settings.json`):

```json
{
  "architector.llmProvider": "ollama",
  "architector.ollamaUrl": "http://localhost:11434",
  "architector.ollamaModel": "deepseek-coder:6.7b",
  "architector.outputDirectory": "docs/arch"
}
```

Or via environment variables in `.env`:

```bash
LLM_PROVIDER=ollama
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=deepseek-coder:6.7b
OUTPUT_BASE_DIR=docs/arch
```
