**Language:** English | [简体中文](README.zh-CN.md)

# Odoo Claude Code

[![Stars](https://img.shields.io/github/stars/echozen88/odoo-claude-code?style=flat)](https://github.com/echozen88/odoo-claude-code/stargazers)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white)
![Shell](https://img.shields.io/badge/-Shell-4EAA25?logo=gnu-bash&logoColor=white)

---

<div align="center">

**🌐 Language / 语言**

[**English**](README.md) | [简体中文](README.zh-CN.md)

</div>

---

**Claude Code plugin specialized for Odoo 19 development.**

Production-ready agents, skills, hooks, commands, and rules tailored specifically for the Odoo ERP framework.

---

## What's Different

This plugin adapts the powerful `everything-claude-code` workflows specifically for Odoo 19 development:

### Odoo-Specific Features
- **Odoo 19 Planning**: Module structure, model/view/controller planning
- **Odoo ORM Guidance**: Field types, relationships, computed fields
- **Odoo Security**: Access rights, record rules, SQL injection prevention
- **Odoo Testing**: TransactionCase, HttpCase, security tests
- **Odoo Views**: Tree, Form, Kanban, Pivot, QWeb templates

### Orchestration Workflow
```
/orchestrate feature "Add new sales report module"

Executes:
planner (Odoo 19) → tdd-guide (Odoo testing) →
code-reviewer (Odoo style) → security-reviewer (Odoo security) →
odoo-reviewer (Odoo framework)
```

---

## Quick Start

### Step 1: Install Plugin

```bash
# Add marketplace
/plugin marketplace add echozen88/odoo-claude-code

# Install plugin
/plugin install odoo-claude-code@odoo-claude-code
```

### Step 2: Install Rules (Required)

> ⚠️ **Important:** Claude Code plugins cannot distribute `rules` automatically. Install them manually:

```bash
# Clone the repo first
git clone https://github.com/echozen88/odoo-claude-code.git

# Copy rules (applies to all projects)
cp -r odoo-claude-code/rules/* ~/.claude/rules/

# Or project level rules (applicable only to the current project)
mkdir -p .claude/rules
cp -r odoo-claude-code/rules/* .claude/rules/

```

### Step 3: Start Using

```bash
# Try orchestrate command
/orchestrate feature "Add a new Odoo module with custom fields"

# Plan an Odoo feature
/plan "Create a wizard for bulk order processing"

# TDD workflow for Odoo
/tdd "Implement Odoo model with constraints"

# Code review
/code-review

# Security review
/security-review
```

---

## What's Inside

```
odoo-claude-code/
|-- .claude-plugin/   # Plugin and marketplace manifests
|   |-- plugin.json         # Plugin metadata and component paths
|   |-- marketplace.json    # Marketplace catalog
|
|-- agents/           # Odoo 19 specialized subagents
|   |-- planner.md           # Odoo feature implementation planning
|   |-- tdd-guide.md         # Odoo test-driven development
|   |-- code-reviewer.md     # Odoo code quality review
|   |-- security-reviewer.md  # Odoo security review
|   |-- odoo-reviewer.md     # Odoo framework compliance review
|
|-- skills/           # Odoo domain knowledge
|   |-- odoo-patterns/       # Odoo module structure & conventions
|   |-- odoo-orm/           # ORM usage & best practices
|   |-- odoo-views/         # Views, QWeb, templates
|   |-- odoo-security/      # Security patterns for Odoo
|
|-- commands/         # Odoo-specific commands
|   |-- orchestrate.md       # Orchestration workflow
|
|-- rules/            # Odoo coding standards
|   |-- odoo-coding-style.md    # PEP8, naming, organization
|   |-- odoo-security.md        # Access rights, record rules
|   |-- odoo-testing.md         # Testing requirements & patterns
|   |-- odoo-api.md            # API development rules
|
|-- hooks/            # Odoo-specific automations
|   |-- hooks.json                # PreToolUse, PostToolUse, Stop hooks
```

---

## Orchestration Workflow

The `/orchestrate` command provides complete development workflows for Odoo 19:

### Feature Workflow
```
planner → tdd-guide → code-reviewer → security-reviewer → odoo-reviewer
```
- Plans Odoo module structure
- Writes tests first (TDD)
- Reviews for Odoo coding standards
- Security audit (access rights, record rules)
- Framework compliance check

### Bugfix Workflow
```
explorer → tdd-guide → code-reviewer → odoo-reviewer
```
- Investigates Odoo bugs
- Fixes with tests
- Reviews changes

### Security Workflow
```
security-reviewer → code-reviewer → odoo-reviewer → architect
```
- Focused security review
- OWASP Top 10 for Odoo
- Access control verification

---

## Odoo 19 Features Covered

### Module Structure
- `__manifest__.py` configuration
- Model, view, controller organization
- Security groups and record rules

### Model Development
- Field types (Char, Text, Many2one, One2many, etc.)
- Computed fields with `@api.depends`
- Onchange methods
- Constraints
- Inheritance patterns

### Views
- Tree views with decorations and buttons
- Form views with notebooks and sheets
- Kanban views
- Pivot and Graph views
- QWeb templates

### Security
- Access rights (ir.model.access.csv)
- Record rules (ir.rule)
- CSRF protection
- SQL injection prevention
- XSS prevention in QWeb

### Testing
- TransactionCase for model tests
- HttpCase for controller tests
- Security test patterns

---

## Requirements

### Claude Code CLI Version

**Minimum version: v2.1.0 or later**

Check your version:
```bash
claude --version
```

---

## Installation

### Option 1: Install as Plugin (Recommended)

```bash
# Add this repo as a marketplace
/plugin marketplace add echozen88/odoo-claude-code

# Install the plugin
/plugin install odoo-claude-code@odoo-claude-code
```

Or add directly to your `~/.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "odoo-claude-code": {
      "source": {
        "source": "github",
        "repo": "echozen88/odoo-claude-code"
      }
    }
  },
  "enabledPlugins": {
    "odoo-claude-code@odoo-claude-code": true
  }
}
```

This gives you instant access to all commands, agents, skills, and hooks.

> **Note:** The Claude Code plugin system does not support distributing `rules` via plugins ([upstream limitation](https://code.claude.com/docs/en/plugins-reference)). You need to install rules manually:
>
> ```bash
> # Clone the repo first
> git clone https://github.com/echozen88/odoo-claude-code.git
>
> # Option A: User-level rules (applies to all projects)
> cp -r odoo-claude-code/rules/* ~/.claude/rules/
>
>
> # Option B: Project-level rules (applies to current project only)
> mkdir -p .claude/rules
> cp -r odoo-claude-code/rules/* .claude/rules/
> ```

---

### Option 2: Manual Installation

If you prefer manual control over what's installed:

```bash
# Clone the repo
git clone https://github.com/echozen88/odoo-claude-code.git

# Copy agents to your Claude config
cp odoo-claude-code/agents/*.md ~/.claude/agents/

# Copy rules (REQUIRED)
cp odoo-claude-code/rules/*.md ~/.claude/rules/

# Copy commands
cp odoo-claude-code/commands/*.md ~/.claude/commands/

# Copy skills
cp -r odoo-claude-code/skills/* ~/.claude/skills/

# Copy hooks (optional, in plugin.json)
# hooks are auto-loaded from hooks/hooks.json
```

#### Add hooks to settings.json
Copy the hooks from `hooks/hooks.json` to your `~/.claude/settings.json`.

#### Configure MCPs
Copy desired MCP servers from `mcp-configs/mcp-servers.json` to your `~/.claude.json`.

**Important:** Replace `YOUR_*_HERE` placeholders with your actual API keys.

---

## Key Concepts

### Agents

Subagents handle delegated tasks with limited scope. Example:
```markdown
---
name: code-reviewer
description: Reviews code for quality, security, and maintainability
tools: ["Read", "Grep", "Glob", "Bash"]
model: opus
---

You are a senior code reviewer...
```

### Skills

Skills are workflow definitions invoked by commands or agents:
```markdown
# TDD Workflow

1. Define interfaces first
2. Write failing tests (RED)
3. Implement minimal code (GREEN)
4. Refactor (IMPROVE)
5. Verify 80%+ coverage
```

### Hooks

Hooks fire on tool events. Example - warn about console.log:
```json
{
  "matcher": "tool == \"Edit\" && tool_input.file_path matches \"\\\\.(ts|tsx|js|jsx)$\"",
  "hooks": [{
    "type": "command",
    "command": "#!/bin/bash\ngrep -n 'console\\.log' \"$file_path\" && echo '[Hook] Remove console.log' >&2"
  }]
}
```

### Rules

Rules are always-follow guidelines. Keep them modular:
```
~/.claude/rules/
  security.md      # No hardcoded secrets
  coding-style.md  # Immutability, file organization
  testing.md       # TDD, 80% coverage requirement
```

---

## Agent Descriptions

### planner (Odoo 19)
Expert planning specialist for Odoo modules. Creates implementation plans with:
- Model definitions and inheritance
- View requirements
- Security setup (groups, access rights, record rules)
- Data migration considerations

### tdd-guide (Odoo 19)
Test-driven development specialist for Odoo:
- TransactionCase patterns for model tests
- HttpCase patterns for controller tests
- Security test patterns
- 80%+ coverage requirement

### code-reviewer (Odoo 19)
Code quality reviewer with Odoo-specific checks:
- PEP8 compliance
- API decorator usage
- Field definitions
- View structure

### security-reviewer (Odoo 19)
Security specialist for Odoo applications:
- Access rights verification
- Record rule analysis
- SQL injection prevention
- XSS prevention in QWeb
- CSRF protection

### odoo-reviewer (Odoo 19)
Framework compliance specialist:
- Manifest configuration
- Module structure
- Inheritance patterns
- Odoo conventions

---

## Skills Available

### odoo-patterns
Module structure, naming conventions, view patterns

### odoo-orm
Field types, relationships, search/write operations, computed fields

### odoo-views
Tree, form, kanban, pivot views, QWeb templates

### odoo-security
Access rights, record rules, controller security

---

## Commands Available

| Command | Description |
|---------|-------------|
| `/orchestrate feature` | Full Odoo feature workflow |
| `/orchestrate bugfix` | Odoo bug investigation workflow |
| `/orchestrate security` | Odoo security review workflow |
| `/plan` | Create Odoo implementation plan |
| `/tdd` | Odoo test-driven development |
| `/code-review` | Odoo code quality review |
| `/security-review` | Odoo security review |

---

## Usage Examples

### Planning an Odoo Module

```
/plan "Create a new sales order line with custom fields"
```

Output includes:
- Model structure with field definitions
- Required views (tree, form, kanban)
- Security groups and access rights
- Record rules for multi-user data
- Migration considerations

### Implementing with TDD

```
/tdd "Implement sales order model with validation"
```

Workflow:
1. Write failing tests first
2. Implement to pass tests
3. Refactor code
4. Verify 80%+ coverage

### Orchestrate Feature

```
/orchestrate feature "Add approval workflow to purchase orders"
```

Complete workflow execution:
1. **Planner**: Creates implementation plan
2. **TDD Guide**: Writes tests, implements
3. **Code Reviewer**: Reviews for quality
4. **Security Reviewer**: Audits security
5. **Odoo Reviewer**: Framework compliance
6. **Final Report**: Summary and recommendations

---

## Odoo 19 Quick Reference

### Module Naming
- Format: `my_module_name`
- Model format: `module.model_name`

### Field Naming
- Many2one: `name_id`
- One2many: `line_ids`
- Many2many: `tag_ids`

### Common Dependencies
- `base` - Core Odoo models
- `web` - Frontend framework
- `mail` - Messaging
- `sale` - Sales orders
- `purchase` - Purchase orders

### API Decorators

```python
@api.model           # Model-level method
@api.depends(*fields)  # Computed field
@api.onchange(*fields)  # Onchange handler
@api.constrains(*fields)  # Constraint validation
```

---

## Contributing

**Contributions are welcome!**

If you have:
- Odoo-specific patterns
- Better security rules
- Additional testing strategies
- Framework-specific improvements

Please contribute!

---

## Links

- **Based on**: [Everything Claude Code](https://github.com/affaan-m/everything-claude-code)
- **Odoo 19 Documentation**: https://www.odoo.com/documentation/17.0/
- **Odoo Developer Forum**: https://www.odoo.com/forum

---

## License

MIT - Use freely, modify as needed, contribute back if you can.

---

**Star this repo if it helps. Happy Odoo development!**
