# Architector-LLM: AI-Powered Architecture Documentation Generator

[![Version](https://img.shields.io/badge/version-2.0.3-blue.svg)](https://github.com/engrhammadkhurshid/architector-llm)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Research](https://img.shields.io/badge/research-NUST%20Pakistan-red.svg)](https://nust.edu.pk)

An intelligent VS Code extension that automatically generates professional software architecture documentation and diagrams from your codebase using Large Language Models (LLMs).

## 📖 Research Publication

**Paper Title:** *"From Code to Architecture: Leveraging LLMs for Automated Software Design Documentation"*

**Authors:** Engr. Hammad Khurshid  
**Institution:** National University of Sciences and Technology (NUST), Pakistan  
**Year:** 2026  
**Status:** Under Review

**Abstract:** This research explores the application of Large Language Models in automating the generation of software architecture documentation. The proposed system combines Abstract Syntax Tree (AST) parsing, dependency graph analysis, and Retrieval-Augmented Generation (RAG) to produce comprehensive, multi-diagram architecture documentation with minimal human intervention.

## 🎯 Overview

Architector-LLM is a research-backed VS Code extension that transforms codebases into professional architecture documentation. It supports multiple programming languages and generates 6 types of architectural diagrams.

### Key Features

✅ **Multi-LLM Provider Support**
- Local: Ollama (deepseek-coder:6.7b)
- Cloud APIs: DeepSeek, OpenAI GPT-4, Anthropic Claude

✅ **Auto-Detection & Smart Setup**
- Automatically detects installed Ollama
- One-click setup wizard
- Secure API key management (VS Code Secrets API)

✅ **Comprehensive Documentation**
- 6 diagram types: Architecture, Component, Class, Activity, Data Flow, C4 Context
- Interactive HTML documentation
- Version tracking with Git integration
- Quality scoring and validation

✅ **Research-Grade Analytics** (Optional)
- GDPR-compliant data collection
- Usage metrics for empirical research
- Performance benchmarks
- Quality assessment data

## 🚀 Quick Start

### Installation

```bash
# Install from VSIX (local testing)
code --install-extension architector-llm-2.0.3.vsix

# Or from VS Code Marketplace (coming soon)
# Search for "Architector-LLM" by Engr. Hammad Khurshid
```

### First Run

1. **Setup Wizard** appears automatically
2. **Choose LLM Provider:**
   - If Ollama detected: "✅ Ready to use!"
   - Or select cloud API (DeepSeek recommended)
3. **Optional:** Participate in research (anonymous analytics)
4. **Done!** Click "Architector" in status bar to generate docs

### Requirements

- **VS Code:** 1.85.0 or higher
- **Python:** 3.9+ (installed automatically with extension)
- **LLM Option 1 (Local):** Ollama + deepseek-coder:6.7b (~3.8GB)
- **LLM Option 2 (Cloud):** API key from DeepSeek/OpenAI/Claude

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [QUICKSTART_V2.md](QUICKSTART_V2.md) | Quick start guide for users |
| [OLLAMA_AUTO_DETECTION.md](OLLAMA_AUTO_DETECTION.md) | Auto-detection feature guide |
| [V2_IMPLEMENTATION_COMPLETE.md](V2_IMPLEMENTATION_COMPLETE.md) | Complete feature documentation |
| [PRIVACY_POLICY.md](PRIVACY_POLICY.md) | GDPR-compliant privacy policy |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Technical architecture |
| [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) | For contributors |

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│           VS Code Extension (TypeScript)                │
│  ┌────────────┐  ┌──────────────┐  ┌────────────────┐ │
│  │ Setup      │  │ API Key      │  │ Analytics      │ │
│  │ Wizard     │  │ Manager      │  │ Integration    │ │
│  └────────────┘  └──────────────┘  └────────────────┘ │
└───────────────────────────┬─────────────────────────────┘
                            │ Python subprocess
                            ↓
┌─────────────────────────────────────────────────────────┐
│               Python Backend (pipeline.py)              │
│  ┌────────────┐  ┌──────────────┐  ┌────────────────┐ │
│  │ AST Parser │→ │ LLM Client   │→ │ Diagram        │ │
│  │ (Tree-sit) │  │ (Multi-prov) │  │ Renderer       │ │
│  └────────────┘  └──────────────┘  └────────────────┘ │
│  ┌────────────┐  ┌──────────────┐  ┌────────────────┐ │
│  │ Dependency │  │ Quality      │  │ Interactive    │ │
│  │ Graph      │  │ Validation   │  │ Docs (HTML)    │ │
│  └────────────┘  └──────────────┘  └────────────────┘ │
└─────────────────────────────────────────────────────────┘
                            │
                            ↓
             📂 docs/arch/v{version}_{timestamp}/
```

## 🧪 Research Context

### Motivation
Manual architecture documentation is time-consuming and often becomes outdated. This research investigates whether LLMs can automate this process while maintaining quality and accuracy.

### Methodology
1. **Code Analysis:** AST parsing + dependency graph construction
2. **RAG Pipeline:** Inject codebase context into LLM prompts
3. **Multi-Diagram Generation:** 6 architectural views generated
4. **Quality Validation:** Automated consistency and completeness checks
5. **Empirical Evaluation:** User studies + quality metrics

### Data Collection (Optional with Consent)
- Developer demographics (name, email, experience level)
- Project metadata (language, type, size)
- Generation performance (time, quality scores)
- Success/failure rates
- Anonymous usage patterns

**Privacy:** GDPR-compliant, fully transparent, opt-in only, data deletion on request.

## 📊 Generated Artifacts

Each documentation generation creates:

```
docs/arch/v1.0.0_2026-01-23-034500_abc123f/
├── README.md                    # Main documentation
├── INDEX.md                     # Interactive navigation
├── RELATIONSHIPS.md             # Component relationships
├── QUALITY_REPORT.md           # Quality metrics
├── COMPARISONS.md              # Version comparisons
├── diagrams/
│   ├── architecture.png/svg    # System architecture
│   ├── component.png/svg       # Component diagram
│   ├── class.png/svg           # Class diagram
│   ├── activity.png/svg        # Activity diagram
│   ├── data_flow.png/svg       # Data flow diagram
│   └── c4_context.png/svg      # C4 context diagram
└── metadata/
    └── generation_info.json    # Metrics and metadata
```

## 🎓 Academic Use

If you use Architector-LLM in your research, please cite:

```bibtex
@inproceedings{khurshid2026architector,
  title={From Code to Architecture: Leveraging LLMs for Automated Software Design Documentation},
  author={Khurshid, Hammad},
  booktitle={Under Review},
  year={2026},
  organization={National University of Sciences and Technology (NUST), Pakistan}
}
```

## 👨‍💻 Developer Information

**Developer:** Engr. Hammad Khurshid  
**Email:** engr.hammadkhurshid@gmail.com  
**GitHub:** [@engrhammadkhurshid](https://github.com/engrhammadkhurshid)  
**Institution:** National University of Sciences and Technology (NUST), Pakistan  
**Research Area:** Software Engineering, AI/ML, Automated Documentation

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

Copyright (c) 2026 Engr. Hammad Khurshid

## 🤝 Contributing

Contributions are welcome! Please read [DEVELOPMENT.md](docs/DEVELOPMENT.md) first.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Bug Reports & Feature Requests

- **Issues:** https://github.com/engrhammadkhurshid/architector-llm/issues
- **Discussions:** https://github.com/engrhammadkhurshid/architector-llm/discussions
- **Email:** engr.hammadkhurshid@gmail.com

## 🌟 Acknowledgments

- **NUST Pakistan** for research support
- **DeepSeek** for LLM API access
- **Ollama** for local LLM infrastructure
- **VS Code Extension API** for development framework
- **Tree-sitter** for code parsing
- **Mermaid** for diagram rendering

## 📈 Project Status

- ✅ **v2.0.3:** Complete with multi-provider support and analytics
- 🚀 **Next:** VS Code Marketplace publication
- 📝 **Future:** Support for more languages, advanced diagram types

---

**⭐ Star this repository if you find it useful for your research or development work!**
