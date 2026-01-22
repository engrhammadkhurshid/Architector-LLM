# 🚀 Architector-LLM Setup Guide

## Complete Installation & Usage Guide for VS Code Extension

---

## Phase 4: Testing on Real Open-Source Projects

### Selected Test Projects

We'll test on 3 diverse Python projects:

1. **Flask-RESTful API** (Web Framework)
   - Repo: `miguelgrinberg/microblog`
   - Type: Web application with database, authentication, REST API
   - Lines: ~5,000
   - Purpose: Tests web app architecture visualization

2. **Rich** (CLI/Terminal Library)  
   - Repo: `Textualize/rich`
   - Type: Library with extensive class hierarchy
   - Lines: ~10,000
   - Purpose: Tests OOP and library architecture

3. **HTTPie** (CLI Tool)
   - Repo: `httpie/cli`
   - Type: Command-line HTTP client
   - Lines: ~8,000
   - Purpose: Tests CLI tool architecture

---

## 📋 Prerequisites

### 1. System Requirements

- **OS**: macOS, Linux, or Windows
- **Python**: 3.9+ (you have 3.9 ✅)
- **Node.js**: 16+ (for Mermaid CLI)
- **VS Code**: Latest version
- **Git**: For cloning repositories

### 2. Install Ollama (Local LLM)

```bash
# macOS (already installed ✅)
# Verify installation
ollama --version  # Should show 0.14.2

# Ensure deepseek-coder model is available
ollama pull deepseek-coder:6.7b

# Start Ollama service (if not running)
ollama serve
```

### 3. Install Mermaid CLI

```bash
# Install globally with npm
npm install -g @mermaid-js/mermaid-cli

# Verify installation
mmdc --version  # Should show 11.12.0 or higher ✅
```

### 4. Python Dependencies

```bash
cd "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM"

# Install required packages
pip3 install tree-sitter requests flask

# Verify tree-sitter installation
python3 -c "import tree_sitter; print('✓ tree-sitter ready')"
```

---

## 🔧 Setup VS Code Extension

### Option A: Run as Standalone Tool (Current Setup) ✅

**This is what we have now - works without VS Code extension!**

```bash
# Navigate to project
cd "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM"

# Run on any codebase
python3 test_real_project.py
```

### Option B: Create VS Code Extension (Full Integration)

**To build the VS Code extension:**

```bash
# 1. Install VS Code extension development tools
npm install -g yo generator-code

# 2. Create extension structure
yo code
# Choose: New Extension (TypeScript)
# Name: architector-llm
# Identifier: architector-llm
# Description: Multi-diagram architecture documentation generator
# Initialize git: Yes
# Package manager: npm

# 3. Copy backend to extension
mkdir -p architector-llm/backend
cp -r backend/src architector-llm/backend/

# 4. Install extension dependencies
cd architector-llm
npm install

# 5. Open in VS Code
code .

# 6. Press F5 to launch Extension Development Host
```

### Option C: Quick Command-Line Interface (What we'll use)

```bash
# Create a simple CLI wrapper
cat > architector << 'EOF'
#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'backend' / 'src'))
from pipeline import DocumentationPipeline

if len(sys.argv) < 2:
    print("Usage: architector <codebase-path> [version]")
    sys.exit(1)

codebase = sys.argv[1]
version = sys.argv[2] if len(sys.argv) > 2 else "1.0.0"

pipeline = DocumentationPipeline()
result = pipeline.generate(codebase, version)

if result['status'] == 'success':
    print(f"✅ Documentation generated: {result['output_dir']}")
else:
    print(f"❌ Failed: {result.get('error')}")
    sys.exit(1)
EOF

chmod +x architector

# Now you can run:
# ./architector <path-to-project>
```

---

## 📦 Testing on Open-Source Projects

### Project 1: Flask Microblog (Web Application)

```bash
# Step 1: Clone the repository
cd ~/Downloads
git clone https://github.com/miguelgrinberg/microblog.git
cd microblog

# Step 2: Explore the structure
ls -la
# Expected: app/, migrations/, config.py, microblog.py, requirements.txt

# Step 3: Run Architector-LLM
cd "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM"
python3 test_real_project.py ~/Downloads/microblog

# Step 4: View results
ls -la "architecture-docs/microblog/v1.0.0_"*
open "architecture-docs/microblog/v1.0.0_"*/README.md
```

**Expected Output:**
- Component Diagram (Flask app structure)
- Class Diagram (models, forms, routes)
- Sequence Diagram (authentication flow)
- ER Diagram (database schema)
- Quality Report (80-95/100)

### Project 2: Rich (Library/Framework)

```bash
# Step 1: Clone the repository
cd ~/Downloads
git clone https://github.com/Textualize/rich.git
cd rich

# Step 2: Explore the structure
ls -la rich/
# Expected: console.py, table.py, tree.py, etc.

# Step 3: Run Architector-LLM (on rich/ subdirectory)
cd "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM"
python3 test_real_project.py ~/Downloads/rich/rich

# Step 4: View results
open "architecture-docs/rich/v1.0.0_"*/README.md
```

**Expected Output:**
- Class Diagram (extensive OOP hierarchy)
- Package Diagram (module organization)
- Component Diagram (rendering pipeline)
- Quality Report (85-95/100)

### Project 3: HTTPie CLI (Command-Line Tool)

```bash
# Step 1: Clone the repository
cd ~/Downloads
git clone https://github.com/httpie/cli.git httpie-cli
cd httpie-cli

# Step 2: Explore the structure
ls -la httpie/
# Expected: cli.py, core.py, sessions.py, plugins/

# Step 3: Run Architector-LLM
cd "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM"
python3 test_real_project.py ~/Downloads/httpie-cli/httpie

# Step 4: View results
open "architecture-docs/httpie/v1.0.0_"*/README.md
```

