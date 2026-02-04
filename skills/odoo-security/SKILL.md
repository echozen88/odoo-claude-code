# Odoo 19 Security Guide

This skill provides comprehensive guidance on implementing security in Odoo 19 applications.

## Security Architecture

### Odoo Security Layers

1. **Authentication** - User login and session management
2. **Authorization** - Access rights (ir.model.access)
3. **Data Access** - Record rules (ir.rule)
4. **Application Security** - CSRF, input validation, output encoding

## Access Rights (ir.model.access)

### Defining Access Rights

```csv
# security/ir.model.access.csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_my_model_user,my.model,base.group_user,1,1,1,0
access_my_model_manager,my.model,my_module.group_manager,1,1,1,1
access_my_model_admin,my.model,base.group_system,1,1,1,1
```

### Format Explanation

| Column | Description | Example |
|---------|-------------|----------|
| id | Unique ID for access right | `access_my_model_user` |
| name | Description | `my.model` |
| model_id:id | Model reference | `model_my_model` |
| group_id:id | Group that gets access | `base.group_user` |
| perm_read | Can read records (1=yes, 0=no) | 1 |
| perm_write | Can update records | 1 |
| perm_create | Can create records | 1 |
| perm_unlink | Can delete records | 1 |

### Access Right Best Practices

```python
# __manifest__.py
{
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
    ],
}

# security/ir.model.access.csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
# User can read and write, but not create or delete
access_my_model_user,my.model,base.group_user,1,1,0,0
# Manager has full access
access_my_model_manager,my.model,my_module.group_manager,1,1,1,1
# Admin always has full access
access_my_model_admin,my.model,base.group_system,1,1,1,1
```

### Access Right Patterns

```python
# 1. Public read access (no group required)
access_my_model_public,my.model,,1,0,0,0

# 2. Read-only for regular users
access_my_model_readonly,my.model,base.group_user,1,0,0,0

# 3. Full access for regular users
access_my_model_user,my.model,base.group_user,1,1,1,0

# 4. Manager access with delete permission
access_my_model_manager,my.model,my_module.group_manager,1,1,1,1

# 5. Technical user (invisible) - for automation
access_my_model_technical,my.model,,1,1,1,1
```

## Record Rules (ir.rule)

### Basic Record Rule

```xml
<odoo>
    <data noupdate="1">
        <!-- Users can only see their own records -->
        <record id="rule_my_model_own" model="ir.rule">
            <field name="name">My Model: User Records Only</field>
            <field name="model_id" ref="model_my_model"/>
            <field name="domain_force">[('user_id', '=', user.id)]</field>
            <field name="groups" eval="[(4, ref('base.group_user'))]"/>
            <field name="perm_read" eval="True"/>
            <field name="perm_write" eval="True"/>
            <field name="perm_create" eval="True"/>
            <field name="perm_unlink" eval="True"/>
        </record>
    </data>
</odoo>
```

### Record Rule Patterns

```xml
<!-- 1. User can only see their own records -->
<record id="rule_my_model_own" model="ir.rule">
    <field name="domain_force">[('user_id', '=', user.id)]</field>
    <field name="groups" eval="[(4, ref('base.group_user'))]"/>
</record>

<!-- 2. Users can see their own OR company records -->
<record id="rule_my_model_user_or_company" model="ir.rule">
    <field name="domain_force">[
        '|',
        ('user_id', '=', user.id),
        ('company_id', '=', user.company_id.id)
    ]</field>
</record>

<!-- 3. Users can see records from their department -->
<record id="rule_my_model_department" model="ir.rule">
    <field name="domain_force">[
        ('department_id', 'in', user.department_id.child_ids.ids + [user.department_id.id])
    ]</field>
</record>

<!-- 4. Managers can see all records -->
<record id="rule_my_model_manager_all" model="ir.rule">
    <field name="name">My Model: Manager All Records</field>
    <field name="model_id" ref="model_my_model"/>
    <field name="domain_force">[(1, '=', 1)]</field>
    <field name="groups" eval="[(4, ref('my_module.group_manager'))]"/>
</record>

<!-- 5. Rule with multiple conditions -->
<record id="rule_my_model_complex" model="ir.rule">
    <field name="domain_force">[
        '&',
        ('active', '=', True),
        '|',
        ('user_id', '=', user.id),
        ('is_public', '=', True)
    ]</field>
</record>

<!-- 6. Time-based rule -->
<record id="rule_my_model_date" model="ir.rule">
    <field name="domain_force">[
        ('date', '>=', context_today() - relativedelta(days=30))
    ]</field>
</record>
```

