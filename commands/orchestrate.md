# Orchestrate Command (Odoo 19)

Sequential agent workflow for complex Odoo 19 development tasks.

## ⚠️ CRITICAL EXECUTION RULES - MUST FOLLOW

**NEVER SKIP ANY AGENT IN THE WORKFLOW.** Each agent has a specific purpose and MUST be executed in order.

### Mandatory Execution Protocol

1. **NO SHORTCUTS**: You MUST invoke EVERY agent listed in the workflow type
2. **SEQUENTIAL ONLY**: Execute agents one at a time, in the exact order specified
3. **WAIT FOR COMPLETION**: Wait for each agent to complete before starting the next
4. **VERIFY OUTPUT**: Check each agent produced a valid HANDOFF document before proceeding
5. **NO MERGING**: Do NOT combine multiple agent roles into one invocation

### Pre-Execution Checklist

Before starting, CREATE a task list:
```
□ Agent 1: [name] - PENDING
□ Agent 2: [name] - PENDING
□ Agent 3: [name] - PENDING
□ Agent 4: [name] - PENDING
□ Agent 5: [name] - PENDING
```

Update status after each agent completes. ALL MUST BE COMPLETED.

### Forbidden Actions

- ❌ "Skip planner, go straight to implementation"
- ❌ "Combine code-reviewer and security-reviewer"
- ❌ "Omit odoo-reviewer to save time"
- ❌ "Run agents out of order"
- ❌ "Skip handoff document creation"

## Usage

`/orchestrate [workflow-type] [task-description]`

## Workflow Types

### feature
Full Odoo 19 feature implementation workflow:
```
Step 1: planner → Step 2: tdd-guide → Step 3: code-reviewer → Step 4: security-reviewer → Step 5: odoo-reviewer
```

**ALL 5 AGENTS ARE MANDATORY - NO EXCEPTIONS**

### bugfix
Odoo bug investigation and fix workflow:
```
Step 1: explorer → Step 2: tdd-guide → Step 3: code-reviewer → Step 4: odoo-reviewer
```

**ALL 4 AGENTS ARE MANDATORY - NO EXCEPTIONS**

### refactor
Safe Odoo code refactoring workflow:
```
Step 1: architect → Step 2: code-reviewer → Step 3: tdd-guide → Step 4: odoo-reviewer
```

**ALL 4 AGENTS ARE MANDATORY - NO EXCEPTIONS**

### security
Odoo security-focused review:
```
Step 1: security-reviewer → Step 2: code-reviewer → Step 3: odoo-reviewer → Step 4: architect
```

**ALL 4 AGENTS ARE MANDATORY - NO EXCEPTIONS**

### performance
Odoo performance optimization workflow:
```
Step 1: performance-agent → Step 2: planner → Step 3: code-reviewer → Step 4: odoo-reviewer
```

**ALL 4 AGENTS ARE MANDATORY - NO EXCEPTIONS**

### migration
Odoo version migration workflow:
```
Step 1: migration-agent → Step 2: code-reviewer → Step 3: odoo-reviewer → Step 4: security-reviewer
```

**ALL 4 AGENTS ARE MANDATORY - NO EXCEPTIONS**

## Execution Pattern

For each agent in the workflow:

1. **Mark agent as IN_PROGRESS** in your checklist
2. **Invoke agent** with context from previous agent (or original task for first agent)
3. **WAIT for agent completion** - do NOT proceed until agent finishes
4. **Verify HANDOFF document** was created
5. **Mark agent as COMPLETED** in your checklist
6. **Move to next agent** only after verification
7. **Repeat** until ALL agents in workflow are completed
8. **Generate final report** only after ALL agents completed

## Handoff Document Format

**CRITICAL**: Each agent MUST produce a handoff document. Without it, DO NOT proceed to next agent.

### Required Handoff Structure

```markdown
## HANDOFF: [previous-agent] -> [next-agent]

### Completion Status: ✅ COMPLETE

### Context
[Summary of what was done]

### Findings
[Key discoveries or decisions]

### Files Modified
[List of files touched]

### Odoo-Specific Context
[Odoo models, views, controllers mentioned]

### Open Questions
[Unresolved items for next agent]

### Recommendations
[Suggested next steps]

---
### CHECKPOINT VERIFICATION
□ Agent completed all assigned tasks
□ Handoff document created
□ Files listed are accurate
□ Next agent has sufficient context
```

### Handoff Validation Checklist

Before moving to next agent, verify:

- [ ] Handoff contains "Completion Status: ✅ COMPLETE"
- [ ] All required sections are present
- [ ] Files Modified list is accurate
- [ ] Next agent can understand context
- [ ] No blocking issues unresolved

