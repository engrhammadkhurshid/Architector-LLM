# Empirical Testing Plan: Architector-LLM Prototype Evaluation

**Research Study:** "From Code to Architecture: Leveraging LLMs for Automated Software Design Documentation"  
**Researcher:** Engr. Hammad Khurshid, NUST Pakistan  
**Date:** January 24, 2026

---

## Testing Objectives

### Primary Goals
1. **Validate multi-language support** across Python, JavaScript/TypeScript, and PHP
2. **Measure performance scalability** across small, medium, and large codebases
3. **Evaluate documentation quality** for different project complexities
4. **Assess framework detection accuracy** for popular frameworks
5. **Generate empirical evidence** for research paper publication

### Metrics to Collect
- **Performance Metrics:**
  - Generation time (seconds)
  - Lines of code analyzed
  - Files processed
  - Memory usage

- **Quality Metrics:**
  - Documentation quality score (0-100)
  - Diagrams generated (count & types)
  - Classes/Functions detected
  - Framework detection accuracy
  - Architecture pattern recognition

- **Accuracy Metrics:**
  - Language detection accuracy
  - Version auto-detection success rate
  - Project type classification accuracy
  - Completeness score

---

## Testing Matrix: 3 Languages × 3 Sizes = 9 Projects

### Category 1: Python Projects

#### 1.1 Small Python Project (< 1,000 LOC)
**Project:** Flask-Login  
**Repository:** https://github.com/maxcountryman/flask-login  
**Size:** ~800 LOC  
**Type:** Authentication library for Flask  
**Framework:** Flask extension  
**Why Selected:**
- ✅ Well-documented existing project for comparison
- ✅ Single responsibility (authentication)
- ✅ Popular Flask extension (7.5k+ stars)
- ✅ Clear architecture with decorators and mixins
- ✅ Representative of library-style Python projects

**Expected Challenges:**
- Decorator-heavy code
- Mixin patterns
- Flask integration points

---

#### 1.2 Medium Python Project (1,000 - 5,000 LOC)
**Project:** Typer  
**Repository:** https://github.com/tiangolo/typer  
**Size:** ~3,200 LOC  
**Type:** CLI application framework  
**Framework:** Click-based CLI framework  
**Why Selected:**
- ✅ Modern Python CLI framework
- ✅ Type hints throughout
- ✅ Rich documentation for comparison
- ✅ Multiple modules with clear separation
- ✅ Uses Click under the hood (dependency detection test)

**Expected Challenges:**
- CLI-specific patterns
- Type annotation complexity
- Multiple decorator patterns
- Testing framework integration

---

#### 1.3 Large Python Project (> 5,000 LOC)
**Project:** Celery  
**Repository:** https://github.com/celery/celery  
**Size:** ~45,000 LOC  
**Type:** Distributed task queue  
**Framework:** Standalone framework with Django/Flask integration  
**Why Selected:**
- ✅ Industry-standard task queue
- ✅ Complex distributed architecture
- ✅ Multi-backend support (Redis, RabbitMQ)
- ✅ Integration with Django and Flask
- ✅ Real-world enterprise complexity

**Expected Challenges:**
- Large codebase complexity
- Multiple backend adapters
- Distributed system patterns
- Long generation time (stress test)
- Memory management

---

### Category 2: JavaScript/TypeScript Projects

#### 2.1 Small JavaScript Project (< 1,000 LOC)
**Project:** Day.js  
**Repository:** https://github.com/iamkun/dayjs  
**Size:** ~800 LOC  
**Type:** Date manipulation library  
**Framework:** Vanilla JavaScript (ES6+)  
**Why Selected:**
- ✅ Simple, focused utility library
- ✅ Plugin architecture
- ✅ Immutable design pattern
- ✅ 46k+ stars (widely used)
- ✅ Modern JavaScript features

**Expected Challenges:**
- Plugin system detection
- Immutability patterns
- Minimal OOP structure

---

