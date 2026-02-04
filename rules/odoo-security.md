# Odoo 19 Security Rules

## Critical Security Rules

### 1. Never Hardcode Secrets

```python
# ❌ CRITICAL: Hardcoded secrets
API_KEY = "sk-proj-xxxxx"
DB_PASSWORD = "admin123"
TOKEN = "ghp_xxxxxxxxxxxx"

# ✅ CORRECT: Use environment variables or system parameters
import os

API_KEY = os.environ.get('MY_API_KEY')
if not API_KEY:
    raise UserError(_("API key not configured"))

# Or use Odoo system parameters
API_KEY = self.env['ir.config_parameter'].sudo().get_param('my_module.api_key')
```

### 2. Always Define Access Rights

```python
# ❌ CRITICAL: Model without access rights
class MySecretData(models.Model):
    _name = 'my.secret.data'

# ✅ CORRECT: Define access rights in security/ir.model.access.csv
access_my_secret_data_user,my.secret.data,base.group_user,1,1,0,0
```

### 3. Multi-User Models Must Have Record Rules

```python
# ❌ CRITICAL: Multi-user model without record rules
class UserNote(models.Model):
    _name = 'user.note'
    user_id = fields.Many2one('res.users', required=True)
    # Anyone can read anyone's notes!

# ✅ CORRECT: Add record rule in security/security.xml
<record id="rule_user_note_own" model="ir.rule">
    <field name="domain_force">[('user_id', '=', user.id)]</field>
    <field name="model_id" ref="model_user_note"/>
</record>
```

### 4. Never Use sudo() Without Justification

```python
# ❌ CRITICAL: sudo() bypasses all security checks
def action_approve(self):
    self.sudo().write({'state': 'approved'})

# ✅ CORRECT: Only sudo when necessary and documented
def action_technical_cleanup(self):
    # Technical cleanup that should bypass access rights
    # Document why sudo is used
    self.sudo()._cleanup_old_records()
```

### 5. CSRF Protection Required for POST Routes

```python
# ❌ CRITICAL: POST route without CSRF protection
@http.route('/my/action', type='http', methods=['POST'], auth='user')
def my_action(self, **kwargs):
    pass

# ✅ CORRECT: Use csrf=True for POST
@http.route('/my/action', type='http', methods=['POST'],
            auth='user', csrf=True)
def my_action(self, **kwargs):
    pass
```

### 6. SQL Injection Prevention

```python
# ❌ CRITICAL: SQL injection vulnerability
query = f"SELECT * FROM table WHERE id = {user_input}"
self.env.cr.execute(query)

# ❌ CRITICAL: SQL injection via format string
query = "SELECT * FROM table WHERE name = '{}'".format(user_input)
self.env.cr.execute(query)

# ✅ CORRECT: Use ORM
records = self.env['table'].search([('id', '=', user_input)])

# ✅ CORRECT: Use parameterized queries (when SQL is necessary)
self.env.cr.execute("SELECT * FROM table WHERE id = %s", (user_input,))
```

### 7. XSS Prevention in QWeb

```xml
<!-- ❌ HIGH: XSS vulnerability -->
<t t-out="user_input"/>
<a t-att-href="user_input">Link</a>

<!-- ✅ CORRECT: Use t-esc (default escapes) or t-raw with caution -->
<t t-esc="user_input"/>
<a t-att-href="validate_url(user_input)">Link</a>
```

### 8. Input Validation Required

```python
# ❌ HIGH: No validation
@http.route('/api/data', type='json', auth='user')
def api_data(self, data):
    return self.env['model'].search([('name', '=', data['query'])])

# ✅ CORRECT: Validate input
@http.route('/api/data', type='json', auth='user')
def api_data(self, **kwargs):
    query = kwargs.get('query')
    if not query or len(query) > 100:
        raise UserError(_("Invalid query"))
    if '<' in query or '>' in query:
        raise UserError(_("Invalid characters"))
    return self.env['model'].search([('name', '=', query)])
```

### 9. Never Expose Sensitive Data in APIs

```python
# ❌ HIGH: Internal fields exposed in API
@http.route('/api/user', type='json', auth='user')
def user_info(self):
    return {
        'id': self.env.user.id,
        'password_hash': self.env.user.password,  # ❌ Never expose!
    }

# ✅ CORRECT: Only expose necessary data
@http.route('/api/user', type='json', auth='user')
def user_info(self):
    return {
        'id': self.env.user.id,
        'name': self.env.user.name,
    }
```

### 10. Information Disclosure Prevention

```python
# ❌ HIGH: Detailed error messages to users
try:
    result = self._external_api_call()
except Exception as e:
    raise UserError(_("Error: %s") % e)  # Exposes stack trace

# ✅ CORRECT: Generic error messages
try:
    result = self._external_api_call()
except Exception as e:
    _logger.error('API call failed: %s', e)
    raise UserError(_('An error occurred. Please try again.'))
```

## Access Control Rules

### Access Rights Definition

```csv
# security/ir.model.access.csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_my_model_user,my.model,base.group_user,1,1,1,0
access_my_model_manager,my.model,my_module.group_manager,1,1,1,1
```

### Record Rule Patterns

