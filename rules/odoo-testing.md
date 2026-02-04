# Odoo 19 Testing Rules

## Testing Philosophy

- **Tests first, code later** - Write failing tests before implementing
- **80%+ coverage required** - All production code must be tested
- **Test isolation** - Tests should be independent
- **Test reality** - Use realistic test scenarios

## Test Structure

### Test Module Layout

```
tests/
├── __init__.py
├── __manifest__.py
├── test_models.py
├── test_security.py
├── test_http.py
└── fixtures/
    └── data.xml
```

### Test Module Manifest

```python
# tests/__manifest__.py
{
    'name': 'My Module Tests',
    'version': '16.0.1.0.0',
    'depends': ['my_module'],
    'data': [
        'fixtures/data.xml',
    ],
    'installable': True,
}
```

## Test Types

### 1. Model Tests (TransactionCase)

```python
from odoo.tests import TransactionCase, tagged

@tagged('post_install', '-at_install')
class TestMyModel(TransactionCase):
    """Test MyModel methods and constraints"""

    @classmethod
    def setUpClass(cls):
        super(TestMyModel, cls).setUpClass()
        # Setup for all tests

    def setUp(self):
        super(TestMyModel, self).setUp()
        # Setup for each test
        self.user = self.env['res.users'].create({
            'name': 'Test User',
            'login': 'test@example.com',
        })
        self.record = self.env['my.model'].create({
            'name': 'Test Record',
            'user_id': self.user.id,
        })

    def test_create_record(self):
        """Test creating a new record"""
        record = self.env['my.model'].create({
            'name': 'New Record',
            'value': 100,
        })
        self.assertTrue(record.id)
        self.assertEqual(record.name, 'New Record')
        self.assertEqual(record.value, 100)

    def test_field_default(self):
        """Test default field values"""
        record = self.env['my.model'].create({'name': 'Test'})
        self.assertEqual(record.value, 0)  # Default value

    def test_required_field_validation(self):
        """Test required field validation"""
        with self.assertRaises(Exception):
            self.env['my.model'].create({})  # Missing required 'name'

    def test_constrains(self):
        """Test SQL constraints"""
        record1 = self.env['my.model'].create({
            'name': 'Unique',
            'code': 'A001',
        })
        with self.assertRaises(Exception):
            # Unique constraint should fail
            self.env['my.model'].create({
                'name': 'Unique',
                'code': 'A001',
            })

    def test_compute_field(self):
        """Test computed field calculation"""
        record = self.env['my.model'].create({
            'name': 'Test',
            'value1': 10,
            'value2': 20,
        })
        self.assertEqual(record.compute_total, 30)

    def test_onchange_method(self):
        """Test onchange method behavior"""
        record = self.env['my.model'].new({'value1': 10})
        record._onchange_value1()
        self.assertEqual(record.value2, 20)  # Should double

    def test_search_method(self):
        """Test custom search methods"""
        record1 = self.env['my.model'].create({
            'name': 'Active',
            'active': True,
        })
        record2 = self.env['my.model'].create({
            'name': 'Inactive',
            'active': False,
        })

        active_records = self.env['my.model'].search([
            ('is_active', '=', True)
        ])
        self.assertIn(record1.id, active_records.ids)
        self.assertNotIn(record2.id, active_records.ids)

    def test_write_method(self):
        """Test write method"""
        self.record.write({'value': 200})
        self.assertEqual(self.record.value, 200)

    def test_unlink_method(self):
        """Test unlink method"""
        record_id = self.record.id
        self.record.unlink()
        not_found = self.env['my.model'].search([
            ('id', '=', record_id)
        ])
        self.assertFalse(not_found)
```

### 2. Security Tests (TransactionCase)

