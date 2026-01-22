# Research & Development Implementation Plan: Architector-LLM Prototype

## 1. Project Overview and Goal

**Project Name:** Architector-LLM
**Goal:** To develop a functional, open-source IDE plugin (targeting VS Code/GitHub Codespaces compatibility) that automates the generation of professional, versioned software architecture documentation and multi-level diagrams directly from a codebase using a lightweight Large Language Model (LLM).
**Target Audience:** Software Architects, Senior Developers, and Researchers.
**Implementation Agent:** Google's Antigravity IDE with Gemini Pro 3 Coding Agent.

## 2. Core Requirements (Functional & Non-Functional)

### 2.1. Functional Requirements (FR)
| ID | Requirement | Description |
| :--- | :--- | :--- |
| FR-01 | **Codebase Ingestion** | The plugin MUST be able to scan and parse an entire codebase (multi-language support: Python, JavaScript/TypeScript). |
| FR-02 | **Dependency Graph Extraction** | The plugin MUST extract key architectural metadata, including class definitions, function signatures, and a full dependency graph (Abstract Syntax Tree/AST-based). |
| FR-03 | **LLM Interface** | The plugin MUST securely interface with a lightweight, open-source LLM (e.g., DeepSeek Coder, Code Llama) via a dedicated API endpoint. |
| FR-04 | **Prompt Curation (RAG)** | The plugin MUST construct a structured prompt by injecting the extracted code metadata (FR-02) into a fixed System Prompt, following Retrieval-Augmented Generation (RAG) principles. |
| FR-05 | **Documentation Generation** | The LLM MUST generate the final documentation content in structured Markdown format. |
| FR-06 | **Diagram Generation** | The LLM MUST generate the source code for architectural diagrams (C4 Model, UML) using text-based tools (PlantUML or Mermaid syntax). |
| FR-07 | **Diagram Rendering** | The plugin MUST render the generated diagram source code (FR-06) into visual assets (PNG/SVG). |
| FR-08 | **Output Organization** | The plugin MUST save all generated artifacts (Markdown, Diagram Source, Visual Assets) into a dedicated, versioned folder (e.g., `docs/arch/vX.Y.Z/`). |
| FR-09 | **IDE Integration** | The plugin MUST provide a simple user interface (e.g., a single button or command palette entry) to trigger the documentation generation process. |

### 2.2. Non-Functional Requirements (NFR)
| ID | Requirement | Description |
| :--- | :--- | :--- |
| NFR-01 | **Performance** | The end-to-end generation process MUST complete within a reasonable time limit (Target: < 5 minutes for a medium-sized repository). |
| NFR-02 | **Reproducibility** | The entire toolchain, including the LLM and prompting strategy, MUST be open-source or easily reproducible for research validation. |
| NFR-03 | **Maintainability** | The codebase MUST be modular, clearly separating the IDE-specific frontend logic from the core Python-based LLM/analysis backend. |
| NFR-04 | **Security** | The plugin MUST NOT transmit sensitive code content to the LLM without explicit user consent. All LLM calls should be secured via API keys. |

## 3. Technical Architecture Blueprint

The architecture follows a **Hybrid Frontend-Backend Model** to leverage the strengths of both the IDE environment (TypeScript/JavaScript) and the data science ecosystem (Python).

### 3.1. Technical Stack
| Component | Technology | Rationale |
| :--- | :--- | :--- |
| **Frontend (IDE Plugin)** | TypeScript/JavaScript (Node.js) | Native language for VS Code/GitHub Codespaces extensions. Handles UI, file system access, and communication with the backend. |
| **Backend (Core Logic)** | Python | Superior ecosystem for AST parsing (`ast`, `tree-sitter`), dependency analysis, and LLM API interaction (`requests`, `langchain` or custom API client). |
| **LLM** | DeepSeek Coder / Code Llama | Lightweight, open-source, and specialized in code. Will be hosted locally or via a dedicated, private endpoint for the prototype. |
| **Diagramming** | PlantUML / Mermaid | Text-based diagramming for LLM output. Python libraries (e.g., `plantuml` wrapper) will handle rendering. |

### 3.2. Architectural Diagram (Conceptual Flow)

The flow is a direct implementation of the five-stage pipeline:

1.  **User Action:** Developer clicks "Generate Documentation" in the IDE.
2.  **Frontend (TS/JS):** Plugin identifies the codebase root and sends a request to the Python Backend.
3.  **Backend (Python - Stage 1):** Uses AST parsing (e.g., `tree-sitter`) to analyze code, extract metadata, and build a structured dependency graph (RAG Context).
4.  **Backend (Python - Stage 2/3):** Curates the prompt (System Prompt + RAG Context) and sends it to the LLM API.
5.  **LLM API:** Processes the prompt and returns two outputs: Structured Markdown Text and Diagram Source Code (PlantUML/Mermaid).
6.  **Backend (Python - Stage 4):** Renders the Diagram Source Code into PNG/SVG visual assets.
7.  **Backend (Python - Stage 5):** Organizes all artifacts into a versioned folder and signals completion to the Frontend.
8.  **Frontend (TS/JS):** Displays a success notification and opens the generated documentation folder.

## 4. Research & Development Phased Plan

The prototype development will be executed in four distinct phases, each with clear deliverables and testing milestones.

### Phase 1: Foundation and Code Analysis (MVP - Minimum Viable Parser)