If ANY item fails, RE-INVOKE the current agent.

## Example: Odoo Feature Workflow

```
/orchestrate feature "Add a new sales report with custom fields"
```

### Pre-Execution: Create Task Checklist

```
□ Step 1: planner - PENDING
□ Step 2: tdd-guide - PENDING
□ Step 3: code-reviewer - PENDING
□ Step 4: security-reviewer - PENDING
□ Step 5: odoo-reviewer - PENDING
```

### Step-by-Step Execution

**STEP 1/5: Invoke Planner Agent**
```
□ Mark planner as IN_PROGRESS
□ Invoke planner agent with task description
□ WAIT for completion
□ Verify HANDOFF: planner -> tdd-guide exists
□ Verify handoff has "Completion Status: ✅ COMPLETE"
□ Mark planner as COMPLETED
□ Proceed to Step 2
```

**STEP 2/5: Invoke TDD Guide Agent**
```
□ Mark tdd-guide as IN_PROGRESS
□ Invoke tdd-guide agent with HANDOFF from planner
□ WAIT for completion
□ Verify HANDOFF: tdd-guide -> code-reviewer exists
□ Verify handoff has "Completion Status: ✅ COMPLETE"
□ Mark tdd-guide as COMPLETED
□ Proceed to Step 3
```

**STEP 3/5: Invoke Code Reviewer Agent**
```
□ Mark code-reviewer as IN_PROGRESS
□ Invoke code-reviewer agent with HANDOFF from tdd-guide
□ WAIT for completion
□ Verify HANDOFF: code-reviewer -> security-reviewer exists
□ Verify handoff has "Completion Status: ✅ COMPLETE"
□ Mark code-reviewer as COMPLETED
□ Proceed to Step 4
```

**STEP 4/5: Invoke Security Reviewer Agent**
```
□ Mark security-reviewer as IN_PROGRESS
□ Invoke security-reviewer agent with HANDOFF from code-reviewer
□ WAIT for completion
□ Verify HANDOFF: security-reviewer -> odoo-reviewer exists
□ Verify handoff has "Completion Status: ✅ COMPLETE"
□ Mark security-reviewer as COMPLETED
□ Proceed to Step 5
```

**STEP 5/5: Invoke Odoo Reviewer Agent**
```
□ Mark odoo-reviewer as IN_PROGRESS
□ Invoke odoo-reviewer agent with HANDOFF from security-reviewer
□ WAIT for completion
□ Verify final report exists
□ Verify report includes all agent outputs
□ Mark odoo-reviewer as COMPLETED
```

### Final Checklist Verification

```
✓ Step 1: planner - COMPLETED
✓ Step 2: tdd-guide - COMPLETED
✓ Step 3: code-reviewer - COMPLETED
✓ Step 4: security-reviewer - COMPLETED
✓ Step 5: odoo-reviewer - COMPLETED

ALL 5 AGENTS COMPLETED - WORKFLOW COMPLETE
```

### What Each Agent Does

1. **Planner Agent** (Odoo 19 specialist)
   - Analyzes requirements for Odoo 19
   - Creates implementation plan including:
     - Model structure (new model or inheritance)
     - Field definitions (types, constraints)
     - Security requirements (access rights, record rules)
     - View definitions (tree, form, pivot, graph)
     - Controller routes if needed
   - **Must produce**: `HANDOFF: planner -> tdd-guide`

2. **TDD Guide Agent** (Odoo testing specialist)
   - Reads planner handoff with Odoo context
   - Writes Odoo tests first (TransactionCase, HttpCase)
   - Tests include:
     - Model method tests
     - Security tests (access rights, record rules)
     - Controller tests
     - View rendering tests
   - Implements to pass tests
   - Output: `HANDOFF: tdd-guide -> code-reviewer`

3. **Code Reviewer Agent** (Odoo code quality specialist)
   - Reviews Odoo implementation
   - Checks for:
     - PEP8 compliance
     - Odoo coding standards
     - API decorator usage
     - Error handling
   - Output: `HANDOFF: code-reviewer -> security-reviewer`

4. **Security Reviewer Agent** (Odoo security specialist)
   - Security audit for Odoo application
   - Checks for:
     - SQL injection risks (ORM vs raw SQL)
     - Access control issues (ir.model.access, ir.rule)
     - Unauthorized sudo() usage
     - Missing CSRF protection
     - XSS in QWeb templates
   - Output: `HANDOFF: security-reviewer -> odoo-reviewer`

