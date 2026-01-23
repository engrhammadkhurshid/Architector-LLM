# Architector-LLM Extension Test Report

**Test Date:** January 23, 2026  
**Tester:** Hammad Khurshid Chughtai  
**Extension:** Architector-LLM by enghammadkhurshid  
**Versions Tested:** v1.0.0, v2.0.3, v2.0.4, v2.0.5  
**Test Project:** WP Project Guard (WordPress Plugin)

---

## Executive Summary

Comprehensive testing of the Architector-LLM VS Code extension revealed **critical functionality issues** that prevent it from working correctly for PHP-based WordPress projects. While the extension shows promise for Python/JavaScript/TypeScript codebases, **it cannot analyze PHP code** due to missing language parser support.

### Key Findings

✅ **Working Features:**
- Ollama integration and model detection
- Python backend infrastructure
- Documentation generation pipeline
- Diagram generation (component, C4 context)
- Metadata JSON output

❌ **Critical Issues:**
- **PHP language completely unsupported** (no tree-sitter-php parser)
- LLM_PROVIDER defaults to wrong value ('deepseek' instead of 'ollama')
- Setup wizard doesn't auto-run on extension installation
- Only Python/JavaScript/TypeScript supported (undocumented limitation)

### Test Outcome

**Overall Result:** ❌ **FAILED** for WordPress/PHP projects  
**Accuracy:** 0% (detected 0/6 project metrics correctly)  
**Usability:** Poor (requires manual workarounds)  
**Recommendation:** Extension requires PHP support before production use on WordPress projects

---

## Test Environment

### System Configuration
- **OS:** macOS (LibreSSL 2.8.3)
- **VS Code:** Latest version
- **Python:** 3.9.6
- **LLM Provider:** Ollama (localhost:11434)
- **LLM Model:** deepseek-coder:6.7b (local)

### Extension Installation
- **Method:** VSIX file installation
- **Location:** `~/.vscode/extensions/enghammadkhurshid.architector-llm-2.0.5`
- **Backend:** Python Flask application
- **Dependencies:** Flask 3.1.2, tree-sitter 0.23.2, requests, dotenv

### Test Project Details
- **Name:** WP Project Guard
- **Type:** WordPress Security Plugin
- **Language:** PHP 7.4+
- **File Count:** 9 PHP files
- **Lines of Code:** 507
- **Classes:** 4 (WP_Project_Guard_Admin_UI, WP_Project_Guard_Settings, WP_Project_Guard_Guard, base class)
- **Functions:** 15
- **Structure:**
  ```
  wp-project-guard/
  ├── wp-project-guard.php (main plugin file, 69 LOC)
  ├── includes/
  │   ├── class-admin-ui.php (227 LOC)
  │   ├── class-settings.php (58 LOC)
  │   └── helpers.php (56 LOC)
  ├── public/
  │   ├── class-guard.php (85 LOC)
  │   └── templates/ (3 files)
  └── uninstall.php (12 LOC)
  ```

---

## Version Testing History

### v1.0.0 - Complete Failure

**Installation Date:** January 23, 2026  
**Test Result:** ❌ Extension completely broken

#### Critical Bugs Discovered:

1. **Backend Path Calculation Error**
   - **File:** `out/extension.js`
   - **Issue:** `path.dirname(extensionPath)` goes up wrong directory
   - **Impact:** Backend not found, extension fails to activate
   - **Fix Required:** Use `extensionPath` directly instead of parent directory

2. **Missing node_modules**
   - **Error:** `Cannot find module 'axios'`
   - **Impact:** Extension crashes on activation
   - **Fix Required:** Bundle axios with extension or update dependencies

3. **UI Escaped Newlines**
   - **Issue:** Setup wizard shows `\\n\\n` instead of line breaks
   - **Impact:** Unreadable dialog text
   - **Fix Required:** Use `\n` properly in string templates

4. **Missing .env File**
   - **Issue:** Backend requires .env but not included in VSIX
   - **Impact:** Configuration fails silently
   - **Fix Required:** Create .env from .env.example on first run

**Bug Report Generated:** 18 total issues documented

---

### v2.0.3 - Partial Improvement

**Installation Date:** January 23, 2026 (after clean uninstall)  
**Test Result:** ⚠️ Installs but setup wizard doesn't auto-run

#### Issues Found:

