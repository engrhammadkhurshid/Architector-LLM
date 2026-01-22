# Development Guide - Architector-LLM

This guide is for developers who want to contribute to or extend Architector-LLM.

## Development Setup

Follow the [SETUP.md](SETUP.md) guide first, then continue here for development-specific configuration.

### Development Tools

#### Recommended VS Code Extensions

Install these extensions for optimal development experience:

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "ms-vscode.vscode-typescript-next",
    "bierner.markdown-mermaid"
  ]
}
```

Save this to `.vscode/extensions.json`

#### Python Development

```bash
# Create virtual environment
python3 -m venv backend/venv
source backend/venv/bin/activate  # On Mac/Linux
# backend\venv\Scripts\activate  # On Windows

# Install development dependencies
pip install -r backend/requirements.txt
pip install pytest pytest-cov black flake8 mypy
```

#### TypeScript Development

```bash
# Install development dependencies
npm install --save-dev \
  @types/node \
  @typescript-eslint/eslint-plugin \
  @typescript-eslint/parser \
  eslint \
  prettier
```

## Project Structure Deep Dive

### Frontend Structure

```
src/
├── extension.ts       # Entry point
│   ├── activate()    # Called when extension activates
│   └── deactivate()  # Called when extension deactivates
│
├── commands.ts        # Command implementations
│   ├── generateArchitectureDocs()
│   ├── startBackendServer()
│   └── stopBackendServer()
│
└── config.ts          # Configuration utilities
    ├── getBackendUrl()
    └── getOutputDirectory()
```

### Backend Structure

```
backend/src/
├── main.py                    # Flask HTTP server
│   ├── /health              # Health check endpoint
│   ├── /generate            # Main generation endpoint
│   └── /status/<job_id>     # Job status endpoint
│
├── parser/
│   ├── ast_parser.py         # AST parsing with Tree-sitter
│   │   ├── CodeParser
│   │   ├── parse_file()
│   │   └── parse_directory()
│   │
│   └── dependency_graph.py   # Dependency graph construction
│       ├── DependencyGraphBuilder
│       └── build_graph()
│
├── llm/
│   ├── client.py             # LLM API client
│   │   ├── LLMClient
│   │   ├── generate()
│   │   └── test_connection()
│   │
│   └── prompt_curator.py     # Prompt engineering
│       ├── PromptCurator
│       └── curate_prompt()
│
├── diagram/
│   └── renderer.py           # Mermaid diagram rendering
│       ├── DiagramRenderer
│       └── render()
│
└── output/
    └── organizer.py          # Output organization
        ├── OutputOrganizer
        ├── create_output_directory()
        └── save_documentation()
```

## Development Workflow

### 1. Feature Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/your-feature-name

# 2. Make changes

# 3. Test locally
npm run compile
npm run start-backend
# Press F5 in VS Code to test extension

# 4. Run tests
cd backend
pytest tests/

# 5. Commit changes
git add .
git commit -m "feat: add your feature"

# 6. Push and create PR
git push origin feature/your-feature-name
```

### 2. Development Commands

#### Frontend (TypeScript)

```bash
# Compile TypeScript
npm run compile

# Watch mode (auto-compile on save)
npm run watch

# Lint TypeScript
npm run lint

# Package extension
npm run package
```

#### Backend (Python)

```bash
# Run server
python backend/src/main.py

# Run tests
cd backend
pytest tests/

# Run tests with coverage
pytest tests/ --cov=src --cov-report=html

# Format code
black src/

# Lint code
flake8 src/

# Type check
mypy src/
```

### 3. Debugging

#### Debug Frontend (Extension)

1. Open project in VS Code
2. Set breakpoints in TypeScript files
3. Press `F5` to launch Extension Development Host
4. Debugger will attach automatically
5. Trigger commands to hit breakpoints

