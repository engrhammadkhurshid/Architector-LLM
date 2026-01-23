# Architector-LLM v2.0.7 - Supported Languages & Features

## 🌍 Universal Language Support (All Included by Default)

### All 11 Languages Fully Supported Out-of-the-Box

✅ **Python** (.py, .pyw)
- Full AST parsing with tree-sitter-python
- Classes, functions, methods, imports
- Frameworks: Django, Flask, FastAPI, Streamlit

✅ **JavaScript** (.js, .jsx, .mjs, .cjs)
- ES6+ support
- Classes, functions, imports, exports
- Frameworks: React, Vue, Express, Next.js

✅ **TypeScript** (.ts, .tsx)
- Full type system support
- Interfaces, classes, generics
- Frameworks: NestJS, Angular, Next.js

✅ **PHP** (.php, .phtml, .php3-5)
- WordPress plugin/theme detection
- Classes, methods, functions, namespaces
- Frameworks: WordPress, Laravel, Symfony

✅ **Java** (.java)
- Classes, methods, imports
- Frameworks: Spring Boot, Jakarta EE, Hibernate
- Maven (pom.xml) support

✅ **C** (.c, .h)
- Structures, functions
- CMake support

✅ **C++** (.cpp, .cc, .cxx, .hpp, .hh, .hxx)
- Classes, templates, functions
- CMake support

✅ **C#** (.cs)
- Classes, methods, namespaces
- Frameworks: ASP.NET Core, Entity Framework
- .csproj project file support

✅ **Go** (.go)
- Structs, functions, packages
- Frameworks: Gin, Echo, Fiber
- go.mod support

✅ **Rust** (.rs)
- Structs, traits, enums, functions
- Cargo.toml support

✅ **Ruby** (.rb, .rake)
- Classes, methods, modules
- Frameworks: Rails, Sinatra
- Gemspec support

## 📦 Automatic Version Detection

The extension automatically detects project version from:

### Node.js / JavaScript / TypeScript
- `package.json` → `version` field

### Python
- `pyproject.toml` → `[project]` or `[tool.poetry]` sections
- `setup.py` → `version=` parameter
- `setup.cfg` → `[metadata] version`
- `__init__.py` → `__version__` variable

### PHP
- `composer.json` → `version` field
- WordPress plugin headers → `Version:` field
- WordPress theme `style.css` → `Version:` field

### Java
- `pom.xml` (Maven) → `<version>` tag
- `build.gradle` (Gradle) → `version =` property

### C# / .NET
- `*.csproj` → `<Version>` or `<VersionPrefix>` tag
- `Directory.Build.props` → `<Version>` tag

### Rust
- `Cargo.toml` → `[package] version`

### C/C++
- `CMakeLists.txt` → `project(... VERSION ...)`
- `configure.ac` → `AC_INIT(..., version)`

### Generic
- `VERSION`, `version.txt`, `.version` files

## 🎯 Framework Detection

### Python Frameworks
- Django (settings.py, manage.py, wsgi.py)
- Flask (Flask(), app.run())
- FastAPI (@app.get, FastAPI())
- Streamlit (st.)
- SQLAlchemy (declarative_base, Column)
- Celery (@app.task)

### JavaScript/TypeScript Frameworks
- React (useState, useEffect, jsx)
- Vue (v-if, v-for, .vue files)
- Angular (@Component, @NgModule)
- Express (app.listen, express())
- NestJS (@Controller, @Injectable)
- Next.js (getStaticProps, getServerSideProps)
- Gatsby (gatsby-config)
- Nuxt (nuxt.config)
- Svelte (.svelte files)

### PHP Frameworks
- WordPress (wp_enqueue, add_action, add_filter)
- Laravel (Illuminate\\, artisan)
- Symfony (Symfony\\, bin/console)
- CodeIgniter (CodeIgniter\\, system/core)

### Java Frameworks
- Spring Boot (@SpringBootApplication)
- Spring (@RestController, @Service)
- Hibernate (@Entity, @Table)