1. **Setup Wizard Doesn't Auto-Run**
   - **Expected:** Wizard runs on `onStartupFinished` activation event
   - **Actual:** Must manually invoke via Command Palette
   - **Impact:** Poor user experience, confusing for new users

2. **Escaped Newlines Still Present**
   - **Issue:** Dialog text still shows `\\n\\n`
   - **Status:** Not fixed from v1.0.0

3. **Backend Path Partially Fixed**
   - **Status:** Path calculation improved but still issues

---

### v2.0.4 - Incremental Fix

**Installation Date:** January 23, 2026  
**Test Result:** ⚠️ Setup wizard still manual, new activation issues

#### Changes Observed:

- Extension activation improved
- Backend path more reliable
- Setup wizard still requires manual invocation
- LLM_PROVIDER bug still present

---

### v2.0.5 - Current Version (Main Testing)

**Installation Date:** January 23, 2026  
**Test Result:** ❌ Critical bug prevents Ollama usage

#### Critical Bug: LLM_PROVIDER Default Value

**Location:** `backend/src/pipeline.py` line 34

**Current Code:**
```python
llm_provider = os.getenv('LLM_PROVIDER', 'deepseek').lower()
```

**Issue:**
- Defaults to 'deepseek' instead of 'ollama'
- Throws `ValueError: DEEPSEEK_API_KEY not found` for Ollama users
- Inconsistent with `.env.example` which shows `LLM_PROVIDER=ollama`
- Inconsistent with `backend/src/llm/client.py` which correctly defaults to 'ollama'

**Impact:**
- Extension completely broken for Ollama users (majority use case)
- Requires manual environment variable workaround
- Poor user experience

**Fix Required:**
```python
llm_provider = os.getenv('LLM_PROVIDER', 'ollama').lower()
```

**Workaround:**
```bash
LLM_PROVIDER=ollama python3 architector.py <path> <version>
```

---

## Real Project Testing

### Test Execution

**Command:**
```bash
cd ~/.vscode/extensions/enghammadkhurshid.architector-llm-2.0.5
LLM_PROVIDER=ollama python3 architector.py \
  "/Users/hammadkhurshidchughtaii/Downloads/WP Project Gaurd/wp-project-guard" \
  "1.0.0" 2>&1 | tee /tmp/architector_full_output.log
```

**Execution Time:** 24.3 seconds  
**Status:** ✅ Completed without errors  
**Output:** Documentation generated in `output/` directory

### Generated Output Structure

```
output/
├── README.md (project documentation)
├── diagrams/
│   ├── component.png
│   ├── component.svg
│   ├── c4_context.png
│   └── c4_context.svg
├── generation_info.json (metadata)
└── quality_report.json (quality metrics)
```

---

## Test Results Analysis

### Expected vs Actual Detection

| Metric | Expected (Reality) | Detected (Extension) | Match |
|--------|-------------------|---------------------|-------|
| **Language** | PHP | JavaScript | ❌ |
| **Project Type** | WordPress Plugin | CLI Tool | ❌ |
| **Files Analyzed** | 9 | 1 | ❌ |
| **Total Classes** | 4 | 0 | ❌ |
| **Total Functions** | 15 | 0 | ❌ |
| **Lines of Code** | 507 | 0 | ❌ |

**Accuracy: 0/6 = 0%**

### Metadata Analysis (generation_info.json)

```json
{
  "project_name": "wp-project-guard",
  "version": "1.0.0",
  "language": "javascript",  // ❌ WRONG - Should be "php"
  "project_type": "cli_tool",  // ❌ WRONG - Should be "wordpress_plugin"
  "files_analyzed": 1,  // ❌ WRONG - Should be 9
  "total_classes": 0,  // ❌ WRONG - Should be 4
  "total_functions": 0,  // ❌ WRONG - Should be 15
  "lines_of_code": 0,  // ❌ WRONG - Should be 507
  "llm_provider": "ollama",  // ✅ CORRECT
  "model": "deepseek-coder:6.7b",  // ✅ CORRECT
  "generation_time": "24.30s"  // ✅ CORRECT
}
```

### Documentation Quality

**README.md Contents:**
- Generic CLI tool documentation
- No WordPress-specific information
- No PHP code examples
- No mention of plugin hooks/actions
- No class/function documentation
- Template-like content (demo data)

**Diagram Quality:**
- Generic component diagrams
- No real project structure
- Placeholder relationships
- No WordPress architecture
- Unable to find `.mmd` source files (only PNG/SVG outputs)