**Expected Output:**
- Component Diagram (CLI architecture)
- Activity Diagram (request processing flow)
- Class Diagram (plugin system)
- Sequence Diagram (HTTP request lifecycle)
- Quality Report (80-90/100)

---

## 🎯 Step-by-Step Workflow

### Complete Workflow for Any Project

```bash
# 1. Start Ollama (if not running)
ollama serve &

# 2. Verify model is available
ollama list | grep deepseek-coder

# 3. Clone target repository
cd ~/Downloads
git clone <repo-url> <project-name>

# 4. Navigate to Architector-LLM
cd "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM"

# 5. Run documentation generation
python3 -c "
import sys
from pathlib import Path
sys.path.insert(0, 'backend/src')
from pipeline import DocumentationPipeline

pipeline = DocumentationPipeline()
result = pipeline.generate('~/Downloads/<project-name>', '1.0.0')
print(f'Output: {result[\"output_dir\"]}')
"

# 6. View results
open architecture-docs/<project-name>/v1.0.0_*/README.md

# 7. Explore all artifacts
cd architecture-docs/<project-name>/v1.0.0_*
ls -la
# README.md - Main documentation
# QUALITY_REPORT.md - Quality metrics
# RELATIONSHIPS.md - Cross-diagram analysis
# INDEX.md - Navigation guide
# diagrams/ - All diagrams (PNG, SVG, Mermaid)
# docs/ - Category documentation
```

---

## 🔍 Understanding the Output

### Generated Files Structure

```
architecture-docs/
└── <project-name>/
    └── v1.0.0_<timestamp>_<hash>/
        ├── README.md                    # Main documentation with embedded diagrams
        ├── QUALITY_REPORT.md           # Quality assessment (Phase 3.2)
        ├── RELATIONSHIPS.md            # Cross-diagram relationships (Phase 3.3)
        ├── COMPARISONS.md              # Side-by-side comparisons (Phase 3.4)
        ├── INDEX.md                    # Interactive navigation (Phase 3.4)
        ├── diagrams/
        │   ├── component.mmd           # Mermaid source
        │   ├── component.png           # Rendered image
        │   ├── component.svg           # Vector graphic
        │   ├── class.mmd/.png/.svg
        │   ├── sequence.mmd/.png/.svg
        │   └── ... (5-8 diagrams)
        ├── docs/
        │   ├── structural-diagrams.md
        │   ├── behavioral-diagrams.md
        │   └── data-diagrams.md
        └── metadata/
            └── generation_info.json    # Processing metrics
```

### Key Features to Check

1. **README.md Quality Badges**: Each diagram shows quality score (0-100)
2. **QUALITY_REPORT.md**: Executive summary with scores and recommendations
3. **RELATIONSHIPS.md**: Shows which entities appear across multiple diagrams
4. **INDEX.md**: Quick navigation with quality indicators
5. **Diagrams**: Multiple formats for different use cases

---

## 📊 Performance Metrics to Measure

For each project, document:

```bash
# Extract metrics from metadata
cat architecture-docs/<project>/v1.0.0_*/metadata/generation_info.json | \
  python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f'Files Analyzed: {data[\"files_analyzed\"]}')
print(f'Classes Found: {data[\"total_classes\"]}')
print(f'Diagrams Generated: {data[\"diagrams_successful\"]}/{data[\"diagrams_generated\"]}')
print(f'Average Quality: {data[\"average_quality_score\"]:.1f}/100')
print(f'Processing Time: {data[\"processing_time\"]}s')
print(f'Shared Entities: {data[\"shared_entities\"]}')
print(f'Diagram Connections: {data[\"diagram_connections\"]}')
"
```

---

## 🐛 Troubleshooting

### Issue: "Ollama not responding"
```bash
# Check if Ollama is running
ps aux | grep ollama

# Restart Ollama
pkill ollama
ollama serve &

# Wait a few seconds, then test
curl http://localhost:11434/api/tags
```

### Issue: "Tree-sitter parser error"
```bash
# Reinstall tree-sitter
pip3 uninstall tree-sitter
pip3 install tree-sitter

# Rebuild parsers
python3 -c "from tree_sitter import Language; print('OK')"
```

### Issue: "Mermaid rendering failed"
```bash
# Check mmdc installation
which mmdc
mmdc --version

# Reinstall if needed
npm install -g @mermaid-js/mermaid-cli@latest
```

### Issue: "Import errors"
```bash
# Ensure you're in the right directory
cd "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM"

# Check Python path
python3 -c "import sys; print('\\n'.join(sys.path))"
```

---

## 🎓 Next Steps

1. **Test on 3 projects** (as outlined above)
2. **Compare results** across different project types
3. **Measure quality scores** and processing times
4. **Document findings** for research paper
5. **Optional**: Build full VS Code extension for one-click generation

---

## 📝 Research Data Collection

Create a results table:

| Project | Type | Files | Classes | Diagrams | Avg Quality | Time | Shared Entities |
|---------|------|-------|---------|----------|-------------|------|-----------------|
| Microblog | Web App | ? | ? | ?/8 | ?/100 | ?s | ? |
| Rich | Library | ? | ? | ?/8 | ?/100 | ?s | ? |
| HTTPie | CLI Tool | ? | ? | ?/8 | ?/100 | ?s | ? |

Fill this in after running each test!

---

**Ready to begin? Start with Project 1 (Microblog)!**
