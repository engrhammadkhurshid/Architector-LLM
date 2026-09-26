# Architecture Overview: Architector-LLM

**Research Publication:** *"From Code to Architecture: Leveraging LLMs for Automated Software Design Documentation"*  
**Author:** Engr. Hammad Khurshid  
**Institution:** National University of Sciences and Technology (NUST), Pakistan  
**System Version:** v2.1.0

---

## 1. System Philosophy & High-Level Architecture

Architector-LLM employs a **Hybrid Client-Engine Architecture**:
1. **Frontend (VS Code Extension):** Implemented in TypeScript, integrating deeply with VS Code APIs (`vscode.window`, `vscode.commands`, `SecretStorage`, Webviews, and StatusBar).
2. **Core Pipeline Engine (Python):** Robust, high-performance AST parsing with Tree-sitter (11 languages), codebase metric profiling, rule/LLM-based architectural view selection, prompt curation, multi-model generation, 4-dimension quality validation, cross-diagram relationship mapping, and interactive documentation generation.
3. **Analytics & Empirical Research Backend:** A lightweight, GDPR-compliant Flask service for optional participant registration, telemetry tracking, and empirical evaluation data export.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    VS Code IDE Frontend (TypeScript)                         │
│  ┌─────────────────┐  ┌───────────────────┐  ┌───────────────────────────┐  │
│  │  Setup Wizard   │  │  API Key Manager  │  │  Webview Progress Panel   │  │
│  └─────────────────┘  └───────────────────┘  └───────────────────────────┘  │
│  ┌─────────────────┐  ┌───────────────────┐  ┌───────────────────────────┐  │
│  │ Dependency Check│  │ Status Bar Item   │  │ Voluntary Telemetry Mgr   │  │
│  └─────────────────┘  └───────────────────┘  └───────────────────────────┘  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Subprocess / CLI (`architector.py`)
                                       │ or REST API (`main.py:8765`)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│               Python Core Backend Engine (`backend/src/`)                   │