#### 2.2 Medium TypeScript Project (1,000 - 5,000 LOC)
**Project:** React Hook Form  
**Repository:** https://github.com/react-hook-form/react-hook-form  
**Size:** ~4,500 LOC  
**Type:** Form validation library for React  
**Framework:** React hooks-based library  
**Why Selected:**
- ✅ Modern React patterns (hooks)
- ✅ TypeScript with advanced generics
- ✅ Performance-optimized architecture
- ✅ 40k+ stars
- ✅ Real-world React integration

**Expected Challenges:**
- React hooks patterns
- TypeScript generics complexity
- Context API usage
- Performance optimization patterns

---

#### 2.3 Large TypeScript Project (> 5,000 LOC)
**Project:** NestJS  
**Repository:** https://github.com/nestjs/nest  
**Size:** ~50,000 LOC  
**Type:** Progressive Node.js framework  
**Framework:** Express/Fastify-based (Angular-inspired)  
**Why Selected:**
- ✅ Full-featured backend framework
- ✅ Decorator-based architecture
- ✅ Microservices support
- ✅ 66k+ stars (industry standard)
- ✅ Complex module system

**Expected Challenges:**
- Massive codebase
- Decorator metadata
- Dependency injection patterns
- Module federation
- Long generation time

---

### Category 3: PHP Projects

#### 3.1 Small PHP Project (< 1,000 LOC)
**Project:** PHP-DI (Container component)  
**Repository:** https://github.com/PHP-DI/PHP-DI  
**Size:** ~900 LOC (container core)  
**Type:** Dependency injection container  
**Framework:** Standalone DI container  
**Why Selected:**
- ✅ Clean OOP architecture
- ✅ PSR-11 compliant
- ✅ Reflection-heavy code
- ✅ Popular DI solution (1.2k+ stars)
- ✅ Modern PHP 8+ features

**Expected Challenges:**
- Reflection API usage
- Container patterns
- PSR interface detection

---

#### 3.2 Medium PHP Project (1,000 - 5,000 LOC)
**Project:** Slim Framework  
**Repository:** https://github.com/slimphp/Slim  
**Size:** ~3,800 LOC  
**Type:** Micro-framework for PHP  
**Framework:** PSR-7 compliant micro-framework  
**Why Selected:**
- ✅ Popular micro-framework (11.9k+ stars)
- ✅ Modern PHP architecture
- ✅ PSR standards throughout
- ✅ Middleware pattern
- ✅ Routing system

**Expected Challenges:**
- PSR-7/PSR-15 interfaces
- Middleware chains
- Routing pattern detection

---

#### 3.3 Large PHP Project (> 5,000 LOC)
**Project:** Laravel Framework (Core)  
**Repository:** https://github.com/laravel/framework  
**Size:** ~200,000 LOC  
**Type:** Full-stack web framework  
**Framework:** Laravel (most popular PHP framework)  
**Why Selected:**
- ✅ Industry-leading PHP framework
- ✅ Comprehensive feature set
- ✅ Facade pattern
- ✅ Service container
- ✅ Ultimate stress test for large codebases

**Expected Challenges:**
- Extremely large codebase
- Complex architecture patterns
- Facade and service container
- Very long generation time
- High memory usage

---

## Testing Protocol

### Phase 1: Environment Setup (Day 1)
1. Clone all 9 repositories
2. Create project structure:
   ```
   test-projects/
   ├── python/
   │   ├── small-flask-login/
   │   ├── medium-typer/
   │   └── large-celery/
   ├── javascript/
   │   ├── small-dayjs/
   │   ├── medium-react-hook-form/
   │   └── large-nestjs/
   └── php/
       ├── small-php-di/
       ├── medium-slim/
       └── large-laravel/
   ```
3. Document baseline metrics for each project
4. Verify extension setup with v2.1.0

### Phase 2: Testing Execution (Days 2-3)
For each project, execute the following:

1. **Pre-Documentation Analysis:**
   - Count LOC: `cloc <project-dir>`
   - List files: `find . -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.php"`
   - Identify expected framework
   - Document actual version