5. **Odoo Reviewer Agent** (Odoo framework specialist)
   - Framework compliance check
   - Validates:
     - Module structure
     - Manifest configuration
     - Inheritance patterns
     - Field definitions
     - View structure
     - API usage
   - Output: Final Report

## Final Report Format

```markdown
# ODOO 19 ORCHESTRATION REPORT
# ================================

Workflow: feature
Task: Add a new sales report with custom fields
Agents: planner -> tdd-guide -> code-reviewer -> security-reviewer -> odoo-reviewer

SUMMARY
-------
[One paragraph summary of the Odoo feature implementation]

IMPLEMENTATION PHASES
---------------------
Phase 1: Module Setup
- __manifest__.py configured with dependencies
- Directory structure created following Odoo conventions

Phase 2: Models
- New model(s) created with proper fields
- Computed fields with @api.depends
- Constraints defined

Phase 3: Security
- Access rights defined in ir.model.access.csv
- Record rules for multi-user data
- Security groups created

Phase 4: Views
- Tree view created
- Form view created
- Pivot/Graph views for reporting
- Menu items configured

Phase 5: Controllers
- HTTP routes defined with proper auth
- Input validation implemented
- CSRF protection where needed

AGENT OUTPUTS
-------------
Planner:
- Created detailed implementation plan
- Identified 3 Odoo dependencies: sale, web, mail
- Planned 2 models: sale.report.line, sale.report.summary

TDD Guide:
- Wrote 15 tests covering all model methods
- Tests include security scenarios
- Achieved 85% code coverage

Code Reviewer:
- PEP8 compliant
- All public methods have docstrings
- 3 minor suggestions for improvement

Security Reviewer:
- No SQL injection risks
- Access rights properly configured
- Record rules prevent data leakage
- CSRF protection on POST routes

Odoo Reviewer:
- Module structure follows Odoo 19 conventions
- API decorators used correctly
- View inheritance patterns correct
- Manifest properly configured

FILES CHANGED
--------------
__manifest__.py
models/sale_report.py
security/ir.model.access.csv
security/security.xml
views/sale_report_views.xml
views/menu.xml
controllers/report_controller.py
tests/test_sale_report.py
tests/test_security.py

TEST RESULTS
------------
- Model tests: 12 passed, 0 failed
- Security tests: 3 passed, 0 failed
- HTTP tests: 2 passed, 0 failed
- Coverage: 85.3%

ODOO SECURITY STATUS
-------------------
- Access Rights: ✓ Configured
- Record Rules: ✓ Configured
- SQL Injection: ✓ Safe (ORM used)
- CSRF Protection: ✓ Enabled
- sudo() Usage: ✓ Minimal and justified
- Input Validation: ✓ Implemented

FRAMEWORK COMPLIANCE
--------------------
- Module Structure: ✓ Compliant
- Manifest: ✓ Correct
- API Decorators: ✓ Used appropriately
- Field Definitions: ✓ Proper
- View Structure: ✓ Correct
- Inheritance: ✓ Patterns correct

RECOMMENDATION
--------------
✓ READY TO DEPLOY

Next Steps:
1. Test module in Odoo development environment
2. Run full test suite with `--test-enable`
3. Verify security rules in multi-user scenario
4. Create user documentation
5. Prepare upgrade script for existing installations

NOTES
-----
- Model uses inheritance from sale.order for easy integration
- Pivot view requires JavaScript widget for custom aggregation
- Consider adding caching for report generation performance
```

## Example: Performance Workflow

```
/orchestrate performance "Optimize slow report generation"
```

### Task Checklist
```
□ Step 1: performance-agent - PENDING
□ Step 2: planner - PENDING
□ Step 3: code-reviewer - PENDING
□ Step 4: odoo-reviewer - PENDING
```

### Execution Steps (Must complete ALL 4)

1. **Performance Agent** → Verify HANDOFF → **Planner Agent**
2. **Planner Agent** → Verify HANDOFF → **Code Reviewer Agent**
3. **Code Reviewer Agent** → Verify HANDOFF → **Odoo Reviewer Agent**
4. **Odoo Reviewer Agent** → Verify Final Report → **COMPLETE**

## Example: Migration Workflow

```
/orchestrate migration "17.0" "19.0"
```

### Task Checklist
```
□ Step 1: migration-agent - PENDING
□ Step 2: code-reviewer - PENDING
□ Step 3: odoo-reviewer - PENDING
□ Step 4: security-reviewer - PENDING
```

### Execution Steps (Must complete ALL 4)

1. **Migration Agent** → Verify HANDOFF → **Code Reviewer Agent**
2. **Code Reviewer Agent** → Verify HANDOFF → **Odoo Reviewer Agent**
3. **Odoo Reviewer Agent** → Verify HANDOFF → **Security Reviewer Agent**
4. **Security Reviewer Agent** → Verify Final Report → **COMPLETE**