```python
@tagged('post_install', '-at_install')
class TestMyModelSecurity(TransactionCase):
    """Test MyModel security configuration"""

    def setUp(self):
        super(TestMyModelSecurity, self).setUp()
        self.group_user = self.env.ref('my_module.group_user')
        self.group_manager = self.env.ref('my_module.group_manager')
        self.record = self.env['my.model'].sudo().create({
            'name': 'Test Record',
            'user_id': self.env.user.id,
        })

    def test_user_can_read_own_records(self):
        """Test regular users can read records"""
        record = self.record.with_user(self.env.user)
        self.assertTrue(bool(record))
        self.assertEqual(record.name, 'Test Record')

    def test_user_cannot_delete_all(self):
        """Test regular users cannot delete all records"""
        user = self.env['res.users'].create({
            'name': 'Regular User',
            'login': 'user@example.com',
            'groups_id': [(6, 0, [self.group_user.id])]
        })
        other_record = self.env['my.model'].sudo().create({
            'name': 'Other Record',
            'user_id': self.env.user.id,
        })
        with self.assertRaises(Exception):
            other_record.with_user(user).unlink()

    def test_record_rules_isolation(self):
        """Test record rules properly isolate data"""
        user1 = self.env['res.users'].create({
            'name': 'User 1',
            'login': 'user1@example.com',
            'groups_id': [(6, 0, [self.group_user.id])]
        })
        user2 = self.env['res.users'].create({
            'name': 'User 2',
            'login': 'user2@example.com',
            'groups_id': [(6, 0, [self.group_user.id])]
        })

        record1 = self.env['my.model'].sudo().create({
            'name': 'User1 Record',
            'user_id': user1.id,
        })
        record2 = self.env['my.model'].sudo().create({
            'name': 'User2 Record',
            'user_id': user2.id,
        })

        # User1 should only see their own records
        user1_records = self.env['my.model'].with_user(user1).search([])
        self.assertIn(record1.id, user1_records.ids)
        self.assertNotIn(record2.id, user1_records.ids)

    def test_group_read_access(self):
        """Test group read access rights"""
        # Test that only users with proper group can read
        pass
```

### 3. HTTP/Controller Tests (HttpCase)

```python
@tagged('post_install', '-at_install')
class TestMyController(HttpCase):
    """Test MyController HTTP endpoints"""

    def setUp(self):
        super(TestMyController, self).setUp()
        self.user = self.env['res.users'].create({
            'name': 'Test User',
            'login': 'test@example.com',
        })
        self.record = self.env['my.model'].create({
            'name': 'Test Record',
        })

    def test_index_page_loads(self):
        """Test main index page loads"""
        response = self.url_open('/my/module')
        self.assertEqual(response.status_code, 200)
        self.assertIn('My Module', response.text)

    def test_json_endpoint(self):
        """Test JSON API endpoint"""
        self.authenticate('test@example.com', 'password')
        response = self.url_open(
            '/my/module/api/data',
            data=json.dumps({'param': 'value'}),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('result', data)

    def test_authenticated_endpoint(self):
        """Test endpoint requires authentication"""
        response = self.url_open('/my/module/protected')
        self.assertEqual(response.status_code, 401)  # Unauthorized

    def test_post_endpoint(self):
        """Test POST endpoint"""
        self.authenticate('test@example.com', 'password')
        response = self.url_open(
            '/my/module/create',
            data=json.dumps({'name': 'Test'}),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response.status_code, 201)
```

### 4. UI/JS Tests (QUnit)

```javascript
// tests/js_tests/my_widget_tests.js
odoo.define('my_module.tests', function (require) {
    "use strict";

    const FormView = require('web.FormView');
    const testUtils = require('web.test_utils');
    const { createView } = testUtils;

    QUnit.module('My Module Widget');

    QUnit.test('widget renders correctly', async function (assert) {
        assert.expect(1);

        const form = await createView({
            View: FormView,
            model: 'my.model',
            data: {},
            arch: `<form><field name="name"/></form>`,
        });

        assert.strictEqual(form.$('.o_field_widget').length, 1);
        form.destroy();
    });

    QUnit.test('widget handles user input', async function (assert) {
        assert.expect(1);

        const form = await createView({
            View: FormView,
            model: 'my.model',
            data: {},
            arch: `<form><field name="name"/></form>`,
        });

        const input = form.$('input');
        input.val('Test Value').trigger('input');

        assert.strictEqual(form.model.data.name, 'Test Value');
        form.destroy();
    });
});
```

## Test Decorators

```python
# Run after module installation (with demo data)
@tagged('post_install', '-at_install')
class MyTests(TransactionCase):
    pass

# Run before installation (without demo data)
@tagged('standard', '-at_install')
class MyTests(TransactionCase):
    pass

# Never run (manual testing only)
@tagged('standard', '-at_install', '-post_install')
class MyTests(TransactionCase):
    pass
```

## Test Data Fixtures