2. **Documentation Generation:**
   - Open project in VS Code
   - Run Architector extension
   - Record start timestamp
   - Monitor resource usage
   - Record completion timestamp
   - Capture all output logs

3. **Post-Documentation Analysis:**
   - Verify generated documentation files
   - Count diagrams generated
   - Review quality score
   - Check detected framework
   - Validate version detection
   - Compare with manual analysis

4. **Data Collection:**
   - Screenshot results
   - Export analytics data
   - Save generation logs
   - Document any errors/warnings

### Phase 3: Data Analysis (Day 4)

#### Quantitative Analysis
- Calculate average generation time per LOC
- Measure scalability (time vs. codebase size)
- Compare quality scores across sizes
- Analyze success rates by language

#### Qualitative Analysis
- Review documentation accuracy
- Assess architecture diagram correctness
- Evaluate framework detection accuracy
- Compare with existing documentation

#### Statistical Analysis
- Generate graphs: Time vs. LOC
- Create comparison tables
- Calculate correlation coefficients
- Identify performance bottlenecks

---

## Report Template for Each Project

```markdown
# Architector-LLM Test Report: [Project Name]

**Project:** [Name]
**Repository:** [URL]
**Language:** [Python/JavaScript/PHP]
**Size Category:** [Small/Medium/Large]
**Date:** [YYYY-MM-DD]
**Extension Version:** 2.1.0

## Project Metrics

### Codebase Statistics
- **Total Lines of Code:** [X]
- **Number of Files:** [X]
- **Number of Classes:** [X]
- **Number of Functions:** [X]
- **Actual Framework:** [Framework Name]
- **Actual Version:** [X.Y.Z]

### Generation Metrics
- **Generation Time:** [X.X seconds]
- **Files Analyzed:** [X/X]
- **Classes Detected:** [X/X]
- **Functions Detected:** [X/X]
- **Framework Detected:** [Name] (✅/❌)
- **Version Detected:** [X.Y.Z] (✅/❌)

### Quality Metrics
- **Documentation Quality Score:** [X/100]
- **Diagrams Generated:** [X]
  - Component Diagram: [✅/❌]
  - Class Diagram: [✅/❌]
  - Sequence Diagram: [✅/❌]
  - Package Diagram: [✅/❌]
- **Completeness:** [X%]
- **Accuracy:** [X%]

## Results

### ✅ Successes
- [List successful aspects]

### ⚠️ Limitations
- [List limitations found]

### ❌ Issues
- [List any errors or problems]

## Documentation Quality Assessment

### Architecture Understanding
- [Rating 1-5] How well did it understand the architecture?
- [Comments]

### Pattern Recognition
- [List patterns correctly identified]
- [List patterns missed]

### Code Structure Analysis
- [Rating 1-5] Accuracy of structure analysis
- [Comments]

## Comparison with Existing Documentation

### Similarities
- [What matched existing docs]

### Differences
- [What was different or novel]

### Added Value
- [What new insights were provided]

## Performance Analysis

### Resource Usage
- **Peak Memory:** [X MB]
- **CPU Usage:** [X%]
- **Disk I/O:** [X MB]

### Scalability Assessment
- **LOC per Second:** [X]
- **Estimated Time for 10k LOC:** [X seconds]
- **Bottlenecks Identified:** [List]

## Recommendations

### For This Project Type
- [Specific recommendations]

### For Extension Improvement
- [Improvement suggestions]

---

**Tester:** Hammad Khurshid Chughtaii
**Test Environment:** macOS, VS Code [version], Python [version], Node.js [version], PHP [version]
```

---

## Data Aggregation for Research Paper

### Table 1: Performance Comparison Across Projects

