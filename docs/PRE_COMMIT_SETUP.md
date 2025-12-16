# Pre-commit Hooks Setup Guide

This document explains how to set up and use pre-commit hooks for automated code quality checks before commits.

## What Are Pre-commit Hooks?

Pre-commit hooks automatically run code quality checks before you commit code. This prevents:
- Formatting issues
- Lint violations
- Security vulnerabilities
- Type errors
- Secrets being committed

**Benefits:**
- Catch issues before they reach CI/CD
- Consistent code style across team
- Prevent bad commits at the source
- Faster CI/CD pipeline (fewer failures)

---

## Installation

### 1. Install pre-commit Framework

```bash
pip install pre-commit
```

### 2. Install Git Hooks

In the repository root directory:

```bash
pre-commit install
```

This creates `.git/hooks/pre-commit` file that runs before each commit.

### 3. Verify Installation

```bash
pre-commit --version
pre-commit list-files
```

---

## Hook Categories

### Python Hooks

| Hook | Purpose | Config |
|------|---------|--------|
| **black** | Code formatting | 120-char line length |
| **isort** | Import organization | Black profile |
| **flake8** | Linting | E501/W503 ignored |
| **pylint** | Advanced linting | Missing docstring allowed |
| **mypy** | Type checking | Ignore missing imports |
| **bandit** | Security checks | Exclude tests/ |

### JavaScript/TypeScript Hooks

| Hook | Purpose | Config |
|------|---------|--------|
| **prettier** | Code formatting | 100-char line length |
| **eslint** | Linting | Angular config, auto-fix |

### Infrastructure Hooks

| Hook | Purpose | Config |
|------|---------|--------|
| **hadolint** | Dockerfile linting | Best practices |
| **yamllint** | YAML validation | 120-char lines |
| **sqlfluff** | SQL formatting | PostgreSQL dialect |

### Security Hooks

| Hook | Purpose | Config |
|------|---------|--------|
| **detect-secrets** | Find hardcoded secrets | Baseline mode |
| **bandit** | Python security | OWASP guidelines |

---

## Usage

### Run All Hooks on Staged Files

Hooks run automatically before commit. If they fail:

```bash
# Fix issues shown in error message
# Stage fixed files
git add .

# Try committing again
git commit -m "..."
```

### Run All Hooks on All Files

```bash
pre-commit run --all-files
```

### Run Specific Hook

```bash
pre-commit run black --all-files
pre-commit run eslint --all-files
```

### Bypass Hooks (Not Recommended)

```bash
git commit --no-verify
```

**⚠️ Only use for emergencies!**

---

## Common Issues

### Hook Fails: `black` wants to reformat code

**Error:**
```
Reformat with black
```

**Solution:**
```bash
# black automatically reformats - just stage and commit
git add .
git commit -m "..."
```

### Hook Fails: `isort` wants to reorganize imports

**Error:**
```
Import sorting issues found
```

**Solution:**
```bash
# isort automatically fixes - just stage and commit
git add .
git commit -m "..."
```

### Hook Fails: `pylint` or `flake8` violations

**Error:**
```
Line too long / Undefined variable
```

**Solution:**
```bash
# Fix violations manually
vim path/to/file.py

# Then stage and commit
git add .
git commit -m "..."
```

### Hook Fails: `mypy` type errors

**Error:**
```
error: Argument 1 to "foo" has incompatible type "str"; expected "int"
```

**Solution:**
```bash
# Fix type hints or variable usage
# Then stage and commit
git add .
git commit -m "..."
```

### Hook Fails: `detect-secrets` found a secret

**Error:**
```
Potential secrets detected
```

**Critical Solution:**
```bash
# NEVER commit secrets!
# 1. Remove secret from code
rm secret_value
# OR
# Use environment variable instead of hardcoding

# 2. If accidentally committed before hooks:
# See security incident procedure below

# 3. Stage fixed code and commit
git add .
git commit -m "Remove hardcoded secret"
```

### Multiple hooks fail

**Solution:** Fix them in order shown. Some hooks auto-fix (black, prettier, isort), others require manual fixes (pylint, mypy).

```bash
# Black auto-fixes formatting
git add .
git commit -m "..."  # Might fail again on next hook

# Keep fixing and re-committing until all pass
```

---

## Configuration

### Modify Hook Behavior

Edit `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/psf/black
  hooks:
    - id: black
      args: ['--line-length=120']  # Change here
```

Then reinstall:

```bash
pre-commit install
```

### Skip Specific Hook for a Commit

Edit `.pre-commit-config.yaml` and set:

```yaml
- repo: https://github.com/psf/black
  hooks:
    - id: black
      stages: []  # Disable this hook
```

Or use SKIP environment variable:

```bash
SKIP=black,pylint git commit -m "..."
```

---

## Team Best Practices

### 1. Commit Pre-commit Configuration

The `.pre-commit-config.yaml` should be version-controlled:

```bash
git add .pre-commit-config.yaml
git commit -m "Add pre-commit configuration"
```

### 2. Enforce on All Team Members

In team README or contributing guide:

```markdown
## Setup Development Environment

1. Clone repository
2. Install pre-commit:
   pip install pre-commit
   pre-commit install
3. Code will now be checked before each commit
```

### 3. CI/CD Validation

Optionally add pre-commit check to CI/CD:

```yaml
# .github/workflows/lint.yml
- name: Run pre-commit checks
  run: pre-commit run --all-files
```

### 4. Update Hooks Regularly

```bash
# Update all hooks to latest versions
pre-commit autoupdate

# Test changes
pre-commit run --all-files

# Commit if passing
git add .pre-commit-config.yaml
git commit -m "Update pre-commit hooks"
```

---

## Security: Secrets Management

### Detecting Secrets

The `detect-secrets` hook finds hardcoded API keys, passwords, etc.

**Never commit:**
```python
# ❌ BAD
API_KEY = "sk-abc123xyz"
DATABASE_URL = "postgres://user:password@host"
```

**Instead use:**
```python
# ✅ GOOD
import os
API_KEY = os.getenv("GROQ_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
```

### If You Accidentally Committed a Secret

1. **Immediately rotate the secret** (revoke old key, generate new)
2. **Remove from code** and commit fix
3. **Consider the repo compromised** (if public)
4. **Audit access logs** for unauthorized use

### Manage Baseline

The `.secrets.baseline` file tracks known secrets:

```bash
# If legitimate secret in code (very rare):
detect-secrets scan --update .secrets.baseline

# Review what was added:
git diff .secrets.baseline
```

---

## Performance

### Hooks Take Too Long?

Pre-commit caches results. First run is slow, subsequent runs are faster:

```bash
# Force rerun (skip cache)
pre-commit run --all-files --no-cache
```

### Which Hooks Are Slowest?

1. `mypy` (type checking) - 5-10s
2. `pylint` (advanced linting) - 3-5s
3. `bandit` (security scan) - 2-3s

**Tip:** These run only on modified files, so usually fast.

---

## Debugging

### See What Hooks Will Run

```bash
pre-commit run --dry-run
```

### Verbose Output

```bash
PRE_COMMIT_FROM_REF=origin/main PRE_COMMIT_TO_REF=HEAD pre-commit run --all-files --verbose
```

### Run Specific Hook with Debug

```bash
pre-commit run black --all-files --verbose
```

---

## References

- [pre-commit Framework](https://pre-commit.com/)
- [Available Hooks Registry](https://pre-commit.com/hooks.html)
- [Black Formatter](https://black.readthedocs.io/)
- [ESLint](https://eslint.org/)
- [Bandit Security](https://bandit.readthedocs.io/)