**Overall Quality:** ❌ **Completely generic/unusable** for actual project

---

## Root Cause Analysis

### Primary Issue: PHP Language Not Supported

**Investigation Steps:**

1. **Checked parser implementation:**
   ```bash
   cat backend/src/parser/ast_parser.py | head -100
   ```

2. **Findings:**
   - Only imports: `tree-sitter-python`, `tree-sitter-javascript`, `tree-sitter-typescript`
   - **NO `tree-sitter-php` import**
   - Parser dictionary only contains 3 languages:
   ```python
   self.parsers = {
       'python': Parser(Language(tspython.language())),
       'javascript': Parser(Language(tsjavascript.language())),
       'typescript': Parser(Language(tstypescript.language_typescript()))
   }
   # PHP MISSING
   ```

3. **Checked requirements.txt:**
   ```bash
   cat backend/requirements.txt
   ```
   - Contains: `tree-sitter-python`, `tree-sitter-javascript`, `tree-sitter-typescript`
   - **Missing: `tree-sitter-php`**

4. **Checked codebase analyzer:**
   ```bash
   cat backend/src/analyzer/codebase_analyzer.py | head -150
   ```
   - File detection logic exists
   - Language detection by extension exists
   - **PHP detection missing or fallback to JavaScript**

### Why Generic Documentation Generated

1. **No PHP Files Parsed:**
   - Extension skips all `.php` files (no parser available)
   - Falls back to empty/minimal data structure

2. **LLM Generates from Template:**
   - With 0 classes and 0 functions, LLM has no real data
   - Generates generic "CLI Tool" documentation
   - Creates placeholder diagrams

3. **Language Misdetection:**
   - Without PHP parser, analyzer guesses language
   - Falls back to "javascript" as default
   - Wrong project type classification

### Impact Assessment

**For WordPress Developers:**
- Extension completely unusable
- 0% accuracy in code analysis
- Generic documentation has no value
- Wasted time and resources

**For Other PHP Projects:**
- Laravel projects: Won't work
- Symfony projects: Won't work
- Drupal projects: Won't work
- Custom PHP applications: Won't work

**For Supported Languages (Python/JS/TS):**
- Extension should work correctly
- Not tested due to PHP project focus
- Requires separate testing

---

## Required Fixes

### Priority 1: Add PHP Language Support

**Changes Required:**

1. **backend/requirements.txt:**
   ```diff
   + tree-sitter-php>=0.21.0
   ```

2. **backend/src/parser/ast_parser.py:**
   ```python
   import tree_sitter_php as tsphp
   
   self.parsers = {
       'python': Parser(Language(tspython.language())),
       'javascript': Parser(Language(tsjavascript.language())),
       'typescript': Parser(Language(tstypescript.language_typescript())),
       'php': Parser(Language(tsphp.language()))  # ADD THIS
   }
   ```

3. **Add PHP query patterns:**
   - Class detection: `(class_declaration)` node
   - Function detection: `(function_definition)` node
   - Method detection: `(method_declaration)` node
   - Property detection: `(property_declaration)` node

4. **Add WordPress framework detection:**
   - Check for `wp-content/plugins/` path
   - Check for WordPress headers in main file
   - Detect hooks/filters/actions
   - Recognize WP class patterns

**Estimated Effort:** 4-6 hours

---

### Priority 2: Fix LLM_PROVIDER Default

**File:** `backend/src/pipeline.py` line 34

**Current:**
```python
llm_provider = os.getenv('LLM_PROVIDER', 'deepseek').lower()
```

**Fixed:**
```python
llm_provider = os.getenv('LLM_PROVIDER', 'ollama').lower()
```

**Rationale:**
- Ollama is local/free (default use case)
- DeepSeek API requires paid API key
- Consistent with `.env.example`
- Consistent with `client.py` default

**Estimated Effort:** 5 minutes

---

### Priority 3: Auto-Run Setup Wizard

**Issue:** Setup wizard requires manual invocation via Command Palette

**Required Changes:**

1. Verify `onStartupFinished` activation event works
2. Add explicit wizard auto-launch logic
3. Check for existing settings before showing wizard
4. Store "wizard_completed" flag to prevent re-showing

**Estimated Effort:** 1-2 hours

---

### Priority 4: Fix Escaped Newlines in UI

**Issue:** Dialogs show `\\n\\n` instead of actual line breaks

**Required Changes:**