**Launch Configuration (.vscode/launch.json):**

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Run Extension",
      "type": "extensionHost",
      "request": "launch",
      "args": [
        "--extensionDevelopmentPath=${workspaceFolder}"
      ],
      "outFiles": [
        "${workspaceFolder}/out/**/*.js"
      ],
      "preLaunchTask": "${defaultBuildTask}"
    }
  ]
}
```

#### Debug Backend (Python)

**Option 1: VS Code Python Debugger**

Add to `.vscode/launch.json`:

```json
{
  "name": "Python: Backend Server",
  "type": "python",
  "request": "launch",
  "program": "${workspaceFolder}/backend/src/main.py",
  "console": "integratedTerminal",
  "justMyCode": true,
  "env": {
    "PYTHONPATH": "${workspaceFolder}/backend/src"
  }
}
```

**Option 2: Print Debugging**

```python
import logging
logger = logging.getLogger(__name__)
logger.info(f'Debug: {variable}')
```

Check logs in terminal running the backend.

## Adding New Features

### Adding a New Programming Language

**1. Install Tree-sitter grammar:**

```bash
pip install tree-sitter-<language>
```

**2. Update `ast_parser.py`:**

```python
def _detect_language(self, file_extension: str) -> str:
    extension_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.go': 'go',  # Add new language
    }
    return extension_map.get(file_extension.lower(), 'unknown')

def _is_source_file(self, filename: str) -> bool:
    source_extensions = {'.py', '.js', '.ts', '.go'}  # Add extension
    return Path(filename).suffix.lower() in source_extensions
```

**3. Add language-specific parsing logic:**

```python
def _parse_go_file(self, file_path: str):
    # Implement Go-specific parsing
    pass
```

### Adding a New LLM Provider

**1. Create new client in `llm/client.py`:**

```python
class OpenAIClient:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        # ...
    
    def generate(self, prompt: str, system_prompt: str = None):
        # Implement OpenAI API call
        pass
```

**2. Add configuration:**

```bash
# In .env
LLM_PROVIDER=openai  # or deepseek
OPENAI_API_KEY=sk-...
```

**3. Update main.py to use correct client:**

```python
from llm.client import LLMClient, OpenAIClient

provider = os.getenv('LLM_PROVIDER', 'deepseek')
if provider == 'openai':
    client = OpenAIClient()
else:
    client = LLMClient()
```

### Adding a New Diagram Type

**1. Extend `diagram/renderer.py`:**

```python
def render_plantuml(self, code: str, output_path: str):
    """Render PlantUML diagrams"""
    # Implementation
    pass

def render(self, code: str, output_path: str, diagram_type: str = 'mermaid'):
    if diagram_type == 'plantuml':
        return self.render_plantuml(code, output_path)
    elif diagram_type == 'mermaid':
        return self.render_mermaid(code, output_path)
```

**2. Update prompt in `llm/prompt_curator.py`:**

```python
SYSTEM_PROMPT = """
...
Generate both:
1. Mermaid diagram
2. PlantUML diagram (optional)
"""
```

### Adding New Commands

**1. Register command in `package.json`:**

```json
{
  "contributes": {
    "commands": [
      {
        "command": "architector-llm.validateDocs",
        "title": "Validate Generated Documentation",
        "category": "Architector"
      }
    ]
  }
}
```

**2. Implement in `src/commands.ts`:**

```typescript
export async function validateDocumentation(): Promise<void> {
    // Implementation
}
```

**3. Register in `src/extension.ts`:**

```typescript
const validateCommand = vscode.commands.registerCommand(
    'architector-llm.validateDocs',
    async () => {
        await validateDocumentation();
    }
);
context.subscriptions.push(validateCommand);
```

## Testing Guidelines

### Unit Testing

#### Python Tests

```python
# backend/tests/test_new_feature.py
import unittest
from your_module import YourClass

class TestYourFeature(unittest.TestCase):
    def setUp(self):
        self.instance = YourClass()
    
    def test_something(self):
        result = self.instance.method()
        self.assertEqual(result, expected_value)
```

Run tests:
```bash
cd backend
pytest tests/test_new_feature.py -v
```

#### TypeScript Tests

```typescript
// src/test/extension.test.ts
import * as assert from 'assert';
import * as vscode from 'vscode';