```xml
<!-- tests/fixtures/data.xml -->
<odoo>
    <data noupdate="1">
        <record id="test_partner_1" model="res.partner">
            <field name="name">Test Partner 1</field>
        </record>
        <record id="test_partner_2" model="res.partner">
            <field name="name">Test Partner 2</field>
        </record>
    </data>
</odoo>

<!-- Use in tests -->
def test_using_fixtures(self):
    partner = self.env.ref('test_partner_1')
    self.assertEqual(partner.name, 'Test Partner 1')
```

## Mocking

### Mock External API Calls

```python
from unittest.mock import patch

@patch('odoo.addons.my_module.models.my_model.external_api_call')
def test_external_call(self, mock_api):
    """Test that external API is called correctly"""
    mock_api.return_value = {'status': 'success'}

    result = self.record.call_external()

    mock_api.assert_called_once()
    self.assertEqual(result['status'], 'success')
```

### Mock Send Mail

```python
@patch('odoo.addons.mail.models.mail_mail.MailMail.send')
def test_email_sent(self, mock_send):
    """Test that email is sent on action"""
    self.record.action_send_email()
    mock_send.assert_called_once()
```

## Test Coverage Requirements

### Minimum Coverage

- **Statements**: 80%
- **Branches**: 80%
- **Functions**: 80%

### Running Coverage

```bash
# Run tests with coverage
odoo -d test_db \
    --test-enable \
    --test-tags=test_module \
    --stop-after-init \
    --log-level=test

# View coverage report (if configured)
```

## Test Quality Rules

### Test Independence

```python
# ✅ GOOD: Tests are independent
def test_create_1(self):
    record = self.env['my.model'].create({'name': 'Test 1'})
    self.assertTrue(record.id)

def test_create_2(self):
    record = self.env['my.model'].create({'name': 'Test 2'})
    self.assertTrue(record.id)

# ❌ BAD: Tests depend on each other
def test_create(self):
    self.record = self.env['my.model'].create({'name': 'Test'})

def test_update(self):
    # Depends on test_create
    self.record.write({'name': 'Updated'})
```

### Test Naming

```python
# ✅ GOOD: Descriptive test names
def test_user_can_create_record(self):
    pass

def test_record_validation_rejects_invalid_data(self):
    pass

# ❌ BAD: Generic test names
def test_1(self):
    pass

def test_create(self):
    pass
```

## Edge Cases to Test

1. **Empty values** - What if field is None or False?
2. **Zero values** - What if numeric field is 0?
3. **Negative values** - Should negative values be allowed?
4. **Empty lists** - What if recordset is empty?
5. **Invalid types** - What if wrong type passed?
6. **Boundary conditions** - Min/max values, length limits
7. **Concurrency** - Multiple users modifying same record
8. **Permissions** - Different user group access
9. **Archived records** - Test with active=False
10. **Multi-company** - Test with different companies

## Test Anti-Patterns

### ❌ Testing Implementation Details

```python
# ❌ Testing internal state
def test_internal_value(self):
    self.assertEqual(record._internal_value, 5)

# ✅ Testing user-visible behavior
def test_display_name(self):
    self.assertEqual(record.display_name, 'Test (001)')
```

### ❌ Tests Depend on Order

```python
# ❌ Relying on previous test
def test_create(self):
    self.record = self.env['my.model'].create({'name': 'Test'})

def test_update(self):
    # Needs previous test
    self.record.write({'name': 'Updated'})

# ✅ Independent tests
def test_update(self):
    record = self.env['my.model'].create({'name': 'Test'})
    record.write({'name': 'Updated'})
    self.assertEqual(record.name, 'Updated')
```

## Test Checklist

Before considering tests complete:

- [ ] All public model methods have tests
- [ ] All HTTP controllers have tests
- [ ] Access rights are tested
- [ ] Record rules are tested
- [ ] Edge cases covered (null, empty, invalid)
- [ ] Error paths tested (not just happy path)
- [ ] Tests are independent (no shared state)
- [ ] Test names describe what's being tested
- [ ] Assertions are specific and meaningful
- [ ] Coverage is 80%+ (verify with coverage report)

## Running Tests

```bash
# Run specific test module
odoo -d test_db --test-enable --test-tags=test_module --stop-after-init

# Run all tests
odoo -d test_db --test-enable --stop-after-init

# Run with development mode
odoo -d test_db --test-enable --test-tags=test_module --dev=reload

# Run specific test class
odoo -d test_db --test-enable --test-tags=test_module.TestMyModel --stop-after-init

# Run specific test method
odoo -d test_db --test-enable --test-tags=test_module.TestMyModel.test_create --stop-after-init
```

## Common Odoo Test Patterns

