# Orchestrate Command (Odoo 19)

Sequential agent workflow for complex Odoo 19 development tasks.

## Usage

`/orchestrate [workflow-type] [task-description]`

## Workflow Types

### feature
Full Odoo 19 feature implementation workflow:
```
planner -> tdd-guide -> code-reviewer -> security-reviewer -> odoo-reviewer
```

### bugfix
Odoo bug investigation and fix workflow:
```
explorer -> tdd-guide -> code-reviewer -> odoo-reviewer
```

### refactor
Safe Odoo code refactoring workflow:
```
architect -> code-reviewer -> tdd-guide -> odoo-reviewer
```

### security
Odoo security-focused review:
```
security-reviewer -> code-reviewer -> odoo-reviewer -> architect
```

### performance
Odoo performance optimization workflow:
```
performance-agent -> planner -> code-reviewer -> odoo-reviewer
```

### migration
Odoo version migration workflow:
```
migration-agent -> code-reviewer -> odoo-reviewer -> security-reviewer
```

## Execution Pattern

For each agent in the workflow:

1. **Invoke agent** with context from previous agent
2. **Collect output** as structured handoff document
3. **Pass to next agent** in chain
4. **Aggregate results** into final report

## Handoff Document Format

Between agents, create a handoff document:

```markdown
## HANDOFF: [previous-agent] -> [next-agent]

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
```

## Example: Odoo Feature Workflow

```
/orchestrate feature "Add a new sales report with custom fields"
```

Executes:

1. **Planner Agent** (Odoo 19 specialist)
   - Analyzes requirements for Odoo 19
   - Creates implementation plan including:
     - Model structure (new model or inheritance)
     - Field definitions (types, constraints)
     - Security requirements (access rights, record rules)
     - View definitions (tree, form, pivot, graph)
     - Controller routes if needed
   - Output: `HANDOFF: planner -> tdd-guide`

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

Executes:

1. **Performance Agent**
   - Analyzes ORM queries for N+1 problems
   - Identifies missing database indexes
   - Checks computed field caching
   - Reviews view performance (tree limits, expensive fields)
   - Analyzes record rules performance impact
   - Output: `HANDOFF: performance-agent -> planner`

2. **Planner Agent**
   - Creates optimization plan
   - Identifies quick wins vs major refactor
   - Output: `HANDOFF: planner -> code-reviewer`

3. **Code Reviewer Agent**
   - Reviews suggested optimizations
   - Checks PEP8 compliance
   - Output: `HANDOFF: code-reviewer -> odoo-reviewer`

4. **Odoo Reviewer Agent**
   - Framework compliance check for optimized code
   - Output: Final Report

## Example: Migration Workflow

```
/orchestrate migration "17.0" "19.0"
```

Executes:

1. **Migration Agent**
   - Analyzes code for deprecated APIs between versions
   - Generates migration checklist
   - Identifies breaking changes
   - Recommends data migration scripts
   - Output: `HANDOFF: migration-agent -> code-reviewer`

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

For independent checks, run agents in parallel:

```markdown
### Parallel Phase
Run simultaneously:
- code-reviewer (code quality)
- security-reviewer (security)
- odoo-reviewer (framework compliance)

### Merge Results
Combine outputs into single report
```

## Arguments

$ARGUMENTS:
- `feature <description>` - Full Odoo feature workflow
- `bugfix <description>` - Odoo bug fix workflow
- `refactor <description>` - Odoo refactoring workflow
- `security <description>` - Odoo security review workflow
- `performance <description>` - Odoo performance optimization workflow
- `migration <from-version> <to-version>` - Odoo version migration workflow
- `custom <agents> <description>` - Custom agent sequence

## Custom Workflow Example

```
/orchestrate custom "planner,tdd-guide,odoo-reviewer" "Create a new Odoo module"
```

## Odoo Development Workflow Tips

1. **Start with planner** for complex Odoo modules
2. **Always include odoo-reviewer** for framework compliance
3. **Use security-reviewer** for modules handling sensitive data
4. **Keep handoffs concise** - focus on Odoo context next agent needs
5. **Run verification** between agents if needed
6. **Test in real Odoo environment** before final deployment

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