1. Review all `vscode.window.showInformationMessage()` calls
2. Use template literals with actual newlines
3. Or use array of strings joined with `\n`
4. Test on macOS, Windows, Linux

**Estimated Effort:** 30 minutes

---

### Priority 5: Improve Documentation

**README.md Updates Needed:**

1. **Add "Supported Languages" section:**
   ```markdown
   ## Supported Languages
   
   Currently supported:
   - ✅ Python
   - ✅ JavaScript
   - ✅ TypeScript
   
   Coming soon:
   - ⏳ PHP
   - ⏳ Java
   - ⏳ C++
   - ⏳ Go
   ```

2. **Add prerequisites section:**
   - Ollama installation required
   - Supported LLM models
   - Python 3.8+ requirement (if running manually)

3. **Add troubleshooting section:**
   - Common errors and solutions
   - How to check Ollama status
   - How to run manual tests

**Estimated Effort:** 1 hour

---

## Additional Findings

### Working Components

1. **Ollama Integration:** ✅
   - Model detection works correctly
   - Communication with localhost:11434 successful
   - deepseek-coder:6.7b model loaded and responding

2. **Python Backend:** ✅
   - Flask server structure sound
   - Module imports working
   - Error handling present

3. **Documentation Pipeline:** ✅
   - Pipeline executes end-to-end
   - Output files generated correctly
   - JSON metadata structure valid

4. **Diagram Generation:** ✅
   - Mermaid to PNG/SVG conversion works
   - File outputs created successfully
   - Image quality acceptable

### Non-Critical Issues

1. **urllib3 OpenSSL Warning:**
   ```
   urllib3 v2 only supports OpenSSL 1.1.1+
   ```
   - **Impact:** Cosmetic only, doesn't affect functionality
   - **Cause:** macOS default LibreSSL 2.8.3
   - **Fix:** Not urgent, warning can be suppressed

2. **Missing .mmd Source Files:**
   - Only PNG/SVG outputs found in `diagrams/` folder
   - No `.mmd` (Mermaid) source files preserved
   - **Impact:** Cannot edit diagrams without regenerating
   - **Recommendation:** Save .mmd files alongside images

3. **No Progress Indicators:**
   - 24 second generation time with no feedback
   - User doesn't know if extension is working
   - **Recommendation:** Add progress notifications in VS Code

---

## Testing Verification Steps

### Commands Used to Verify Project Structure

```bash
# Count PHP files
find . -name "*.php" -type f | wc -l
# Result: 9 files

# Count lines of code
wc -l *.php includes/*.php public/*.php public/templates/*.php
# Result: 507 total lines

# Count classes
grep -r "class\s" --include="*.php" | wc -l
# Result: 4 classes

# Count functions
grep -r "function\s" --include="*.php" | wc -l
# Result: 15 functions

# List all PHP files
find . -name "*.php" -type f
# Result:
# ./wp-project-guard.php
# ./uninstall.php
# ./includes/class-admin-ui.php
# ./includes/class-settings.php
# ./includes/helpers.php
# ./public/class-guard.php
# ./public/templates/polite.php
# ./public/templates/standard.php
# ./public/templates/urgent.php
```

### Manual Test Command

```bash
# Navigate to extension
cd ~/.vscode/extensions/enghammadkhurshid.architector-llm-2.0.5

# Run with workaround
LLM_PROVIDER=ollama python3 architector.py \
  "/Users/hammadkhurshidchughtaii/Downloads/WP Project Gaurd/wp-project-guard" \
  "1.0.0" 2>&1 | tee /tmp/architector_full_output.log

# Check output
cat output/generation_info.json | jq '.'

# Verify diagrams
ls -la output/diagrams/
```

---

## Recommendations

### For Extension Developer

1. **Immediate Action Required:**
   - Fix LLM_PROVIDER default value (5 min fix)
   - Add PHP language support (4-6 hours)
   - Update documentation with language limitations (1 hour)

2. **Short-term Improvements:**
   - Auto-run setup wizard on first install
   - Fix escaped newlines in UI dialogs
   - Add progress indicators during generation
   - Save .mmd source files alongside images

3. **Long-term Roadmap:**
   - Add Java support (tree-sitter-java)
   - Add C++ support (tree-sitter-cpp)
   - Add Go support (tree-sitter-go)
   - Add Ruby support (tree-sitter-ruby)
   - Framework detection (WordPress, Laravel, Django, React, etc.)
   - Custom documentation templates per framework

