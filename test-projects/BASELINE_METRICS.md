# Baseline Metrics: Test Projects for Empirical Evaluation

**Date Generated:** January 24, 2026  
**Tool Used:** cloc v2.06  
**Total Projects:** 9 (3 languages × 3 sizes)

---

## Summary Table

| # | Project | Language | Size | Files | LOC (Code) | Blank | Comment | Total Lines |
|---|---------|----------|------|-------|------------|-------|---------|-------------|
| 1 | Flask-Login | Python | Small | 8 | 599 | 227 | 308 | 1,134 |
| 2 | Typer | Python | Medium | 16 | 3,981 | 542 | 567 | 5,090 |
| 3 | Celery | Python | Large | 156 | 26,726 | 7,538 | 7,728 | 41,992 |
| 4 | Day.js | JavaScript | Small | 184 | 8,031 | 827 | 210 | 9,068 |
| 5 | React Hook Form | TypeScript | Medium | 228 | 41,806 | 6,971 | 1,612 | 50,389 |
| 6 | NestJS | TypeScript | Large | 816 | 61,049 | 7,516 | 6,880 | 75,445 |
| 7 | PHP-DI | PHP | Small | 62 | 3,162 | 871 | 1,417 | 5,450 |
| 8 | Slim Framework | PHP | Medium | 72 | 3,133 | 970 | 1,710 | 5,813 |
| 9 | Laravel Framework | PHP | Large | 1,453 | 112,126 | 32,198 | 99,556 | 243,880 |

---

## Detailed Metrics by Language

### Python Projects

#### 1. Flask-Login (Small)
- **LOC:** 599
- **Files:** 8 Python files
- **Directory:** `test-projects/python/small-flask-login/src/`
- **Repository:** https://github.com/maxcountryman/flask-login
- **Description:** Flask extension for user session management
- **Expected Framework:** Flask extension
- **Expected Patterns:** Decorators, Mixins, Flask integration

#### 2. Typer (Medium)
- **LOC:** 3,981
- **Files:** 16 Python files
- **Directory:** `test-projects/python/medium-typer/typer/`
- **Repository:** https://github.com/tiangolo/typer
- **Description:** CLI application framework built on Click
- **Expected Framework:** Click-based CLI
- **Expected Patterns:** Type hints, Click decorators, CLI commands

#### 3. Celery (Large)
- **LOC:** 26,726
- **Files:** 156 Python files
- **Directory:** `test-projects/python/large-celery/celery/`
- **Repository:** https://github.com/celery/celery
- **Description:** Distributed task queue for Python
- **Expected Framework:** Standalone framework
- **Expected Patterns:** Worker patterns, Message queues, Distributed systems

---

### JavaScript/TypeScript Projects

#### 4. Day.js (Small)
- **LOC:** 8,031
- **Files:** 184 JavaScript files (includes plugins)
- **Directory:** `test-projects/javascript/small-dayjs/src/`
- **Repository:** https://github.com/iamkun/dayjs
- **Description:** Minimalist date library alternative to Moment.js
- **Expected Framework:** Vanilla JavaScript
- **Expected Patterns:** Plugin architecture, Immutable patterns

#### 5. React Hook Form (Medium)
- **LOC:** 41,806
- **Files:** 228 TypeScript files
- **Directory:** `test-projects/javascript/medium-react-hook-form/src/`
- **Repository:** https://github.com/react-hook-form/react-hook-form
- **Description:** Form validation library for React
- **Expected Framework:** React hooks
- **Expected Patterns:** Custom hooks, Context API, TypeScript generics

#### 6. NestJS (Large)
- **LOC:** 61,049
- **Files:** 816 TypeScript files
- **Directory:** `test-projects/javascript/large-nestjs/packages/`
- **Repository:** https://github.com/nestjs/nest
- **Description:** Progressive Node.js framework for building server-side applications
- **Expected Framework:** NestJS (Express/Fastify-based)
- **Expected Patterns:** Decorators, Dependency injection, Modules

---

### PHP Projects

#### 7. PHP-DI (Small)
- **LOC:** 3,162
- **Files:** 62 PHP files
- **Directory:** `test-projects/php/small-php-di/src/`
- **Repository:** https://github.com/PHP-DI/PHP-DI
- **Description:** Dependency injection container for PHP
- **Expected Framework:** Standalone DI container
- **Expected Patterns:** Dependency injection, Reflection, PSR-11

#### 8. Slim Framework (Medium)
- **LOC:** 3,133
- **Files:** 72 PHP files
- **Directory:** `test-projects/php/medium-slim/Slim/`
- **Repository:** https://github.com/slimphp/Slim
- **Description:** Micro-framework for building web applications
- **Expected Framework:** Slim (PSR-7 compliant)
- **Expected Patterns:** Middleware, Routing, PSR standards