│                                                                             │
│  1. Codebase Parsing & Graph Construction                                    │
│     ├── Tree-sitter AST Parser (Python, JS, TS, PHP, Java, C, C++, C#, ...) │
│     └── Dependency Graph Builder (Nodes, Edges, Import Flow)                │
│                                                                             │
│  2. Codebase Profiling & View Selection                                     │
│     ├── Codebase Analyzer (Language, Paradigm, Architecture Patterns)       │
│     └── Diagram Selector (Heuristic Prioritization: High / Medium / Low)    │
│                                                                             │
│  3. Multi-View Context Extraction & LLM Prompt Curators                     │
│     ├── Specialized Context Extractors (Component, Class, Activity, C4, ...)│
│     └── Multi-Provider LLM Client (Local Ollama, DeepSeek, OpenAI, Claude)  │
│                                                                             │
│  4. Quality Validation & Synthesis                                          │
│     ├── Diagram Validator (Syntax, Completeness, Clarity, Accuracy)         │
│     ├── Relationship Mapper (Cross-diagram entity correlation)              │
│     └── Interactive Doc Generator (README.md, INDEX.md, RELATIONSHIPS.md)   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
           Output: `docs/arch/v{version}_{timestamp}_{githash}/`
```

---

## 2. Component Directory Structure

```
Architector-LLM/
├── vscode-extension/src/         # VS Code Extension (TypeScript)
│   ├── extension.ts              # Extension activation and command router
│   ├── setupWizard.ts            # First-run guided configuration
│   ├── dependencyChecker.ts      # Python, Ollama, and model diagnostics
│   ├── pythonRunner.ts           # Subprocess pipeline execution
│   ├── progressPanel.ts          # Interactive webview progress UI
│   ├── apiKeyManager.ts          # Secure VS Code SecretStorage client
│   └── analytics/                # Empirical research data manager
│       ├── developerInfo.ts      # Participant demographics modal
│       └── telemetry.ts          # GDPR-compliant session logging
├── backend/src/                  # Core Python Pipeline
│   ├── pipeline.py               # DocumentationPipeline master orchestrator
│   ├── main.py                   # Optional Flask HTTP service
│   ├── parser/                   # AST & graph extraction
│   │   ├── ast_parser.py         # Multi-language Tree-sitter AST parser
│   │   └── dependency_graph.py   # Codebase graph builder
│   ├── analyzer/                 # Project characterization
│   │   ├── codebase_analyzer.py  # Language, pattern, and complexity profiler
│   │   └── version_detector.py   # Semver extraction from git/manifests
│   ├── diagram/                  # Multi-diagram generation
│   │   ├── diagram_types.py      # Diagram registry and taxonomies
│   │   ├── diagram_selector.py   # Rule-based and priority selector
│   │   ├── context_extractors.py # Specialized AST context filters
│   │   ├── multi_diagram_generator.py # Parallel diagram synthesis
│   │   └── relationship_mapper.py # Entity tracking across diagrams
│   ├── llm/                      # Model integration
│   │   ├── client.py             # OllamaClient & LLMClient (DeepSeek, OpenAI)
│   │   └── prompts/              # Architecture-specific prompt templates
│   ├── validation/               # Quality evaluation
│   │   ├── diagram_validator.py  # 4-dimension scoring engine
│   │   └── quality_report.py     # Markdown report generator
│   └── output/                   # Deliverables generation
│       ├── interactive_docs.py   # INDEX.md and COMPARISONS.md generator
│       ├── organizer.py          # Directory layout manager
│       └── renderer.py           # Mermaid SVG/PNG rendering
├── tests/                        # Comprehensive test suite
│   ├── test_parser.py            # AST parsing and graph unit tests
│   ├── test_setup.py             # Environment verification
│   ├── test_analyzer.py          # Profiler and selector tests
│   ├── test_prompts.py           # Prompt and context extraction tests
│   ├── test_validation.py        # Quality validation tests
│   ├── test_relationships.py     # Relationship mapping tests
│   ├── test_pipeline.py          # End-to-end pipeline test on test-repo
│   └── test_flask_app.py         # End-to-end test on real web app
├── deploy/                       # Cloud deployment configs for telemetry
├── docs/                         # Comprehensive documentation
├── architector.py                # Standalone CLI entrypoint
└── analytics_backend.py          # Telemetry and participant registration server
```

---

## 3. Detailed Component Deep-Dive

### 3.1. Abstract Syntax Tree (AST) Parsing & Dependency Graph
- **Library:** `tree-sitter==0.23.2` with dedicated grammars for Python, JavaScript, TypeScript, PHP, Java, C, C++, C#, Go, Rust, and Ruby.
- **Parsing Pass:** Traverses source code trees to extract class definitions, methods, signatures, standalone functions, module imports, and inheritance hierarchies.
- **Graph Builder:** Generates a directed graph representing files, entities, and import dependencies.

### 3.2. Codebase Analyzer & Diagram Selector
- **Profiling:** Analyzes primary language, paradigms (OOP, functional, procedural), detected frameworks (e.g. Django, Flask, Express, NestJS, Laravel), API endpoints, database models, and codebase scale (tiny, small, medium, large).
- **Selection Engine:** Evaluates which diagrams will yield the highest informational value for the specific project profile. For example, a pure CLI tool prioritizes Component, Class, and Activity workflows, whereas an enterprise web API prioritizes C4 System Context and Data Flow.

### 3.3. Multi-Provider LLM Integration
- **Local (Privacy-Preserving):** Automated detection of local Ollama instances (`http://localhost:11434`) running `deepseek-coder:6.7b`. No code leaves the developer's workstation.
- **Cloud Providers:** DeepSeek API, OpenAI GPT-4, Anthropic Claude via encrypted `SecretStorage`.

### 3.4. Multi-Diagram Synthesis Taxonomy
The system synthesizes 6 standardized views:
1. **Component Diagram:** High-level modular decomposition and external dependencies.
2. **Class Diagram:** OOP class hierarchy, attributes, methods, and visibility.
3. **Sequence Diagram:** Inter-object temporal message flows and method invocation sequences.
4. **Activity Diagram:** Business logic execution workflows and branching decision trees.
5. **Data Flow Diagram (DFD):** Input sources, transformations, and persistence sinks.
6. **C4 System Context Diagram:** Enterprise boundary, user personas, and external system integrations.

### 3.5. Quality Validation Engine
Automated 4-dimension scoring validates each generated Mermaid diagram:
- **Syntax (100-pt scale):** Validates Mermaid grammatical syntax, keywords, and delimiters.
- **Completeness:** Verifies that major components, classes, and interactions identified in AST analysis are depicted.
- **Clarity:** Evaluates diagram density, connection clarity, and absence of visual spaghetti.
- **Accuracy:** Assesses structural fidelity against the parsed dependency graph.

---

## 4. Documentation Output Layout

Every generation run produces an immutable, versioned documentation package:

```
docs/arch/v{version}_{timestamp}_{githash}/
├── README.md               # Executive architecture summary
├── INDEX.md                # Interactive cross-referenced navigation index
├── RELATIONSHIPS.md        # Cross-diagram entity mapping and coverage analysis
├── QUALITY_REPORT.md      # Automated quality scores and recommendations
├── COMPARISONS.md         # Architectural delta against prior runs
├── diagrams/
│   ├── component.mmd / .svg / .png
│   ├── class.mmd / .svg / .png
│   ├── sequence.mmd / .svg / .png
│   ├── activity.mmd / .svg / .png
│   ├── data_flow.mmd / .svg / .png
│   └── c4_context.mmd / .svg / .png
└── metadata/
    └── generation_info.json # Timing, token usage, model, and git metadata
```