4. **Testing Requirements:**
   - Test on actual Python/JavaScript/TypeScript projects
   - Verify quality on supported languages
   - Add integration tests for PHP once supported
   - Test on Windows/Linux (currently only macOS tested)

### For WordPress Plugin Users

1. **Current Status:**
   - ❌ **DO NOT USE** for PHP/WordPress projects
   - Extension will generate incorrect documentation
   - Wait for PHP support in future version

2. **Alternative Solutions:**
   - PHPDocumentor
   - phpDox
   - Sami
   - Manual documentation

3. **When to Retry:**
   - After developer releases version with PHP support
   - Check release notes for "tree-sitter-php" mention
   - Verify "Supported Languages" includes PHP

### For Python/JS/TS Users

1. **Worth Testing:**
   - Extension may work correctly for supported languages
   - Requires separate testing to verify
   - LLM_PROVIDER workaround needed until fixed

2. **Test Procedure:**
   - Manually invoke setup wizard: `Architector: Setup`
   - Select Ollama provider
   - Generate documentation
   - Verify accuracy of detected metrics
   - Check quality of generated docs

---

## Conclusion

The Architector-LLM extension shows **technical promise** but has **critical functionality gaps** that prevent production use on PHP/WordPress projects. The root cause is clear: **PHP language parser support is completely missing** from the backend infrastructure.

### Summary of Issues

| Issue | Severity | Impact | Fix Effort |
|-------|----------|--------|------------|
| No PHP Support | 🔴 Critical | Extension unusable for PHP | 4-6 hours |
| Wrong LLM_PROVIDER default | 🔴 Critical | Breaks Ollama users | 5 minutes |
| Setup wizard doesn't auto-run | 🟡 Medium | Poor UX | 1-2 hours |
| Escaped newlines in UI | 🟡 Medium | Confusing text | 30 minutes |
| Missing language docs | 🟡 Medium | User confusion | 1 hour |
| No progress indicators | 🟢 Low | UX polish | 2-3 hours |

### Test Result

**Status:** ❌ **FAILED** for WordPress/PHP projects  
**Blocking Issues:** 2 critical bugs  
**Recommendation:** **Wait for PHP support** before using on WordPress projects

### Next Steps

1. Share this report with extension developer
2. Monitor GitHub repository for PHP support updates
3. Re-test after next version release
4. Consider testing on Python/JS project separately
5. Evaluate alternative documentation tools for immediate needs

---

## Appendix

### Test Artifacts

**Location:** `/tmp/architector_full_output.log`  
**Size:** ~100 KB  
**Contains:**
- Complete terminal output
- LLM generation process
- Diagram rendering steps
- File write operations
- Timing information

### Extension Files Examined

```
~/.vscode/extensions/enghammadkhurshid.architector-llm-2.0.5/
├── backend/
│   ├── architector.py (main entry point)
│   ├── requirements.txt (dependencies)
│   ├── .env.example (config template)
│   └── src/
│       ├── pipeline.py (LINE 34 BUG)
│       ├── parser/
│       │   └── ast_parser.py (NO PHP PARSER)
│       ├── analyzer/
│       │   └── codebase_analyzer.py (language detection)
│       └── llm/
│           └── client.py (LLM interface)
└── out/
    └── extension.js (VS Code extension code)
```

### Generated Output Files

```
output/
├── README.md (2.1 KB, generic content)
├── diagrams/
│   ├── component.png (45 KB)
│   ├── component.svg (12 KB)
│   ├── c4_context.png (38 KB)
│   └── c4_context.svg (9 KB)
├── generation_info.json (487 bytes, incorrect metadata)
└── quality_report.json (1.2 KB, generic metrics)
```

### Environment Verification

```bash
# Python version
python3 --version
# Python 3.9.6

# Ollama status
curl -s http://localhost:11434/api/tags | jq '.models[] | select(.name | contains("deepseek"))'
# ✅ deepseek-coder:6.7b found

# Extension installed
ls ~/.vscode/extensions/ | grep architector
# enghammadkhurshid.architector-llm-2.0.5

# Tree-sitter modules
pip3 list | grep tree-sitter
# tree-sitter 0.23.2
# tree-sitter-javascript 0.23.5
# tree-sitter-python 0.23.6
# tree-sitter-typescript 0.23.2
# ❌ tree-sitter-php NOT FOUND
```

---

**Report End**

*For questions or updates, contact the tester or extension developer.*
