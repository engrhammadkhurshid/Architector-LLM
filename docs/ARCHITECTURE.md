# Architecture Overview - Architector-LLM

This document describes the technical architecture of the Architector-LLM system.

## System Architecture

Architector-LLM follows a **Hybrid Frontend-Backend Architecture** to leverage both the VS Code extension ecosystem (TypeScript) and the data science/ML ecosystem (Python).

```
┌─────────────────────────────────────────────────────────────┐
│                      VS Code IDE                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         Architector-LLM Extension (TypeScript)         │ │
│  │                                                         │ │
│  │  ├─ Command Handler                                   │ │
│  │  ├─ Progress UI                                        │ │
│  │  └─ Configuration Manager                             │ │
│  └────────────────────────────────────────────────────────┘ │
│                          │ HTTP/REST                         │
└──────────────────────────┼───────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              Python Backend (Flask Server)                   │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Parser     │  │  LLM Client  │  │   Diagram    │     │
│  │              │  │              │  │   Renderer   │     │
│  │ Tree-sitter  │  │  DeepSeek    │  │   Mermaid    │     │
│  │  AST         │  │   API        │  │    CLI       │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│          │                 │                 │              │
│          └────────┬────────┴────────┬────────┘              │
│                   ▼                 ▼                        │
│          ┌──────────────┐  ┌──────────────┐                │
│          │  Dependency  │  │    Output    │                │
│          │    Graph     │  │  Organizer   │                │
│          │   Builder    │  │              │                │
│          └──────────────┘  └──────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

## Component Overview

### 1. Frontend Layer (VS Code Extension)

**Technology:** TypeScript, Node.js, VS Code Extension API

**Responsibilities:**
- User interface and command registration
- Workspace file system access
- Configuration management
- Backend process lifecycle management
- Progress reporting and notifications

**Key Files:**
- `src/extension.ts` - Entry point, activation/deactivation
- `src/commands.ts` - Command implementations
- `src/config.ts` - Configuration utilities

**Communication:**
- HTTP REST API calls to Python backend
- Uses Axios for HTTP requests
- Async/await pattern for non-blocking operations

### 2. Backend Layer (Python Service)

**Technology:** Python 3.9+, Flask, Tree-sitter

**Responsibilities:**
- HTTP API server
- Code parsing and analysis
- LLM API communication
- Diagram rendering
- Output organization

**Sub-components:**

#### 2.1. HTTP Server (`main.py`)

- Flask-based REST API
- CORS enabled for development
- Health check endpoint
- Async job processing (future)

**Endpoints:**
```
GET  /health              - Health check
POST /generate           - Generate documentation
GET  /status/:job_id     - Check generation status
```

#### 2.2. Parser Module (`parser/`)

**Purpose:** Extract architectural metadata from source code

**Components:**
- `ast_parser.py` - Tree-sitter based AST parsing
- `dependency_graph.py` - Build structured dependency graph

**Capabilities:**
- Multi-language support (Python, TypeScript/JavaScript)
- Extract classes, functions, imports
- Build complete dependency graph
- Ignore patterns (node_modules, __pycache__, etc.)

**Output Format:**
```json
{
  "nodes": [
    {"id": "file.py::ClassName", "type": "class", "name": "ClassName", "file": "file.py"}
  ],
  "edges": [
    {"from": "file.py", "to": "file.py::ClassName", "type": "contains"}
  ],
  "metadata": {
    "total_files": 42,
    "total_classes": 15,
    "total_functions": 87
  }
}
```

#### 2.3. LLM Module (`llm/`)

**Purpose:** Interface with DeepSeek API and curate prompts

**Components:**
- `client.py` - DeepSeek API client
- `prompt_curator.py` - RAG-based prompt construction

**Prompt Strategy:**

```python
System Prompt (Fixed)
    ↓
RAG Context (Injected)
    ↓
User Instructions
    ↓
LLM Response
```

**Key Features:**
- Secure API key management via environment variables
- Configurable LLM parameters (temperature, max_tokens)
- Structured prompt engineering
- Error handling and retry logic

#### 2.4. Diagram Module (`diagram/`)

**Purpose:** Render Mermaid diagrams to visual assets

**Components:**
- `renderer.py` - Mermaid CLI wrapper

**Capabilities:**
- Render .mmd files to PNG/SVG
- Extract Mermaid code from markdown
- Batch rendering for multiple diagrams
- Transparent background support

**Dependencies:**
- Requires @mermaid-js/mermaid-cli
- Falls back gracefully if not installed

#### 2.5. Output Module (`output/`)

**Purpose:** Organize generated artifacts in versioned directories

**Components:**
- `organizer.py` - Directory creation and file management

**Versioning Strategy:**
```
Format: v{semantic_version}_{timestamp}_{git_hash}
Example: v1.0.0_2026-01-21-143022_abc123f
```

**Directory Structure:**
```
docs/arch/v1.0.0_2026-01-21-143022_abc123f/
├── README.md                    # Main documentation
├── INDEX.md                     # Artifact index
├── diagrams/
│   ├── architecture.mmd        # Mermaid source
│   └── architecture.png        # Rendered image
└── metadata/
    └── generation_info.json    # Metrics and metadata
```

## Data Flow

### Complete Pipeline

```
1. USER ACTION
   └─ Click "Generate Documentation" in VS Code

