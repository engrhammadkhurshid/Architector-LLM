# Quick Test Guide - v2.0.8

## Pre-Test Verification

### 1. Check Parser Compilation
```bash
cd "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM"
python3 -m py_compile backend/src/parser/ast_parser.py
# Should complete without errors
```

### 2. Test Parser Import
```bash
cd "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM/backend"
python3 -c "import sys; sys.path.insert(0, 'src'); from parser.ast_parser import CodeParser; print('✅ Import successful')"
```

### 3. Test Parser Initialization
```bash
cd "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM/backend"
python3 -c "
import sys
sys.path.insert(0, 'src')
from parser.ast_parser import CodeParser
parser = CodeParser()
print(f'✅ Initialized {len(parser.parsers)} parsers')
print(f'Languages: {list(parser.parsers.keys())}')
"
```

Expected output:
```
✅ Initialized 11 parsers
Languages: ['python', 'javascript', 'typescript', 'php', 'java', 'c', 'cpp', 'csharp', 'go', 'rust', 'ruby']
```

---

## Package Extension

```bash
cd "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM"

# Build extension
npm run package-extension

# Create VSIX
npx vsce package --out architector-llm-2.0.8.vsix

# Verify created
ls -lh architector-llm-2.0.8.vsix
```

---

## Install Extension

### Option 1: VS Code Command Line
```bash
# Remove old version
code --uninstall-extension enghammadkhurshid.architector-llm

# Install new version
code --install-extension "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM/architector-llm-2.0.8.vsix"
```

### Option 2: VS Code UI
1. Open VS Code
2. Press `Cmd+Shift+P`
3. Run: "Extensions: Install from VSIX..."
4. Select: `architector-llm-2.0.8.vsix`

---

## Test on WordPress Project

```bash
cd "/Users/hammadkhurshidchughtaii/Downloads/WP Project Gaurd/wp-project-guard"

# Method 1: Via VS Code
# - Open project in VS Code
# - Press Cmd+Shift+P
# - Run: "Architector: Generate Documentation"
# - Leave version empty (test auto-detect)
# - OR enter "1.0.0" manually

# Method 2: Via Command Line
cd ~/.vscode/extensions/enghammadkhurshid.architector-llm-2.0.8
python3 architector.py "/Users/hammadkhurshidchughtaii/Downloads/WP Project Gaurd/wp-project-guard" "1.0.0"
```

### Expected Results:
- ✅ No syntax errors
- ✅ No import errors
- ✅ Parser initializes all 11 languages
- ✅ PHP files detected and parsed
- ✅ WordPress plugin detected
- ✅ Classes extracted (4 expected)
- ✅ Functions extracted (15 expected)
- ✅ Documentation generated in `architector_docs/`

### Check Output:
```bash
cd "/Users/hammadkhurshidchughtaii/Downloads/WP Project Gaurd/wp-project-guard"
ls -la architector_docs/

# View metadata
cat architector_docs/v*/generation_info.json | jq

# Expected:
# {
#   "language": "php",  ← Should be PHP, not JavaScript
#   "project_type": "wordpress_plugin",  ← Should detect WordPress
#   "files_analyzed": 9,  ← Should be 9, not 1
#   "total_classes": 4,  ← Should be 4, not 0
#   "total_functions": 15,  ← Should be 15, not 0
#   "llm_provider": "ollama"
# }
```

---

## Validation Checklist

### Language Detection ✅ / ❌
- [ ] Detected as PHP (not JavaScript)
- [ ] All 9 PHP files found
- [ ] Classes detected: 4
- [ ] Functions detected: 15

### Framework Detection ✅ / ❌
- [ ] WordPress plugin detected
- [ ] Plugin Name extracted
- [ ] Version extracted from header

### Documentation Quality ✅ / ❌
- [ ] README.md generated
- [ ] Class documentation present
- [ ] Function documentation present
- [ ] WordPress-specific content
- [ ] Architecture diagrams created

### Version Detection ✅ / ❌
- [ ] Auto-detects "1.0.0" from plugin header
- [ ] Version appears in output folder name
- [ ] Documentation versioned correctly

---

## If Issues Occur

### 1. Parser Import Error
```bash
# Check Python path
cd ~/.vscode/extensions/enghammadkhurshid.architector-llm-2.0.8
python3 -c "import sys; print(sys.path)"

# Verify backend structure
ls -la backend/src/parser/
```

### 2. Tree-sitter Error
```bash
# Check installed version
pip3 show tree-sitter

# Should be 0.22.3
# If different, reinstall:
pip3 uninstall -y tree-sitter
pip3 install tree-sitter==0.22.3
```

### 3. PHP Parser Missing
```bash
# Check if installed
pip3 show tree-sitter-php

# Should show version 0.23.11
# If missing:
pip3 install tree-sitter-php==0.23.11
```

### 4. Extension Won't Activate
- Check VS Code Developer Tools (Help → Toggle Developer Tools)
- Look for errors in Console tab
- Check extension host logs

---

## Success Criteria

**Minimum Acceptable:**
- ✅ Extension installs without errors
- ✅ Parser initializes without errors
- ✅ Detects PHP as primary language
- ✅ Finds all 9 PHP files
- ✅ Extracts at least some classes/functions
- ✅ Generates documentation output

**Ideal Result:**
- ✅ All above +
- ✅ Correctly identifies 4 classes
- ✅ Correctly identifies 15 functions
- ✅ Detects WordPress plugin framework
- ✅ Auto-detects version "1.0.0"
- ✅ Generates WordPress-specific documentation
- ✅ Quality score > 70/100

---

## Report Results

After testing, report:

1. **Installation:** Success / Failed
2. **Parser Initialization:** Success / Failed
3. **Language Detection:** Correct / Incorrect (specify what was detected)
4. **Files Analyzed:** [number] / 9 expected
5. **Classes Found:** [number] / 4 expected
6. **Functions Found:** [number] / 15 expected
7. **Documentation Quality:** Good / Fair / Poor
8. **Overall:** Pass / Fail

Save output to:
```
/Users/hammadkhurshidchughtaii/Downloads/WP Project Gaurd/wp-project-guard/ARCHITECTOR_LLM_v208_TEST_REPORT.md
```

---

**Good luck with testing!** 🚀