suite('Extension Test Suite', () => {
    test('Sample test', () => {
        assert.strictEqual(1 + 1, 2);
    });
});
```

### Integration Testing

Test the full pipeline:

```python
# backend/tests/test_integration.py
def test_full_pipeline():
    # 1. Parse test codebase
    parser = CodeParser()
    parsed_files = parser.parse_directory('test-repo/')
    
    # 2. Build graph
    builder = DependencyGraphBuilder()
    graph = builder.build_graph(parsed_files)
    
    # 3. Curate prompt
    curator = PromptCurator()
    prompt = curator.curate_prompt(graph, 'test-repo/')
    
    # 4. Generate (mock LLM response)
    # 5. Render
    # 6. Organize output
    
    assert os.path.exists('docs/arch/')
```

### Manual Testing Checklist

Before submitting a PR:

- [ ] Extension activates without errors
- [ ] Backend starts successfully
- [ ] Health check endpoint responds
- [ ] Can generate documentation for test repo
- [ ] Output files are created correctly
- [ ] Diagrams render (if Mermaid CLI installed)
- [ ] No errors in VS Code Developer Tools console
- [ ] No Python exceptions in backend logs

## Code Style

### Python Style

Follow PEP 8:

```python
# Good
def parse_file(file_path: str) -> Dict[str, Any]:
    """
    Parse a single file
    
    Args:
        file_path: Path to the file
        
    Returns:
        Parsed metadata
    """
    logger.info(f'Parsing {file_path}')
    return {}

# Bad
def parseFile(filePath):
    print('Parsing', filePath)
    return {}
```

Use type hints:
```python
from typing import Dict, List, Any, Optional

def function(param: str) -> Optional[Dict[str, Any]]:
    pass
```

### TypeScript Style

Follow standard TypeScript conventions:

```typescript
// Good
async function generateDocs(path: string): Promise<void> {
    const result = await backendCall(path);
    console.log(`Generated: ${result}`);
}

// Bad
function generateDocs(path) {
    backendCall(path).then(result => {
        console.log('Generated: ' + result);
    });
}
```

### Documentation Style

Use clear, concise docstrings:

```python
def build_graph(self, parsed_files: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Build a dependency graph from parsed file data
    
    Args:
        parsed_files: List of parsed file metadata from CodeParser
        
    Returns:
        Structured dependency graph with nodes, edges, and metadata
        
    Raises:
        ValueError: If parsed_files is empty
    """
    pass
```

## Performance Optimization

### Profiling Python Code

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Your code here

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumtime')
stats.print_stats(20)
```

### Monitoring LLM Costs

Track token usage:

```python
response = client.generate(prompt)
tokens_used = response['usage']['total_tokens']
logger.info(f'Tokens used: {tokens_used}')
```

## Contributing Guidelines

### Commit Messages

Follow Conventional Commits:

```
feat: add support for Go language parsing
fix: correct dependency graph edge creation
docs: update setup guide with new requirements
test: add tests for OutputOrganizer
refactor: simplify prompt curation logic
perf: optimize file parsing loop
```

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings
```

## Troubleshooting Development Issues

### Tree-sitter Installation Issues

If Tree-sitter fails to install:

```bash
# Mac
brew install tree-sitter

# Linux
sudo apt-get install tree-sitter

# Then reinstall Python package
pip install --force-reinstall tree-sitter
```

### Extension Not Loading

Clear VS Code extension cache:

```bash
rm -rf ~/.vscode/extensions/
code --disable-extensions
```

### Backend Import Errors

Set PYTHONPATH:

```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/backend/src"
```

## Release Process

1. **Version Bump**
   ```bash
   # package.json
   "version": "1.1.0"
   
   # backend/setup.py
   version="1.1.0"
   ```

2. **Changelog Update**
   ```markdown
   ## [1.1.0] - 2026-01-25
   ### Added
   - New feature X
   ### Fixed
   - Bug Y
   ```

3. **Tag Release**
   ```bash
   git tag -a v1.1.0 -m "Release v1.1.0"
   git push origin v1.1.0
   ```

4. **Package Extension**
   ```bash
   npm run package
   # Creates architector-llm-1.1.0.vsix
   ```

## Resources

- [VS Code Extension API](https://code.visualstudio.com/api)
- [Tree-sitter Documentation](https://tree-sitter.github.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Mermaid Documentation](https://mermaid.js.org/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

## Getting Help

- Check existing issues on GitHub
- Review documentation files
- Ask in project discussions
- Consult with maintainers