### Create Test User

```python
def setUp(self):
    super(TestMyModel, self).setUp()
    self.user = self.env['res.users'].create({
        'name': 'Test User',
        'login': 'test@example.com',
        'email': 'test@example.com',
        'groups_id': [(6, 0, [self.env.ref('base.group_user').id])]
    })
```

### Create Test Record

```python
def test_record_creation(self):
    record = self.env['my.model'].create({
        'name': 'Test Record',
        'user_id': self.user.id,
        'value': 100,
    })
    self.assertTrue(record.id)
    self.assertEqual(record.name, 'Test Record')
```

### Test Search and Filter

```python
def test_search_and_filter(self):
    # Create test data
    record1 = self.env['my.model'].create({'name': 'Record 1', 'active': True})
    record2 = self.env['my.model'].create({'name': 'Record 2', 'active': False})

    # Test search
    active_records = self.env['my.model'].search([('active', '=', True)])
    self.assertIn(record1.id, active_records.ids)
    self.assertNotIn(record2.id, active_records.ids)

    # Test filter
    filtered_records = active_records.filtered(lambda r: '1' in r.name)
    self.assertEqual(len(filtered_records), 1)
    self.assertEqual(filtered_records[0].id, record1.id)
```

### Test Domain Expressions

```python
def test_domain_operators(self):
    record = self.env['my.model'].create({
        'name': 'Test',
        'value': 100,
    })

    # Test = operator
    result = self.env['my.model'].search([('value', '=', 100)])
    self.assertEqual(result.id, record.id)

    # Test > operator
    result = self.env['my.model'].search([('value', '>', 50)])
    self.assertEqual(result.id, record.id)

    # Test in operator
    result = self.env['my.model'].search([('id', 'in', [record.id])])
    self.assertEqual(result.id, record.id)
```

### Test Model Methods

```python
def test_model_methods(self):
    record = self.env['my.model'].create({
        'name': 'Test',
        'value': 100,
    })

    # Test write
    record.write({'value': 200})
    self.assertEqual(record.value, 200)

    # Test copy
    copy = record.copy()
    self.assertEqual(copy.name, 'Test (copy)')

    # Test unlink
    record_id = record.id
    record.unlink()
    not_found = self.env['my.model'].search([('id', '=', record_id)])
    self.assertFalse(not_found)
```

### Test Computed Fields

```python
def test_computed_field(self):
    record = self.env['my.model'].create({
        'name': 'Test',
        'value1': 10,
        'value2': 20,
    })
    # Computed field should be calculated
    self.assertEqual(record.compute_total, 30)

    # Test that computed field updates when dependencies change
    record.write({'value1': 20})
    self.assertEqual(record.compute_total, 40)
```

### Test Constraints

```python
def test_sql_constraint(self):
    # Create record with unique code
    record1 = self.env['my.model'].create({
        'name': 'Test',
        'code': 'A001',
    })

    # Try to create duplicate
    with self.assertRaises(Exception):
        self.env['my.model'].create({
            'name': 'Test 2',
            'code': 'A001',
        })

def test_python_constraint(self):
    # Test invalid data
    with self.assertRaises(Exception):
        self.env['my.model'].create({
            'name': 'Test',
            'start_date': '2024-12-31',
            'end_date': '2024-01-01',  # Invalid: end before start
        })
```

### Test Onchange Methods

```python
def test_onchange_behavior(self):
    record = self.env['my.model'].new({'value1': 10})

    # Trigger onchange
    result = record._onchange_value1()

    # Check result
    self.assertEqual(record.value2, 20)
    if result:
        self.assertIn('warning', result)
```

## Test Organization Rules

1. **One test class per major component** - Models, Controllers, Security
2. **Test methods grouped by functionality** - Create, Read, Update, Delete
3. **Use setUp for common setup** - Create test users and data
4. **Clean up in tearDown** - Remove test data if needed
5. **Use test fixtures** - For complex test data

## Performance Testing

```python
def test_search_performance(self):
    """Test that search is efficient"""
    # Create many records
    for i in range(1000):
        self.env['my.model'].create({
            'name': f'Record {i}',
            'active': i % 2 == 0,
        })

    # Test search performance
    import time
    start = time.time()
    records = self.env['my.model'].search([('active', '=', True)])
    elapsed = time.time() - start

    # Should be fast (under 1 second)
    self.assertLess(elapsed, 1.0)
    self.assertEqual(len(records), 500)
```
