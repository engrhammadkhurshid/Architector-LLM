# Usage Guide - Architector-LLM

This guide explains how to use the Architector-LLM extension to generate architecture documentation for your projects.

## Quick Start

### Step 1: Ensure Backend is Running

Open the Command Palette (`Cmd+Shift+P` on Mac, `Ctrl+Shift+P` on Windows/Linux) and run:

```
Architector: Start Backend Server
```

You should see a notification: "Backend server started successfully"

### Step 2: Open Your Project

Open the codebase you want to document in VS Code:
```
File → Open Folder...
```

### Step 3: Generate Documentation

1. Open the Command Palette (`Cmd+Shift+P`)
2. Type "Architector" and select:
   ```
   Architector: Generate Architecture Documentation
   ```
3. Wait for the process to complete (progress will be shown)
4. Choose to open the documentation or show it in Explorer

## Understanding the Output

The generated documentation will be saved in:
```
your-project/docs/arch/v{version}_{timestamp}_{git-hash}/
```

### Output Structure

```
docs/arch/v1.0.0_2026-01-21-143022_abc123f/
├── README.md                        # Main architecture documentation
├── INDEX.md                         # Index of all artifacts
├── diagrams/
│   ├── architecture.mmd            # Mermaid source code
│   └── architecture.png            # Rendered diagram (if Mermaid CLI installed)
└── metadata/
    └── generation_info.json        # Generation metrics and metadata
```

### Generated Content

#### README.md - Architecture Documentation

The main documentation includes:

1. **System Overview**
   - High-level description of the system
   - Key architectural patterns identified

2. **Architecture Patterns**
   - Design patterns used in the codebase
   - Rationale for pattern choices

3. **Component Descriptions**
   - Major components and their responsibilities
   - Component interactions

4. **Key Design Decisions**
   - Important architectural decisions
   - Trade-offs and considerations

5. **Dependency Analysis**
   - Component dependencies
   - External dependencies

6. **Deployment Considerations**
   - Deployment architecture
   - Infrastructure requirements

#### Diagrams

**architecture.mmd** - Contains Mermaid diagram code that can be:
- Viewed directly in GitHub (native support)
- Rendered to PNG/SVG using Mermaid CLI
- Edited and customized for your needs

Diagram types may include:
- C4 Context diagrams
- Component diagrams
- Flowcharts
- Sequence diagrams

#### Metadata

**generation_info.json** - Contains:
```json
{
  "generated_at": "2026-01-21T14:30:22.123456",
  "git_hash": "abc123f",
  "semantic_version": "1.0.0",
  "files_analyzed": 42,
  "processing_time": 45.2,
  "llm_model": "deepseek-coder",
  "llm_metrics": {
    "tokens_used": 3245,
    "temperature": 0.2
  }
}
```

## Advanced Usage

### Customizing Output Location

You can change the output directory in VS Code settings:

1. Open Settings (`Cmd+,`)
2. Search for "architector"
3. Modify `Architector: Output Directory`

Default: `docs/arch`

### Manual Backend Control

If you don't want the backend to start automatically:

1. Open Settings
2. Search for "architector"
3. Uncheck `Architector: Auto Start Backend`

Then manually control the backend:
```
Architector: Start Backend Server
Architector: Stop Backend Server
```

### Custom Port Configuration

If port 8765 is already in use:

1. Open `.env` file in project root
2. Change `BACKEND_PORT=8765` to another port
3. Update VS Code settings → `Architector: Backend Port`
4. Restart the backend server

### Versioning Strategy

The output directory name follows this format:
```
v{semantic_version}_{timestamp}_{git_hash}
```

**Examples:**
- `v1.0.0_2026-01-21-143022_abc123f` - Initial release
- `v1.1.0_2026-01-25-091545_def456g` - Feature update
- `v2.0.0_2026-02-01-160000_ghi789h` - Major refactor

To control semantic versioning:
- Currently set in code (default: 1.0.0)
- Future: Will read from package.json or manual input

### Working with Multiple Projects

You can generate documentation for different projects:

1. Open Project A
2. Generate documentation
3. Close Project A
4. Open Project B
5. Generate documentation