### Global vs Local Record Rules

```xml
<!-- Global rule (no groups) - applies to all users -->
<record id="rule_my_model_active" model="ir.rule">
    <field name="name">My Model: Active Only</field>
    <field name="domain_force">[('active', '=', True)]</field>
    <!-- No groups field -->
</record>

<!-- Local rule (with groups) - applies to specific groups -->
<record id="rule_my_model_user_own" model="ir.rule">
    <field name="name">My Model: User Own</field>
    <field name="domain_force">[('user_id', '=', user.id)]</field>
    <field name="groups" eval="[(4, ref('base.group_user'))]"/>
</record>
```

## Security Groups

### Defining Security Groups

```xml
<odoo>
    <data noupdate="1">
        <!-- Basic user group -->
        <record id="group_my_module_user" model="res.groups">
            <field name="name">My Module User</field>
            <field name="category_id" ref="base.module_category_tools"/>
            <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
            <field name="comment">Basic access to My Module</field>
        </record>

        <!-- Manager group -->
        <record id="group_my_module_manager" model="res.groups">
            <field name="name">My Module Manager</field>
            <field name="category_id" ref="base.module_category_tools"/>
            <field name="implied_ids" eval="[(4, ref('group_my_module_user'))]"/>
            <field name="comment">Full access to My Module including delete</field>
        </record>

        <!-- Administrator group -->
        <record id="group_my_module_admin" model="res.groups">
            <field name="name">My Module Admin</field>
            <field name="category_id" ref="base.module_category_tools"/>
            <field name="implied_ids" eval="[(4, ref('group_my_module_manager'))]"/>
            <field name="users" eval="[(4, ref('base.user_root'))]"/>
            <field name="comment">Technical administration access</field>
        </record>
    </data>
</odoo>
```

### Group Inheritance

```xml
<!-- Implied groups give all permissions of implied group -->
<record id="group_my_module_manager" model="res.groups">
    <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
</record>
```

## Controller Security

### Route Authentication

```python
from odoo import http
from odoo.http import request

# 1. Public route - No authentication required
@http.route('/my/public/page', type='http', auth='public')
def public_page(self):
    return "Public content"

# 2. User route - Requires logged-in user
@http.route('/my/user/page', type='http', auth='user')
def user_page(self):
    if request.env.user == request.env.ref('base.public_user'):
        return "Not logged in"
    return "User content"

# 3. User API Key route - For API access
@http.route('/my/api/endpoint', type='json', auth='user_api_key')
def api_endpoint(self, **kwargs):
    return {'result': 'success'}

# 4. None route - For internal use, no user context
@http.route('/my/internal/action', type='http', auth='none')
def internal_action(self):
    # No user.id available
    return request.render('my_module.template', {})

# 5. Website route - For public website
@http.route('/my/page', type='http', auth='public', website=True)
def website_page(self, **kwargs):
    values = {}
    values['user'] = request.env.user
    return request.render('my_module.website_template', values)
```

### CSRF Protection