### C# Frameworks
- ASP.NET Core (Microsoft.AspNetCore)
- Entity Framework (DbContext)

### Go Frameworks
- Gin (gin.Default)
- Echo (echo.New)
- Fiber (fiber.New)

### Ruby Frameworks
- Rails (ActionController, ActiveRecord)
- Sinatra

## 🏗️ Project Type Detection

The extension intelligently detects:
- **WordPress Plugin** - PHP with Plugin Name header
- **WordPress Theme** - PHP with Theme Name header
- **Web API** - REST/GraphQL endpoints detected
- **Web Application** - Full-stack web frameworks
- **Frontend Application** - React/Vue/Angular apps
- **Desktop Application** - C#/Java/C++ without web APIs
- **CLI Tool** - Small projects (<10 files)
- **Library/Package** - No deployment configs
- **Microservice** - Docker/Kubernetes configs

## 🚀 Installation & Usage

### Quick Start

1. **Install Extension**
   ```bash
   code --install-extension architector-llm-2.0.7.vsix
   ```

2. **All Language Parsers Included** ✅
   - No additional installation needed!
   - All 11 languages work out-of-the-box
   - Python, JavaScript, TypeScript, PHP, Java, C, C++, C#, Go, Rust, Ruby

3. **Generate Documentation**
   - Open your project in VS Code
   - Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
   - Run: "Architector: Generate Documentation"
   - Leave version empty for auto-detection or enter manually

### Version Auto-Detection

When prompted for version:
- **Leave empty** → Automatically detects from project files
- **Enter manually** → Use custom version (e.g., 2.0.7)

### LLM Configuration

Supported LLM providers:
- **Ollama** (local, free) - Default
- **DeepSeek API** (cloud, paid)
- **OpenAI API** (cloud, paid)
- **Claude API** (cloud, paid)

Configure via Setup Wizard or `.env` file.

## 📊 Output Structure

```
architector_docs/
├── v2.0.7/                    # Version-aligned with your project
│   ├── README.md              # Main documentation
│   ├── ARCHITECTURE.md        # Architecture overview
│   ├── QUALITY_REPORT.md      # Quality metrics
│   ├── diagrams/
│   │   ├── class_diagram.md
│   │   ├── sequence_diagram.md
│   │   ├── component_diagram.md
│   │   └── ...
│   └── interactive/
│       └── index.html         # Interactive documentation
```

## 🔧 Troubleshooting

### All Languages Supported by Default

No additional setup needed! All 11 languages are included:
- ✅ Python, JavaScript, TypeScript, PHP
- ✅ Java, C, C++, C#
- ✅ Go, Rust, Ruby

If you encounter issues, verify the extension installed correctly:
```bash
code --list-extensions | grep architector
```

### Version Not Detected?

Ensure you have a supported version file:
- Node.js: `package.json`
- Python: `pyproject.toml`, `setup.py`, or `setup.cfg`
- PHP: `composer.json`
- Java: `pom.xml` or `build.gradle`
- And more...

Or manually enter version when prompted.

## 📈 Quality Metrics

The extension validates generated diagrams for:
- **Syntax** - Valid Mermaid syntax
- **Completeness** - All entities represented
- **Clarity** - Readable and well-structured
- **Accuracy** - Matches codebase structure

Generates quality reports with scores and recommendations.

## 🎓 Research Project

Part of ongoing research at NUST Pakistan on "From Code to Architecture: Leveraging LLMs for Automated Software Design Documentation"

## 📝 License

Research project - See LICENSE file for details.

---

**Version:** 2.0.7  
**Release Date:** January 23, 2026  
**Changelog:**
- ✨ Added support for 11+ programming languages
- 🔍 Automatic version detection from 20+ project file types
- 🌐 Enhanced framework detection (30+ frameworks)
- 🏗️ Improved project type classification
- 📦 Version alignment between project and documentation
- 🐛 Fixed LLM_PROVIDER default bug (ollama)
- 🎯 WordPress plugin/theme detection