```xml
<!-- ✅ Users can only see their own records -->
<record id="rule_my_model_own" model="ir.rule">
    <field name="domain_force">[('user_id', '=', user.id)]</field>
    <field name="groups" eval="[(4, ref('base.group_user'))]"/>
</record>

<!-- ❌ Overly permissive rule -->
<record id="rule_my_model_all" model="ir.rule">
    <field name="domain_force">[(1, '=', 1)]</field>
</record>
```

## Authentication & Authorization

### Route Authentication

```python
# ✅ Correct authentication
@http.route('/public/page', type='http', auth='public')
def public_page(self):
    pass

@http.route('/user/page', type='http', auth='user')
def user_page(self):
    pass

@http.route('/api/data', type='json', auth='user')
def api_data(self):
    pass

# ❌ Missing auth parameter
@http.route('/my/page', type='http')
def my_page(self):
    pass
```

### Group-Based Access Control

```python
# ✅ Check user groups
def my_method(self):
    if not self.env.user.has_group('my_module.group_manager'):
        raise AccessError(_("You don't have permission for this action"))
    # Continue with privileged operation
```

## Sensitive Field Protection

```python
# ✅ Sensitive fields with groups
class MyModel(models.Model):
    _name = 'my.model'

    internal_notes = fields.Text(
        string='Internal Notes',
        groups='base.group_system',
    )

    salary = fields.Float(
        string='Salary',
        groups='hr.group_hr_manager',
    )
```

## Security Testing Requirements

### Required Security Tests

```python
# tests/test_security.py
from odoo.tests import TransactionCase, tagged

@tagged('post_install', '-at_install')
class TestSecurity(TransactionCase):
    """Test security configuration"""

    def test_user_can_read_own_records(self):
        """Test users can read their own records"""
        user = self.env['res.users'].create({
            'name': 'Test User',
            'login': 'test@example.com',
            'groups_id': [(6, 0, [self.env.ref('base.group_user').id])]
        })
        record = self.env['my.model'].sudo().create({
            'name': 'Test Record',
            'user_id': user.id,
        })

        # User should see their own record
        records = self.env['my.model'].with_user(user).search([])
        self.assertIn(record.id, records.ids)

    def test_user_cannot_read_other_records(self):
        """Test users cannot read other users' records"""
        user1 = self.env['res.users'].create({
            'name': 'User 1',
            'login': 'user1@example.com',
            'groups_id': [(6, 0, [self.env.ref('base.group_user').id])]
        })
        user2 = self.env['res.users'].create({
            'name': 'User 2',
            'login': 'user2@example.com',
            'groups_id': [(6, 0, [self.env.ref('base.group_user').id])]
        })

        record1 = self.env['my.model'].sudo().create({
            'name': 'Record 1',
            'user_id': user1.id,
        })
        record2 = self.env['my.model'].sudo().create({
            'name': 'Record 2',
            'user_id': user2.id,
        })

        # User1 should not see record2
        records = self.env['my.model'].with_user(user1).search([])
        self.assertIn(record1.id, records.ids)
        self.assertNotIn(record2.id, records.ids)

    def test_manager_can_read_all_records(self):
        """Test managers can read all records"""
        manager = self.env['res.users'].create({
            'name': 'Test Manager',
            'login': 'manager@example.com',
            'groups_id': [(6, 0, [self.env.ref('my_module.group_manager').id])]
        })

        record1 = self.env['my.model'].sudo().create({
            'name': 'Record 1',
            'user_id': user1.id,
        })

        # Manager should see all records
        records = self.env['my.model'].with_user(manager).search([])
        self.assertIn(record1.id, records.ids)
```

## Security Checklist

Before considering code secure:

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
- [ ] Group-based access control where needed

### Secrets Management
- [ ] No hardcoded API keys, passwords, tokens
- [ ] Secrets in environment variables or system parameters
- [ ] No secrets in git history
- [ ] No secrets in logs

### SQL Security
- [ ] No string concatenation in queries
- [ ] All queries use ORM (except where justified)
- [ ] Parameterized queries for raw SQL

## Security Tools

```bash
# Check for hardcoded secrets
grep -rE "(api_key|password|secret|token|aws_key)" --include="*.py" .

# Check for sudo() usage
grep -r "\.sudo()" --include="*.py" .

# Check for direct SQL
grep -r "\.cr\.execute" --include="*.py" .

# Check for missing access rights
find models/ -name "*.py" -exec basename {} .py \; | while read model; do
    grep -q "$model" security/ir.model.access.csv || echo "Missing: $model"
done

# Python security scanner
pip install bandit
bandit -r odoo_module/

# Dependency vulnerability check
pip install safety
safety check -r requirements.txt
```

## Critical Security Violations

Any of these will block code review:

1. **Hardcoded secrets** (API keys, passwords, tokens)
2. **SQL injection risks** (string concatenation in queries)
3. **Missing access rights** (no ir.model.access.csv entry)
4. **Missing record rules** (for multi-user models)
5. **Unauthorized sudo() usage** (without justification)
6. **Missing CSRF protection** (on POST routes)
7. **XSS vulnerabilities** (unescaped user input in QWeb)
8. **Missing input validation** (on user inputs)
9. **Exposed sensitive data** (in APIs or error messages)
10. **Information disclosure** (stack traces to users)