```python
# HTTP POST routes must have CSRF protection
@http.route('/my/form/submit', type='http', methods=['POST'],
            auth='public', website=True, csrf=True)
def form_submit(self, **kwargs):
    # CSRF token validated automatically
    data = kwargs.get('data')
    return "Form submitted"

# JSON routes handle CSRF automatically
@http.route('/my/api/data', type='json', auth='user')
def api_data(self, **kwargs):
    # CSRF protection built-in for JSON
    return {'result': 'success'}
```

### Input Validation

```python
@http.route('/my/api/data', type='json', auth='user')
def api_data(self, **kwargs):
    data = kwargs.get('data')

    # Validate presence
    if not data:
        return {'error': 'No data provided'}

    # Validate type
    if not isinstance(data, dict):
        return {'error': 'Invalid data format'}

    # Validate required fields
    required_fields = ['name', 'value']
    for field in required_fields:
        if field not in data:
            return {'error': f'Missing required field: {field}'}

    # Validate field types and constraints
    name = data.get('name')
    if not name or len(name) < 3:
        return {'error': 'Name must be at least 3 characters'}

    value = data.get('value')
    try:
        value = float(value)
    except (ValueError, TypeError):
        return {'error': 'Value must be numeric'}

    if value < 0:
        return {'error': 'Value must be positive'}

    # Sanitize input
    name = bleach.clean(name, tags=[], strip=True)

    # Process validated data
    record = request.env['my.model'].create({
        'name': name,
        'value': value,
    })

    return {'success': True, 'record_id': record.id}
```

### Output Filtering

```python
@http.route('/my/api/data', type='json', auth='user')
def api_data(self):
    # Never return sensitive internal data
    records = request.env['my.model'].search([])
    data = records.read(['name', 'value', 'date'])
    # Don't include: password_hash, internal_notes, etc.
    return {
        'success': True,
        'data': data,
    }
```

## Model Security

### Prevent Unauthorized sudo()

```python
class MyModel(models.Model):
    _name = 'my.model'

    # ❌ BAD: Always using sudo()
    def action_approve(self):
        # Bypasses all security
        self.sudo().write({'state': 'approved'})

    # ✅ GOOD: Only sudo when necessary
    def action_technical_cleanup(self):
        # Technical cleanup that shouldn't be blocked by access rights
        # Document why sudo is used
        self.sudo()._cleanup_old_records()

    # ✅ GOOD: Use regular access
    def action_approve(self):
        # Security rules apply
        self.write({'state': 'approved'})
```

### Check Record Ownership

```python
class MyModel(models.Model):
    _name = 'my.model'

    def action_delete(self):
        for record in self:
            # Verify user can delete this record
            if record.user_id != self.env.user:
                raise AccessError(_("You can only delete your own records"))
        return super(MyModel, self).unlink()

    def check_access_rights(self, operation='read'):
        """Custom access check"""
        for record in self:
            if not self.env['ir.access'].check(
                self._name,
                operation,
                raise_exception=False
            ):
                raise AccessError(_(
                    "You don't have permission to %s this record",
                    operation
                ))
```

### Sensitive Field Protection

```python
class MyModel(models.Model):
    _name = 'my.model'

    # Sensitive fields - use groups
    internal_notes = fields.Text(
        string='Internal Notes',
        groups='base.group_system',
    )

    salary = fields.Float(
        string='Salary',
        groups='hr.group_hr_manager',
    )

    # Override read to filter sensitive fields
    def read(self, fields=None, load='_classic_read'):
        if not fields:
            # Don't return sensitive fields by default
            result = super(MyModel, self).read(fields)
            # Filter out sensitive fields based on user groups
            if not self.env.user.has_group('base.group_system'):
                result = [r for r in result if 'internal_notes' not in r]
            if not self.env.user.has_group('hr.group_hr_manager'):
                result = [r for r in result if 'salary' not in r]
            return result
        return super(MyModel, self).read(fields, load=load)
```

## QWeb Security

### Output Encoding