#### 9. Laravel Framework (Large)
- **LOC:** 112,126 (PHP only)
- **Total LOC:** 118,262 (includes Blade, JSON, etc.)
- **Files:** 1,453 PHP files (1,574 total)
- **Directory:** `test-projects/php/large-laravel/src/`
- **Repository:** https://github.com/laravel/framework
- **Description:** Full-featured PHP web application framework
- **Expected Framework:** Laravel
- **Expected Patterns:** Facades, Service container, Eloquent ORM, Blade templates

---

## Size Category Analysis

### Small Projects (< 1,000 LOC target)
| Project | LOC | Files | Actual Category |
|---------|-----|-------|-----------------|
| Flask-Login | 599 | 8 | ✅ Small |
| Day.js | 8,031 | 184 | ⚠️ Medium (includes all plugins) |
| PHP-DI | 3,162 | 62 | ⚠️ Medium |

**Note:** Day.js and PHP-DI are larger than expected but still in the "small-medium" range.

### Medium Projects (1,000 - 5,000 LOC target)
| Project | LOC | Files | Actual Category |
|---------|-----|-------|-----------------|
| Typer | 3,981 | 16 | ✅ Medium |
| React Hook Form | 41,806 | 228 | ⚠️ Large |
| Slim | 3,133 | 72 | ✅ Medium |

**Note:** React Hook Form is much larger than expected (moved to "large" category).

### Large Projects (> 5,000 LOC target)
| Project | LOC | Files | Actual Category |
|---------|-----|-------|-----------------|
| Celery | 26,726 | 156 | ✅ Large |
| NestJS | 61,049 | 816 | ✅ Very Large |
| Laravel | 112,126 | 1,453 | ✅ Very Large |

---

## Revised Size Categories (Actual)

### Tier 1: Small (< 5,000 LOC)
1. Flask-Login: **599 LOC**
2. Typer: **3,981 LOC**
3. Slim: **3,133 LOC**
4. PHP-DI: **3,162 LOC**

### Tier 2: Medium (5,000 - 30,000 LOC)
5. Day.js: **8,031 LOC**
6. Celery: **26,726 LOC**

### Tier 3: Large (> 30,000 LOC)
7. React Hook Form: **41,806 LOC**
8. NestJS: **61,049 LOC**
9. Laravel: **112,126 LOC**

---

## Testing Order (Recommended)

### Phase 1: Small Projects (Quick Tests)
1. ✅ Flask-Login (599 LOC) - Fastest baseline
2. ✅ Typer (3,981 LOC) - Medium-small
3. ✅ Slim (3,133 LOC) - Medium-small

### Phase 2: Medium Projects
4. ✅ PHP-DI (3,162 LOC) - Test PHP OOP patterns
5. ✅ Day.js (8,031 LOC) - Test JavaScript plugin architecture
6. ✅ Celery (26,726 LOC) - Complex distributed system

### Phase 3: Large Projects (Stress Tests)
7. ✅ React Hook Form (41,806 LOC) - TypeScript complexity
8. ✅ NestJS (61,049 LOC) - Large-scale TypeScript framework
9. ✅ Laravel (112,126 LOC) - Ultimate stress test

---

## Expected Testing Time Estimates

Based on preliminary tests (WP Project Guard: 507 LOC in 18.2s):

| Project | LOC | Est. Time | Est. Memory | Risk Level |
|---------|-----|-----------|-------------|------------|
| Flask-Login | 599 | ~20s | Low | ✅ Low |
| Typer | 3,981 | ~2min | Low | ✅ Low |
| Slim | 3,133 | ~2min | Low | ✅ Low |
| PHP-DI | 3,162 | ~2min | Low | ✅ Low |
| Day.js | 8,031 | ~4min | Medium | ⚠️ Medium |
| Celery | 26,726 | ~12min | Medium | ⚠️ Medium |
| React Hook Form | 41,806 | ~18min | High | ⚠️ High |
| NestJS | 61,049 | ~25min | High | ⚠️ High |
| Laravel | 112,126 | ~45min | Very High | 🔴 Very High |

**Total Estimated Time:** ~2 hours (excluding Laravel)  
**With Laravel:** ~2.75 hours total

---

## Repository Paths

```
test-projects/
├── python/
│   ├── small-flask-login/      ✅ Cloned
│   ├── medium-typer/            ✅ Cloned
│   └── large-celery/            ✅ Cloned
├── javascript/
│   ├── small-dayjs/             ✅ Cloned
│   ├── medium-react-hook-form/  ✅ Cloned
│   └── large-nestjs/            ✅ Cloned
└── php/
    ├── small-php-di/            ✅ Cloned
    ├── medium-slim/             ✅ Cloned
    └── large-laravel/           ✅ Cloned
```

---

## Next Steps

1. ✅ **COMPLETED:** Clone all repositories
2. ✅ **COMPLETED:** Generate baseline metrics
3. **READY:** Begin testing with Flask-Login (smallest project)
4. **READY:** Generate test reports for each project
5. **TODO:** Aggregate data for research paper

---

**Status:** Ready to begin testing Phase 1  
**Recommended Start:** Flask-Login (599 LOC, ~20 seconds)