2. FRONTEND (TypeScript)
   ├─ Validate workspace
   ├─ Get codebase path
   └─ POST /generate {codebase_path}

3. BACKEND: PARSING (Python)
   ├─ CodeParser.parse_directory()
   ├─ Extract classes, functions, imports
   └─ DependencyGraphBuilder.build_graph()

4. BACKEND: RAG PREPARATION
   ├─ PromptCurator.curate_prompt()
   ├─ Inject dependency graph into prompt
   └─ Combine with system instructions

5. BACKEND: LLM GENERATION
   ├─ LLMClient.generate()
   ├─ Send to DeepSeek API
   └─ Receive: Markdown + Mermaid code

6. BACKEND: RENDERING
   ├─ DiagramRenderer.render()
   └─ Convert .mmd → .png

7. BACKEND: ORGANIZATION
   ├─ OutputOrganizer.create_output_directory()
   ├─ Save documentation files
   ├─ Save diagram files
   └─ Save metadata

8. FRONTEND: COMPLETION
   ├─ Show success notification
   └─ Offer to open documentation
```

## Design Patterns

### 1. Modular Architecture

Each component is self-contained with clear interfaces:
- Parser doesn't know about LLM
- LLM doesn't know about Output
- Clean separation of concerns

### 2. Configuration Management

Centralized configuration via:
- `.env` file for secrets
- VS Code settings for user preferences
- Default values with override capability

### 3. Error Handling

Multi-level error handling:
- Frontend: User-friendly error messages
- Backend: Detailed logging with context
- LLM: Retry logic for transient failures

### 4. Extensibility

Easy to extend:
- Add new language support: Extend `CodeParser`
- Add new diagram types: Extend `DiagramRenderer`
- Add new LLM providers: Implement `LLMClient` interface

## Technology Choices

### Why TypeScript for Frontend?

- Native VS Code extension language
- Type safety for IDE API
- Rich ecosystem of VS Code extension tools

### Why Python for Backend?

- Superior AST parsing libraries (Tree-sitter)
- Easy LLM API integration
- Strong data manipulation capabilities
- Familiar to ML/AI researchers

### Why Flask?

- Lightweight and simple
- Easy to debug
- Sufficient for local development
- Future: Can scale to FastAPI if needed

### Why Tree-sitter?

- Multi-language support out of the box
- Fast incremental parsing
- Robust error recovery
- Production-ready (used by GitHub)

### Why Mermaid?

- Text-based (LLM-friendly)
- GitHub native support
- Easy to version control
- JavaScript-based (no Java dependency like PlantUML)

## Security Considerations

### API Key Management

- Stored in `.env` file (gitignored)
- Never logged or transmitted except to API
- Environment variable isolation

### Code Privacy

- All processing happens locally
- Only metadata sent to LLM (not full code)
- User consent required before generation
- Option for fully local LLM (future)

### HTTP Communication

- Local-only communication (localhost:8765)
- CORS enabled for development
- No external exposure by default

## Performance Considerations

### Parsing Optimization

- Incremental parsing (Tree-sitter)
- Parallel file processing (future)
- Smart ignore patterns

### LLM Optimization

- Prompt size optimization
- Token limit management
- Context window utilization
- Streaming responses (future)

### Caching Strategy (Future)

- Cache parsed AST
- Cache dependency graph
- Incremental updates only

## Scalability

### Current Limitations

- Single-threaded backend
- Synchronous LLM calls
- Local-only deployment

### Future Improvements

- Async/await in backend (FastAPI)
- Job queue for long-running tasks
- Distributed parsing
- Cloud deployment option

## Research Considerations

### Reproducibility

- All LLM parameters logged
- Git hash included in output
- Prompt templates versioned
- Deterministic output (low temperature)

### Metrics Collection

Collected in `generation_info.json`:
- Processing time
- Files analyzed
- Tokens used
- Model version
- Timestamp
- Git hash

### Evaluation Framework

Supports research evaluation:
- Ground truth comparison (dependency graph)
- Fidelity metrics (diagram accuracy)
- Performance metrics (time, tokens)

## Testing Strategy

### Unit Tests

- Parser: Test extraction accuracy
- Graph Builder: Test graph correctness
- LLM Client: Test API communication
- Renderer: Test diagram generation

### Integration Tests

- End-to-end pipeline
- Frontend-backend communication
- File system operations

### Validation Tests

- Output format validation
- Dependency graph validation
- Documentation completeness

## Development Roadmap

### Phase 1: Foundation (Current)
- ✅ Project setup
- 🔄 Basic parser
- 🔄 Dependency graph
- 🔄 IDE integration

### Phase 2: LLM Integration
- LLM API client
- Prompt engineering
- Basic generation
- Diagram rendering

### Phase 3: Polish
- Output organization
- Git integration
- Multi-language support
- User experience

### Phase 4: Research
- Metrics collection
- Case studies
- Evaluation framework
- Documentation

## References

- [VS Code Extension API](https://code.visualstudio.com/api)
- [Tree-sitter](https://tree-sitter.github.io/tree-sitter/)
- [DeepSeek API](https://platform.deepseek.com/api-docs/)
- [Mermaid](https://mermaid.js.org/)
- [Flask](https://flask.palletsprojects.com/)
