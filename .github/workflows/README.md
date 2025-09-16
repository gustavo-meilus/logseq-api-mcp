# GitHub Actions Workflows

This directory contains the consolidated GitHub Actions workflows for the logseq-api-mcp project.

## 🎯 **Workflow Structure**

### **1. `ci.yml` - Main CI Pipeline**

**Triggers:** Push to main/develop, Pull requests to main/develop

**Purpose:** Core continuous integration with comprehensive testing

- **Multi-version testing:** Python 3.11, 3.12, 3.13
- **Code quality:** Ruff linting and formatting
- **Testing:** Full test suite with 80%+ coverage requirement
- **MCP validation:** Server health and tool discovery
- **Build testing:** Package building and installation (PR only)

### **2. `quality.yml` - Advanced Quality & Security**

**Triggers:** Pull requests, Daily schedule (3 AM UTC), Manual dispatch

**Purpose:** Advanced code quality, security, and performance checks

- **Type checking:** MyPy static analysis
- **Security scanning:** Bandit security linter
- **Dependency checks:** Safety vulnerability scanning
- **Code analysis:** TODO/FIXME detection, secret scanning
- **Performance testing:** Memory usage validation (scheduled only)

### **3. `release.yml` - Release & Cross-Platform Testing**

**Triggers:** Release events, Weekly schedule (Sunday 2 AM UTC), Manual dispatch

**Purpose:** Comprehensive testing for releases and cross-platform compatibility

- **Cross-platform testing:** Ubuntu, Windows, macOS
- **Multi-version testing:** Python 3.11, 3.12, 3.13
- **Package building:** Distribution package creation
- **Integration testing:** MCP server with real tools
- **Tool validation:** All tool functions testing

## 📊 **Workflow Comparison**

| Feature                | ci.yml           | quality.yml | release.yml            |
| ---------------------- | ---------------- | ----------- | ---------------------- |
| **Frequency**          | Every push/PR    | PR + Daily  | Release + Weekly       |
| **Python Versions**    | 3.11, 3.12, 3.13 | 3.12        | 3.11, 3.12, 3.13       |
| **Operating Systems**  | Ubuntu           | Ubuntu      | Ubuntu, Windows, macOS |
| **Basic Testing**      | ✅               | ❌          | ✅                     |
| **Coverage Analysis**  | ✅               | ❌          | ✅                     |
| **Linting/Formatting** | ✅               | ❌          | ❌                     |
| **Type Checking**      | ❌               | ✅          | ❌                     |
| **Security Scanning**  | ❌               | ✅          | ❌                     |
| **Dependency Checks**  | ❌               | ✅          | ❌                     |
| **Package Building**   | ✅ (PR only)     | ❌          | ✅                     |
| **Cross-Platform**     | ❌               | ❌          | ✅                     |

## 🚀 **Benefits of Consolidation**

### **Before (5 workflows):**

- ❌ **Massive duplication** of tasks
- ❌ **Redundant CI runs** (same tests multiple times)
- ❌ **Higher GitHub Actions costs**
- ❌ **Complex maintenance** (5 files to update)
- ❌ **Unclear purpose** for each workflow

### **After (3 workflows):**

- ✅ **Focused purpose** for each workflow
- ✅ **Eliminated duplication** of tasks
- ✅ **Reduced CI time** and costs
- ✅ **Easier maintenance** (3 files to update)
- ✅ **Clear separation** of concerns
- ✅ **Better resource utilization**

## 🔧 **Workflow Triggers**

### **Main CI (`ci.yml`)**

```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
```

### **Quality & Security (`quality.yml`)**

```yaml
on:
  pull_request:
    branches: [main, develop]
  schedule:
    - cron: "0 3 * * *" # Daily at 3 AM UTC
  workflow_dispatch:
```

### **Release & Cross-Platform (`release.yml`)**

```yaml
on:
  release:
    types: [published]
  schedule:
    - cron: "0 2 * * 0" # Weekly on Sunday at 2 AM UTC
  workflow_dispatch:
```

## 📈 **Coverage Requirements**

- **Main CI:** 80% minimum coverage
- **Release Testing:** 85% minimum coverage
- **Quality Checks:** No coverage requirement (focuses on code quality)

## 🛡️ **Security Features**

- **Bandit security scanning** for common vulnerabilities
- **Dependency vulnerability checks** with Safety
- **Hardcoded secret detection**
- **License compliance checking**

## 📦 **Artifacts Generated**

- **Coverage reports** (HTML, XML)
- **Security reports** (Bandit JSON)
- **Dependency reports** (Safety, Licenses)
- **Package artifacts** (Wheels, distributions)
- **Test results** (Cross-platform)

## 🔄 **Migration Notes**

The old workflows have been backed up to `.github/workflows/backup/`:

- `test.yml` → Consolidated into `ci.yml`
- `comprehensive-test.yml` → Consolidated into `release.yml`
- `pr-validation.yml` → Consolidated into `ci.yml` and `quality.yml`
- Original `quality.yml` → Enhanced and streamlined

## 🎉 **Result**

**Reduced from 5 workflows to 3 workflows** with:

- **Eliminated duplication** of 80% of tasks
- **Maintained all functionality** with better organization
- **Improved efficiency** and reduced CI costs
- **Clearer separation** of concerns