```xml
<!-- ✅ GOOD: Use t-esc to escape content -->
<t t-esc="user_input"/>

<!-- ✅ GOOD: Use t-raw only with trusted content -->
<t t-raw="internal_html"/>

<!-- ❌ BAD: Not escaping user input -->
<t t-out="user_input"/>

<!-- ❌ BAD: XSS vulnerability -->
<a t-att-href="user_url">Link</a>

<!-- ✅ GOOD: Validate URLs -->
<a t-att-href="validate_url(user_url)">Link</a>
```

### Security in Templates

```xml
<template id="website_template">
    <!-- Always escape user content -->
    <div>
        <h1 t-esc="record.name"/>
        <p t-esc="record.description"/>
    </div>

    <!-- Don't expose internal IDs to public -->
    <div>
        <h2 t-esc="record.display_name"/>
    </div>

    <!-- Conditional display based on access -->
    <div t-if="user.has_group('my_module.group_manager')">
        <button>Manager Only Button</button>
    </div>
</template>
```

## Common Security Pitfalls

### 1. Missing Access Rights

```python
# ❌ BAD: Model without access rights
class MySecretData(models.Model):
    _name = 'my.secret.data'

# ✅ GOOD: Define access rights
# security/ir.model.access.csv
access_my_secret_data_user,my.secret.data,base.group_user,1,1,0,0
```

### 2. Missing Record Rules

```python
# ❌ BAD: Multi-user model without record rules
class UserNote(models.Model):
    _name = 'user.note'
    user_id = fields.Many2one('res.users', required=True)

# ✅ GOOD: Add record rule
<record id="rule_user_note_own" model="ir.rule">
    <field name="domain_force">[('user_id', '=', user.id)]</field>
    <field name="model_id" ref="model_user_note"/>
</record>
```

### 3. Overly Permissive Record Rules

```xml
<!-- ❌ BAD: Users can see all records -->
<record id="rule_my_model_all" model="ir.rule">
    <field name="domain_force">[(1, '=', 1)]</field>
</record>

<!-- ✅ GOOD: Restrict based on user/company -->
<record id="rule_my_model_user" model="ir.rule">
    <field name="domain_force">[('user_id', '=', user.id)]</field>
</record>
```

### 4. SQL Injection

```python
# ❌ CRITICAL: SQL injection
query = f"SELECT * FROM table WHERE id = {user_input}"
self.env.cr.execute(query)

# ✅ GOOD: Use ORM
records = self.env['table'].search([('id', '=', user_input)])

# ✅ GOOD: Or parameterized queries
self.env.cr.execute("SELECT * FROM table WHERE id = %s", (user_input,))
```

### 5. Exposing Internal Data

```python
# ❌ BAD: Expose internal data in API
@http.route('/api/user', type='json', auth='user')
def user_info(self):
    return {
        'id': self.env.user.id,
        'password_hash': self.env.user.password,  # ❌ Never expose!
    }

# ✅ GOOD: Only expose necessary data
@http.route('/api/user', type='json', auth='user')
def user_info(self):
    return {
        'id': self.env.user.id,
        'name': self.env.user.name,
    }
```

## Security Checklist

### Access Control
- [ ] All models have access rights (ir.model.access.csv)
- [ ] Multi-user models have record rules (ir.rule)
- [ ] Groups follow least privilege principle
- [ ] sudo() only used where absolutely necessary
- [ ] Record rules don't conflict

### Input Validation
- [ ] All user inputs validated
- [ ] Length limits on string inputs
- [ ] Type checking on numeric inputs
- [ ] URL/domain validation for external calls

### Output Encoding
- [ ] No t-raw with user input in QWeb
- [ ] URLs validated before use in attributes
- [ ] Sensitive data not in error messages
- [ ] No stack traces exposed to users

### Authentication & Authorization
- [ ] CSRF protection on HTTP POST routes
- [ ] Proper auth parameter on all routes
- [ ] Session management secure
- [ ] API keys validated

