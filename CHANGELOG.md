# Changelog

All notable changes to the **Architector-LLM** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.1.0] - 2026-01-24

### Added
- **Multi-Diagram Architecture Synthesis:** Automated generation of 6 distinct architectural views:
  - System Component Diagram
  - Class Diagram (OOP structure and relationships)
  - Activity Diagram (Business logic and execution workflows)
  - Data Flow Diagram (Information transformations across boundaries)
  - C4 System Context Diagram (High-level system ecosystem boundaries)
  - Sequence Diagram (Inter-object communication protocols)
- **Diagram Quality Validation Engine:**
  - Automated 4-dimension scoring system: Syntax (100-pt scale), Completeness, Clarity, and Accuracy.
  - Quality threshold validation and recommendation generation.
  - Markdown-based quality report generation (`QUALITY_REPORT.md`).
- **Cross-Diagram Relationship Mapper:**
  - Discovers shared entities across generated views.
  - Builds unified entity mapping (`RELATIONSHIPS.md`) connecting component nodes with class and sequence actors.
- **Interactive Documentation Generator:**
  - Auto-generated `INDEX.md` with cross-references, navigation links, and diagram previews.
  - `COMPARISONS.md` for architectural delta tracking between git commits/versions.
- **Empirical Evaluation Benchmark Suite:**
  - Validated on 9 diverse real-world open-source repositories across Python, JavaScript, TypeScript, and PHP (599 to 112,000+ LOC).
  - 94.7% diagram synthesis success rate with average speed of 284 LOC/second.

---

## [2.0.9] - 2026-01-24

### Fixed
- **Tree-Sitter Dependency Alignment Hotfix:**
  - Upgraded core `tree-sitter` runtime from 0.22.3 to 0.23.2.
  - Pinned all 11 language grammar modules (`tree-sitter-python`, `tree-sitter-javascript`, `tree-sitter-typescript`, `tree-sitter-php`, `tree-sitter-java`, `tree-sitter-c`, `tree-sitter-cpp`, `tree-sitter-c-sharp`, `tree-sitter-go`, `tree-sitter-rust`, `tree-sitter-ruby`) to compatible 0.23.x versions.
  - Updated AST parser language initialization to properly handle `PyCapsule` wrapping in tree-sitter 0.23.x API.

---

## [2.0.8] - 2026-01-23

### Added
- Automated Ollama local daemon detection on port 11434 with model availability inspection.
- Extension Setup Wizard with one-click verification and provider switching.
- Secure API key storage leveraging VS Code `SecretStorage` API for cloud providers (DeepSeek, OpenAI, Anthropic Claude).

---

## [2.0.5] - 2026-01-23

### Added
- Webview-based progress panel displaying real-time pipeline execution stages.
- Status bar notification states (`$(gear) Setup`, `$(book) Architector`, `$(sync~spin) Generating`).
- Research Demographics & Consent Wizard for voluntary empirical study participation.

---

## [2.0.3] - 2026-01-22

### Added
- Initial VS Code Extension packaging.
- Multi-provider LLM client supporting local Ollama (`deepseek-coder:6.7b`) and Cloud APIs.
- Tree-sitter AST extraction pipeline with dependency graph builder.
- Output directory organization: `docs/arch/v{version}_{timestamp}_{githash}/`.

---

## [1.0.0] - 2026-01-20

### Added
- Initial proof-of-concept Python CLI for AST extraction and single architecture diagram generation.
- Research prototype for NUST publication: *"From Code to Architecture: Leveraging LLMs for Automated Software Design Documentation"*.