| Project | Language | LOC | Files | Time (s) | LOC/s | Quality | Diagrams |
|---------|----------|-----|-------|----------|-------|---------|----------|
| Flask-Login | Python | 800 | 12 | X | X | X/100 | X |
| Typer | Python | 3200 | 45 | X | X | X/100 | X |
| Celery | Python | 45000 | 300+ | X | X | X/100 | X |
| Day.js | JS | 800 | 8 | X | X | X/100 | X |
| React Hook Form | TS | 4500 | 60 | X | X | X/100 | X |
| NestJS | TS | 50000 | 400+ | X | X | X/100 | X |
| PHP-DI | PHP | 900 | 15 | X | X | X/100 | X |
| Slim | PHP | 3800 | 50 | X | X | X/100 | X |
| Laravel | PHP | 200000 | 1000+ | X | X | X/100 | X |

### Table 2: Detection Accuracy

| Project | Language Detected | Framework Detected | Version Detected | Patterns Found |
|---------|-------------------|-------------------|------------------|----------------|
| ... | ✅/❌ | ✅/❌ | ✅/❌ | X/Y |

### Table 3: Scalability Analysis

| Size Category | Avg LOC | Avg Time (s) | Avg Quality | Success Rate |
|---------------|---------|--------------|-------------|--------------|
| Small (<1k) | X | X | X/100 | X% |
| Medium (1-5k) | X | X | X/100 | X% |
| Large (>5k) | X | X | X/100 | X% |

---

## Research Paper Sections

### 5. Empirical Evaluation

#### 5.1 Experimental Setup
- 9 open-source projects across 3 languages
- 3 size categories per language
- Architector-LLM v2.1.0
- Hardware: [specs]
- LLM: Ollama DeepSeek-Coder

#### 5.2 Research Questions
**RQ1:** How does Architector-LLM scale with codebase size?  
**RQ2:** What is the accuracy of multi-language support?  
**RQ3:** How does documentation quality compare across project types?  
**RQ4:** What are the performance limitations?

#### 5.3 Results
[Present Tables 1-3 with analysis]

#### 5.4 Discussion
[Interpret findings, compare with existing approaches]

#### 5.5 Threats to Validity
- Selection bias (popular projects)
- Limited language coverage
- Single LLM model tested
- Subjective quality assessment

---

## Timeline

- **Day 1 (Jan 24):** Clone repos, setup testing environment
- **Day 2 (Jan 25):** Test Python projects (3)
- **Day 3 (Jan 26):** Test JavaScript/TypeScript projects (3)
- **Day 4 (Jan 27):** Test PHP projects (3)
- **Day 5 (Jan 28):** Data analysis and report compilation
- **Day 6 (Jan 29):** Results review and paper writing

---

## Tools Needed

1. **cloc** - Count lines of code
   ```bash
   brew install cloc
   ```

2. **hyperfine** - Benchmark tool (optional)
   ```bash
   brew install hyperfine
   ```

3. **time** - Measure execution time
   ```bash
   # Built-in Unix command
   time command
   ```

4. **htop/Activity Monitor** - Monitor resources
   ```bash
   brew install htop
   ```

---

## Expected Deliverables

1. ✅ 9 detailed test reports (one per project)
2. ✅ Aggregated data tables for research paper
3. ✅ Performance graphs and visualizations
4. ✅ Comparison analysis document
5. ✅ Recommendations for tool improvement
6. ✅ Research paper draft sections 5.1-5.5

---

## Alternative Projects (Backup Options)

### Python Alternatives
- **Small:** Colorama, Click, python-dotenv
- **Medium:** Sanic, FastAPI-Users, SQLModel
- **Large:** Django, Airflow, Scikit-learn

### JavaScript/TypeScript Alternatives
- **Small:** Chalk, Commander.js, Lodash
- **Medium:** Express.js, Fastify, Socket.IO
- **Large:** Vue.js, Angular, Electron

### PHP Alternatives
- **Small:** Carbon, Guzzle, Monolog
- **Medium:** Symfony Components, Doctrine ORM
- **Large:** Symfony, Magento, WordPress

---

**Status:** Ready to Begin Testing  
**Next Steps:** Clone repositories and begin Phase 1