| Milestone | Deliverable | Testing & Validation |
| :--- | :--- | :--- |
| **1.1** | **Project Setup** | Initialize the hybrid TypeScript/Python project structure. Define communication channel (e.g., simple HTTP server or IPC) between frontend and backend. | Unit tests for IPC/HTTP communication. |
| **1.2** | **Basic Code Parser** | Implement a Python-based parser (using `tree-sitter` or similar) for a single language (e.g., Python). Must extract class names and function signatures. | Unit tests against small, controlled code snippets to verify correct extraction of all classes/functions. |
| **1.3** | **Dependency Graph** | Implement logic to trace imports/calls and generate a basic, structured dependency graph (JSON format). | Integration tests against a small, multi-file repository to verify the graph accurately reflects dependencies. |
| **1.4** | **IDE Integration** | Create the basic VS Code extension with a single command that successfully calls the Python backend and receives a simple "Hello World" response. | Manual test in VS Code: Click button, see "Hello World" notification. |

### Phase 2: LLM Integration and Prompt Engineering (MVP - Minimum Viable Documentation)

| Milestone | Deliverable | Testing & Validation |
| :--- | :--- | :--- |
| **2.1** | **LLM API Client** | Implement a secure Python client to connect to the chosen LLM (Gemini Pro 3 API endpoint). | Unit tests for API connectivity and latency. |
| **2.2** | **Prompt Curator** | Implement the logic to construct the RAG prompt: Inject the JSON dependency graph (from Phase 1) into the System Prompt. | Unit tests to verify the final prompt structure and token count are within limits. |
| **2.3** | **Raw Generation** | Execute the first end-to-end run: Parser -> Prompt -> LLM -> Raw Markdown/Diagram Text Output. | Manual test: Verify the LLM output contains both Markdown and PlantUML/Mermaid syntax. |
| **2.4** | **Diagram Rendering** | Implement the Python logic to take the PlantUML/Mermaid text and render it to a PNG/SVG file. | Unit tests for the rendering function against known-good diagram source code. |

### Phase 3: Output Structuring and Versioning (Prototype Completion)

| Milestone | Deliverable | Testing & Validation |
| :--- | :--- | :--- |
| **3.1** | **Output Organizer** | Implement the final stage: Create the versioned output folder (`docs/arch/vX.Y.Z/`) and save all artifacts (Markdown, Diagram Source, Visual Assets). | Integration tests: Run against a test repo, verify all files are created in the correct, versioned directory. |
| **3.2** | **Git Integration** | Implement logic to read the current Git commit hash and use it for versioning (FR-08). | Unit tests to ensure the correct commit hash is read and included in the output path/metadata. |
| **3.3** | **User Experience Refinement** | Improve the IDE UI: Add progress bar/status updates during the long-running LLM process. | Manual test: Verify smooth UX and clear status messages. |
| **3.4** | **Multi-Language Support (Initial)** | Extend the parser (1.2) to support a second language (e.g., JavaScript). | Unit tests against a small, polyglot repository. |

### Phase 4: Research Validation and Documentation

| Milestone | Deliverable | Testing & Validation |
| :--- | :--- | :--- |
| **4.1** | **Prototype Documentation** | Generate comprehensive documentation for the prototype, including installation guide, usage instructions, and API reference. | Review documentation for clarity and completeness. |
| **4.2** | **Empirical Case Study** | Execute the first case study against a small, real-world open-source repository (e.g., a small Flask app). | Measure $T_{LLM}$ and perform a preliminary qualitative review of $C_{Arch}$ against the ground truth. |
| **4.3** | **Threats to Validity Mitigation** | Implement logging and configuration options to ensure the LLM's prompt and context are fully auditable and reproducible (NFR-02). | Review logs to ensure all RAG context is recorded for each generation run. |
| **4.4** | **Final Prototype Release** | Tag the first official prototype release (v1.0.0). | End-to-end test on a clean machine. |

## 5. Testing and Quality Assurance Strategy

The strategy is centered on **Reproducibility** and **Architectural Fidelity**.

| Test Type | Focus | Tooling/Method |
| :--- | :--- | :--- |
| **Unit Tests** | Individual components (Parser functions, API client, Renderer). | Standard Python/TypeScript unit testing frameworks. |
| **Integration Tests** | Communication between Frontend/Backend and the full Parser -> LLM pipeline. | Test harnesses that simulate the IDE environment and mock the LLM API response. |
| **Fidelity Tests** | Quality of the generated output. | **Ground Truth Comparison:** Automated comparison of generated dependency graphs (JSON) against a manually verified ground truth graph. |
| **Empirical Validation** | Performance and Accuracy. | **Case Study Execution:** Running the tool against selected open-source repositories and measuring the metrics defined in the research paper ($T_{LLM}$, $C_{Arch}$, $F_{Diag}$). |

## 6. Key Research Considerations for the Coding Agent

The coding agent MUST prioritize the following research-driven aspects:

1.  **RAG Implementation:** The core novelty lies in the structured prompt. The agent must ensure the extracted code context is injected *before* the LLM's instruction, minimizing the chance of the LLM ignoring the context.
2.  **LLM Selection:** The agent should confirm the chosen LLM (DeepSeek/Code Llama) is indeed the most performant lightweight model for this specific task (architectural reasoning, not just code generation).
3.  **Reproducibility:** All LLM parameters (temperature, top\_p, seed) MUST be configurable and logged for every run to ensure the research is reproducible (NFR-02).
4.  **Diagram Fidelity:** The agent should focus on generating clean, syntactically correct PlantUML/Mermaid code, as this is the most direct measure of the LLM's architectural understanding.

This plan provides a detailed roadmap for the Gemini Pro 3 Coding Agent to successfully implement the Architector-LLM prototype.