### Secrets Management
- [ ] No hardcoded API keys, passwords, tokens
- [ ] Secrets in environment variables or system parameters
- [ ] No secrets in git history
- [ ] No secrets in logs

## Security Testing

```python
# tests/test_security.py
from odoo.tests import TransactionCase, tagged

@tagged('post_install', '-at_install')
class TestSecurity(TransactionCase):
    """Test security configuration"""

    def setUp(self):
        super(TestSecurity, self).setUp()
        self.user = self.env['res.users'].create({
            'name': 'Test User',
            'login': 'test@example.com',
            'groups_id': [(6, 0, [self.env.ref('base.group_user').id])]
        })
        self.manager = self.env['res.users'].create({
            'name': 'Test Manager',
            'login': 'manager@example.com',
            'groups_id': [(6, 0, [self.env.ref('my_module.group_manager').id])]
        })
        self.record = self.env['my.model'].sudo().create({
            'name': 'Test Record',
            'user_id': self.user.id,
        })

    def test_user_can_read_own_records(self):
        """Test users can read their own records"""
        record = self.record.with_user(self.user)
        self.assertTrue(bool(record))
        self.assertEqual(record.user_id, self.user)

    def test_user_cannot_read_other_records(self):
        """Test users cannot read other users' records"""
        other_user = self.env['res.users'].create({
            'name': 'Other User',
            'login': 'other@example.com',
            'groups_id': [(6, 0, [self.env.ref('base.group_user').id])]
        })
        other_record = self.env['my.model'].sudo().create({
            'name': 'Other Record',
            'user_id': other_user.id,
        })

        # User should not see other_record
        records = self.env['my.model'].with_user(self.user).search([])
        self.assertNotIn(other_record.id, records.ids)

    def test_manager_can_read_all_records(self):
        """Test managers can read all records"""
        records = self.env['my.model'].with_user(self.manager).search([])
        self.assertIn(self.record.id, records.ids)

    def test_user_cannot_delete_others(self):
        """Test users cannot delete other users' records"""
        other_record = self.env['my.model'].sudo().create({
            'name': 'Other Record',
            'user_id': self.user.id,
        })
        other_user = self.env['res.users'].create({
            'name': 'Other User',
            'login': 'other2@example.com',
            'groups_id': [(6, 0, [self.env.ref('base.group_user').id])]
        })

        with self.assertRaises(Exception):
            other_record.with_user(other_user).unlink()

    def test_no_access_without_rights(self):
        """Test that users without group access cannot access"""
        # Remove user from any module groups
        self.user.write({'groups_id': [(5, self.env.ref('base.group_user').id)]})
        self.assertFalse(self.user.has_group('my_module.group_user'))

        # User should not have any access
        with self.assertRaises(Exception):
            self.env['my.model'].with_user(self.user).search([])

    def test_csrf_protection(self):
        """Test CSRF protection on POST routes"""
        # Test that POST without CSRF token fails
        pass
```

## Security Tools

```bash
# Check for hardcoded secrets
grep -rE "(api_key|password|secret|token|aws_key)" --include="*.py" .

# Check for sudo() usage
grep -r "\.sudo()" --include="*.py" .

# Check for direct SQL
grep -r "\.cr\.execute" --include="*.py" .

# Check for missing access rights
find . -name "models/*.py" -exec basename {} \; | while read model; do
    grep -q "$model" security/ir.model.access.csv || echo "Missing: $model"
done

# Python security scanner
pip install bandit
bandit -r odoo_module/

# Dependency vulnerability check
pip install safety
safety check -r requirements.txt
```

## Summary

Security in Odoo is multi-layered:
1. **Access rights** - Define who can interact with models
2. **Record rules** - Define which records each user can access
3. **Controller security** - Protect endpoints with proper auth and CSRF
4. **Input validation** - Validate and sanitize all user inputs
5. **Output encoding** - Never expose sensitive data or unescaped content
6. **Never sudo()** - Only bypass security when absolutely necessary