Each project's documentation is stored in its own `docs/arch/` directory.

## Best Practices

### When to Generate Documentation

Generate architecture documentation:

✅ **Good times:**
- After major feature completion
- Before code reviews
- For onboarding new team members
- When preparing technical documentation
- After significant refactoring

❌ **Avoid:**
- During active development (code changes frequently)
- For incomplete features
- For prototypes or experimental code

### Preparing Your Codebase

For best results:

1. **Clean up temporary files:**
   ```bash
   # Remove node_modules, __pycache__, etc.
   ```

2. **Ensure code is well-structured:**
   - Use clear class/function names
   - Include docstrings/comments for complex logic
   - Follow consistent coding patterns

3. **Commit your changes:**
   - Documentation includes git hash
   - Ensures reproducibility

### Reviewing Generated Documentation

After generation:

1. **Review for accuracy:**
   - Check if identified patterns are correct
   - Verify component descriptions

2. **Supplement with context:**
   - Add business context
   - Include deployment specifics
   - Add team/process information

3. **Version control:**
   - Commit generated docs to git
   - Use tags for major versions

## Examples

### Example 1: Simple Python Project

```bash
# Project structure
my-flask-app/
├── app.py
├── models/
│   ├── user.py
│   └── post.py
└── utils/
    └── helpers.py
```

**Generated documentation will include:**
- Flask application architecture
- Model relationships
- Route structure
- Utility function purposes

### Example 2: TypeScript/Node.js Project

```bash
# Project structure
my-node-api/
├── src/
│   ├── controllers/
│   ├── services/
│   ├── models/
│   └── routes/
└── package.json
```

**Generated documentation will include:**
- Express.js architecture
- Controller-Service pattern
- API endpoints
- Data models

### Example 3: Monorepo

For monorepos, open the specific package you want to document:
```
File → Open Folder... → /monorepo/packages/backend
```

Then generate documentation for that specific package.

## Troubleshooting

### No Output Generated

**Problem:** Command completes but no documentation created

**Possible causes:**
1. Backend not running - Check with: `curl http://localhost:8765/health`
2. No source files found - Ensure project has .py, .js, or .ts files
3. LLM API error - Check backend logs

**Solution:**
```bash
# Check backend logs
# In terminal running backend, look for errors
```

### Incomplete Documentation

**Problem:** Documentation is very brief or missing sections

**Possible causes:**
1. Small codebase (< 5 files)
2. LLM context limits exceeded
3. Unclear code structure

**Solution:**
- Add more descriptive comments to your code
- Ensure proper code organization
- Review LLM configuration (temperature, tokens)

### Diagram Not Rendering

**Problem:** Only .mmd file generated, no PNG/SVG

**Cause:** Mermaid CLI not installed

**Solution:**
```bash
npm install -g @mermaid-js/mermaid-cli
```

Then manually render:
```bash
mmdc -i docs/arch/v1.0.0_*/diagrams/architecture.mmd -o output.png
```

## Keyboard Shortcuts

You can add custom keyboard shortcuts:

1. Open Keyboard Shortcuts (`Cmd+K Cmd+S`)
2. Search for "Architector: Generate Architecture Documentation"
3. Click the `+` icon and assign your preferred shortcut

Suggested: `Cmd+Shift+A` or `Ctrl+Shift+A`

## Integration with CI/CD

You can automate documentation generation in your CI/CD pipeline:

```yaml
# Example GitHub Actions workflow
name: Generate Architecture Docs

on:
  push:
    branches: [main]

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Generate docs
        env:
          DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
        run: |
          # Start backend and call API
          python backend/src/main.py &
          sleep 5
          curl -X POST http://localhost:8765/generate \
            -H "Content-Type: application/json" \
            -d '{"codebase_path": "'$PWD'"}'
      - name: Commit docs
        run: |
          git config user.name "Bot"
          git config user.email "bot@example.com"
          git add docs/arch/
          git commit -m "Update architecture docs"
          git push
```

## Next Steps

- Read [ARCHITECTURE.md](ARCHITECTURE.md) to understand how the system works
- Read [DEVELOPMENT.md](DEVELOPMENT.md) to contribute to the project
- Explore generated documentation examples