2. **Code Reviewer Agent**
   - Reviews migrated code
   - Checks for correct API usage
   - Output: `HANDOFF: code-reviewer -> odoo-reviewer`

3. **Odoo Reviewer Agent**
   - Framework compliance check for new version
   - Verifies manifest format
   - Output: `HANDOFF: odoo-reviewer -> security-reviewer`

4. **Security Reviewer Agent**
   - Security audit for migrated code
   - Output: Final Report

## Odoo 19 Specific Considerations

### When Planning Odoo Features

1. **Module Dependencies**: Consider which Odoo modules to inherit from
2. **Multi-Company**: Plan for multi-company support if needed
3. **Multi-Currency**: Ensure proper currency handling
4. **Translation**: All user-facing strings must be translatable
5. **Security**: Always plan access rights and record rules

### When Writing Odoo Tests

1. **Test Tags**: Use `@tagged('post_install', '-at_install')` for tests needing data
2. **TransactionCase**: For model and security tests
3. **HttpCase**: For controller and UI tests
4. **Security Tests**: Always test access rights and record rules
5. **Demo Data**: Use demo data for realistic test scenarios

### When Reviewing Odoo Code

1. **PEP8**: Run `pylint --py3k` on all Python files
2. **API Usage**: Verify correct @api decorators
3. **Security**: Check for unauthorized sudo() and missing access rights
4. **Framework**: Ensure Odoo conventions are followed

## Parallel Execution

⚠️ **DO NOT USE PARALLEL EXECUTION UNLESS EXPLICITLY REQUESTED**

Parallel execution risks:
- Skipping workflow steps
- Missing handoff documents
- Incomplete agent outputs
- Difficult to debug failures

**Default to SEQUENTIAL execution always.**

## Arguments

$ARGUMENTS:
- `feature <description>` - Full Odoo feature workflow (5 agents REQUIRED)
- `bugfix <description>` - Odoo bug fix workflow (4 agents REQUIRED)
- `refactor <description>` - Odoo refactoring workflow (4 agents REQUIRED)
- `security <description>` - Odoo security review workflow (4 agents REQUIRED)
- `performance <description>` - Odoo performance optimization workflow (4 agents REQUIRED)
- `migration <from-version> <to-version>` - Odoo version migration workflow (4 agents REQUIRED)
- `custom <agents> <description>` - Custom agent sequence

## Custom Workflow Example

```
/orchestrate custom "planner,tdd-guide,odoo-reviewer" "Create a new Odoo module"
```

**Custom workflow still requires**: Sequential execution + Handoff verification for ALL agents.

## Odoo Development Workflow Tips

1. **Start with planner** for complex Odoo modules
2. **Always include odoo-reviewer** for framework compliance
3. **Use security-reviewer** for modules handling sensitive data
4. **Keep handoffs concise** - focus on Odoo context next agent needs
5. **NEVER skip verification** between agents
6. **Test in real Odoo environment** before final deployment

---

## FINAL REMINDER: EXECUTION MANDATE

When `/orchestrate` is invoked:

1. **Create task checklist** with ALL workflow agents
2. **Execute agents SEQUENTIALLY** - one at a time
3. **Verify each HANDOFF** before proceeding
4. **Mark each agent COMPLETE** before moving to next
5. **ALL agents must complete** - zero exceptions
6. **Generate final report** only after ALL agents done

**VIOLATION OF THESE RULES WILL RESULT IN INCOMPLETE ODOO DEVELOPMENT WORKFLOW.**

## Odoo 19 Quick Reference

### Common Dependencies
- `base` - Core Odoo models (res.partner, res.users)
- `web` - Frontend framework, views
- `mail` - Messaging and chatter
- `sale` - Sales orders, customers
- `purchase` - Purchase orders
- `stock` - Inventory management
- `account` - Accounting
- `hr` - Human resources

### Model Naming
- New model: `module.model_name`
- Inheritance: `_inherit = 'existing.model'`

### View Naming
- XML ID: `module.view_model_type` (e.g., `sale.view_order_form`)

### Field Naming Conventions
- Many2one: `name_id`
- One2many: `line_ids`
- Boolean: `is_feature` or `has_feature`
- Date: `date_field`
- Datetime: `datetime_field`

### Common API Decorators
- `@api.model` - Model-level method
- `@api.depends(*fields)` - Computed field
- `@api.onchange(*fields)` - Onchange handler
- `@api.constrains(*fields)` - Constraint validation
- `@api.returns('self')` - Return type annotation
