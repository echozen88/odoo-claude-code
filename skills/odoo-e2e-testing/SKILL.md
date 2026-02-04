# Odoo 19 E2E Testing Guide

This skill provides comprehensive guidance for end-to-end testing of Odoo 19 modules using HttpCase and UI testing frameworks.

## Testing Framework Overview

### Test Types

| Test Type | Base Class | Purpose | Tags |
|-----------|------------|---------|------|
| Unit Test | TransactionCase | Model methods, constraints, business logic | None |
| Http Test | HttpCase | HTTP requests, controllers, JSON APIs | None |
| UI Test | HttpCase + browser | User interactions, form filling, click actions | None |
| E2E Test | HttpCase + browser | Complete workflows, multi-page scenarios | post_install, -at_install |

### Test Organization

```
tests/
├── __init__.py
├── test_model.py          # Model/unit tests
├── test_security.py       # Security/access tests
├── test_ui.py            # UI interaction tests
├── test_workflows.py      # E2E workflow tests
└── common.py             # Shared test utilities
```

## HttpCase Testing

### Basic HttpCase

```python
from odoo.tests import HttpCase, tagged

@tagged('post_install', '-at_install')
class TestHttpBasic(HttpCase):
    """Basic HTTP testing"""

    def test_homepage_accessible(self):
        """Test that homepage is accessible"""
        response = self.url_open('/web')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        """Test user login"""
        response = self.url_open('/web/login', data={
            'login': 'admin',
            'password': 'admin',
        })
        self.assertEqual(response.status_code, 200)

    def test_json_route(self):
        """Test JSON API endpoint"""
        # Authenticate first
        self.authenticate('admin', 'admin')

        # Call JSON route
        result = self.make_jsonrpc('/web/dataset/call_kw', {
            'model': 'res.users',
            'method': 'search_read',
            'args': [[['id', '=', self.env.user.id]]],
            'kwargs': {'fields': ['name', 'login']},
        })

        self.assertTrue(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Administrator')
```

### Form Submission Tests

```python
@tagged('post_install', '-at_install')
class TestFormSubmission(HttpCase):
    """Test form submissions"""

    def setUp(self):
        super(TestFormSubmission, self).setUp()
        # Create test data
        self.partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'email': 'test@example.com',
        })

    def test_create_record_via_form(self):
        """Test creating record via web form"""
        # Start tour or open form
        self.start_tour('/web', 'my_module_create_record', login='admin')

    def test_form_validation(self):
        """Test form client-side validation"""
        self.authenticate('admin', 'admin')
        response = self.url_open('/my_module/form')
        self.assertIn('validation-error', response.text)
```

### Controller Testing

```python
@tagged('post_install', '-at_install')
class TestControllers(HttpCase):
    """Test HTTP controllers"""

    def setUp(self):
        super(TestControllers, self).setUp()
        self.user = self.env['res.users'].create({
            'name': 'Test User',
            'login': 'testuser',
            'password': 'testpass123',
            'groups_id': [(6, 0, [self.env.ref('base.group_user').id])],
        })

    def test_public_route(self):
        """Test public route access"""
        response = self.url_open('/my_module/public')
        self.assertEqual(response.status_code, 200)

    def test_protected_route_requires_auth(self):
        """Test protected route redirects to login"""
        response = self.url_open('/my_module/protected')
        # Should redirect to login
        self.assertIn('/web/login', response.url)

    def test_user_route_with_auth(self):
        """Test user route with authentication"""
        self.authenticate(self.user.login, 'testpass123')
        response = self.url_open('/my_module/protected')
        self.assertEqual(response.status_code, 200)

    def test_json_endpoint(self):
        """Test JSON API endpoint"""
        self.authenticate('admin', 'admin')

        response = self.make_jsonrpc('/my_module/api/create', {
            'name': 'Test Record',
            'value': 100,
        })

        self.assertTrue(response.get('success'))
        self.assertIn('record_id', response)
```

## UI Testing with Browser

### Basic UI Test

```python
from odoo.tests import HttpCase, tagged
from odoo.tests.common import HOST, PORT

@tagged('post_install', '-at_install', 'ui')
class TestUIBasic(HttpCase):
    """Basic UI testing"""

    def test_load_module(self):
        """Test that module loads correctly"""
        self.start_tour('/web', 'my_module_tour', login='admin')

    def test_menu_accessible(self):
        """Test menu is accessible"""
        self.authenticate('admin', 'admin')

        # Click menu
        self.browser_js('/web', """
            return odoo.define('test', function (require) {
                'use strict';
                var core = require('web.core');
                var menu_data = core.get_menu_data();
                var module_menu = menu_data.children.filter(function (m) {
                    return m.id === 'my_module.menu_root';
                });
                return module_menu.length > 0;
            });
        """, "", 'MyModule')

    def test_tree_view_renders(self):
        """Test tree view renders correctly"""
        self.authenticate('admin', 'admin')

        # Check tree view loads
        self.browser_js('/web', """
            return odoo.define('test', function (require) {
                'use strict';
                return new Promise(function (resolve) {
                    var action = {
                        type: 'ir.actions.act_window',
                        res_model: 'my.model',
                        view_mode: 'tree',
                    };
                    odoo.do_action(action).then(function () {
                        resolve(true);
                    });
                });
            });
        """, "", 'MyModule')
```

### Form Interaction Tests

```python
@tagged('post_install', '-at_install', 'ui')
class TestFormInteraction(HttpCase):
    """Test form interactions"""

    def setUp(self):
        super(TestFormInteraction, self).setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Test Partner',
        })

    def test_create_record(self):
        """Test creating record from form"""
        self.authenticate('admin', 'admin')

        self.browser_js('/web', """
            return odoo.define('test', function (require) {
                'use strict';
                return new Promise(function (resolve) {
                    var model = require('web.Model');

                    // Create record
                    model.call('create', [{
                        name: 'Test Record',
                        partner_id: %d,
                    }]).then(function (record_id) {
                        resolve(record_id > 0);
                    });
                });
            });
        """ % self.partner.id, "", 'MyModule')

    def test_edit_record(self):
        """Test editing record"""
        record = self.env['my.model'].create({
            'name': 'Test Record',
        })

        self.authenticate('admin', 'admin')

        self.browser_js('/web', """
            return odoo.define('test', function (require) {
                'use strict';
                return new Promise(function (resolve) {
                    var model = require('web.Model');
                    model.call('write', [[%d], {name: 'Updated Name'}])
                        .then(function () {
                            resolve(true);
                        });
                });
            });
        """ % record.id, "", 'MyModule')

        # Verify update
        record.invalidate_cache()
        self.assertEqual(record.name, 'Updated Name')

    def test_form_validation(self):
        """Test form validation"""
        self.authenticate('admin', 'admin')

        # Test validation fails
        with self.assertRaises(Exception):
            self.env['my.model'].create({
                'code': '',  # Should fail constraint
            })
```

## E2E Workflow Testing

### Complete User Journey

```python
@tagged('post_install', '-at_install', 'ui')
class TestE2EWorkflows(HttpCase):
    """Test complete user workflows"""

    def setUp(self):
        super(TestE2EWorkflows, self).setUp()

        # Create test data
        self.customer = self.env['res.partner'].create({
            'name': 'Test Customer',
            'email': 'customer@example.com',
            'customer_rank': 1,
        })

        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'list_price': 100.0,
            'type': 'service',
        })

        self.user = self.env['res.users'].create({
            'name': 'Sales User',
            'login': 'salesuser',
            'password': 'password123',
            'groups_id': [(6, 0, [
                self.env.ref('base.group_user').id,
                self.env.ref('sales_team.group_sale_salesman').id,
            ])],
        })

    def test_create_and_confirm_order(self):
        """Test complete order creation and confirmation"""
        self.authenticate('salesuser', 'password123')

        # Step 1: Navigate to orders
        self.browser_js('/web', """
            return odoo.define('test', function (require) {
                'use strict';
                return new Promise(function (resolve) {
                    // Open order form
                    odoo.do_action({
                        type: 'ir.actions.act_window',
                        res_model: 'sale.order',
                        view_mode: 'form',
                    }).then(function () {
                        resolve(true);
                    });
                });
            });
        """, "", 'Sales')

        # Step 2: Create order programmatically
        order = self.env['sale.order'].with_user(self.user).create({
            'partner_id': self.customer.id,
            'order_line': [
                (0, 0, {
                    'product_id': self.product.id,
                    'product_uom_qty': 1.0,
                    'price_unit': 100.0,
                }),
            ],
        })

        # Step 3: Confirm order
        order.action_confirm()
        self.assertEqual(order.state, 'sale')

    def test_complete_customer_journey(self):
        """Test customer from lead to paid invoice"""
        # Create lead
        lead = self.env['crm.lead'].create({
            'name': 'New Lead',
            'contact_name': 'John Doe',
            'email_from': 'john@example.com',
        })

        # Convert to opportunity
        lead.convert_opportunity({
            'name': 'Test Opportunity',
            'planned_revenue': 5000,
        })

        # Create quotation from opportunity
        opportunity = self.env['crm.lead'].browse(lead.id)
        quotation = self.env['sale.order'].create({
            'partner_id': partner_id,
            'opportunity_id': opportunity.id,
            'order_line': [...],
        })

        # Confirm and create invoice
        quotation.action_confirm()
        invoice = quotation._create_invoices()
        invoice.action_post()

        # Verify payment
        payment = self.env['account.payment'].create({
            'payment_type': 'inbound',
            'partner_type': 'customer',
            'amount': invoice.amount_total,
            'currency_id': invoice.currency_id.id,
            'partner_id': invoice.partner_id.id,
            'destination_account_id': self.env['account.account'].search([
                ('user_type_id', '=', self.env.ref('account.data_account_type_current_assets').id),
            ], limit=1).id,
        })
        payment.action_post()
        payment.action_post()

        self.assertEqual(invoice.payment_state, 'paid')
```

### Multi-Step Workflow Test

```python
@tagged('post_install', '-at_install')
class TestMultiStepWorkflow(HttpCase):
    """Test multi-step workflows"""

    def test_approval_workflow(self):
        """Test document approval workflow"""
        manager = self.env['res.users'].create({
            'name': 'Manager',
            'login': 'manager',
            'groups_id': [(6, 0, [self.env.ref('my_module.group_manager').id])],
        })

        employee = self.env['res.users'].create({
            'name': 'Employee',
            'login': 'employee',
            'groups_id': [(6, 0, [self.env.ref('my_module.group_user').id])],
        })

        # Step 1: Employee submits request
        document = self.env['my.document'].with_user(employee).create({
            'name': 'Test Document',
            'description': 'Test content',
        })

        self.assertEqual(document.state, 'draft')

        # Step 2: Employee submits for approval
        document.action_submit()
        self.assertEqual(document.state, 'pending')

        # Step 3: Manager approves
        document.with_user(manager).action_approve()
        self.assertEqual(document.state, 'approved')

        # Step 4: Employee can edit again if rejected
        document.with_user(manager).action_reject()
        self.assertEqual(document.state, 'rejected')
        document.with_user(employee).write({'description': 'Updated'})
        self.assertEqual(document.state, 'rejected')

    def test_parallel_workflow(self):
        """Test parallel approval workflow"""
        # Create multiple approvers
        approver1 = self.env['res.users'].create({
            'name': 'Approver 1',
            'login': 'approver1',
        })
        approver2 = self.env['res.users'].create({
            'name': 'Approver 2',
            'login': 'approver2',
        })

        document = self.env['my.document'].create({
            'name': 'Test Document',
        })

        document.action_submit()

        # Both approvers need to approve
        approval1 = self.env['document.approval'].create({
            'document_id': document.id,
            'user_id': approver1.id,
        })
        approval2 = self.env['document.approval'].create({
            'document_id': document.id,
            'user_id': approver2.id,
        })

        # First approval
        approval1.action_approve()
        self.assertEqual(document.state, 'pending')

        # Second approval
        approval2.action_approve()
        self.assertEqual(document.state, 'approved')
```

## Permission Boundary Testing

### Access Rights Tests

```python
@tagged('post_install', '-at_install')
class TestAccessRights(HttpCase):
    """Test access rights and permissions"""

    def setUp(self):
        super(TestAccessRights, self).setUp()

        self.user = self.env['res.users'].create({
            'name': 'Test User',
            'login': 'testuser',
            'password': 'password123',
        })

        self.manager = self.env['res.users'].create({
            'name': 'Manager',
            'login': 'manager',
            'groups_id': [(6, 0, [self.env.ref('my_module.group_manager').id])],
        })

        # Create records
        self.user_record = self.env['my.model'].create({
            'name': 'User Record',
            'user_id': self.user.id,
        })

        self.other_record = self.env['my.model'].create({
            'name': 'Other Record',
            'user_id': self.manager.id,
        })

    def test_user_can_read_own(self):
        """Test user can read own records"""
        self.authenticate('testuser', 'password123')

        records = self.env['my.model'].with_user(self.user).search([])
        self.assertIn(self.user_record.id, records.ids)
        self.assertNotIn(self.other_record.id, records.ids)

    def test_user_cannot_delete_own(self):
        """Test user cannot delete own records (no unlink permission)"""
        self.authenticate('testuser', 'password123')

        with self.assertRaises(AccessError):
            self.user_record.with_user(self.user).unlink()

    def test_manager_can_delete(self):
        """Test manager can delete any record"""
        self.authenticate('manager', 'password123')

        record_id = self.user_record.id
        self.user_record.with_user(self.manager).unlink()

        self.assertFalse(self.env['my.model'].search([('id', '=', record_id)]))

    def test_group_based_access(self):
        """Test group-based access control"""
        # Remove user from module groups
        self.user.write({'groups_id': [(5, self.env.ref('my_module.group_user').id)]})

        self.authenticate('testuser', 'password123')

        with self.assertRaises(AccessError):
            self.env['my.model'].with_user(self.user).search([])
```

### Record Rule Tests

```python
@tagged('post_install', '-at_install')
class TestRecordRules(HttpCase):
    """Test record rules"""

    def setUp(self):
        super(TestRecordRules, self).setUp()

        self.user1 = self.env['res.users'].create({
            'name': 'User 1',
            'login': 'user1',
            'company_id': self.env.company.id,
        })

        self.user2 = self.env['res.users'].create({
            'name': 'User 2',
            'login': 'user2',
            'company_id': self.env.company.id,
        })

        company2 = self.env['res.company'].create({
            'name': 'Company 2',
        })

        self.user2.write({'company_id': company2.id})

        # Create records
        self.record1 = self.env['my.model'].create({
            'name': 'Record 1',
            'company_id': self.env.company.id,
        })

        self.record2 = self.env['my.model'].create({
            'name': 'Record 2',
            'company_id': company2.id,
        })

    def test_multi_company_isolation(self):
        """Test multi-company record isolation"""
        self.authenticate('user2', 'password123')

        # User2 should only see Company 2 records
        records = self.env['my.model'].with_user(self.user2).search([])
        self.assertIn(self.record2.id, records.ids)
        self.assertNotIn(self.record1.id, records.ids)
```

## Tour Testing

### Define a Tour

```xml
<!-- static/tours/my_tour.js -->
odoo.define('my_module.my_tour', function (require) {
    "use strict";

    var tour = require('web_tour.tour');
    var base = require('web_tour.tour_manager');

    tour.register('my_module_create_record', {
        url: '/web',
        test: true,
        rainbowMan: true,
    }, [
        {
            content: "Click on My Module menu",
            trigger: 'a:contains("My Module")',
        },
        {
            content: "Click Create",
            trigger: 'button.o_list_button_add',
        },
        {
            content: "Enter name",
            trigger: 'input[name="name"]',
            run: "text Test Record",
        },
        {
            content: "Select partner",
            trigger: 'div.o_field_many2one input',
            run: "text Test Partner",
        },
        {
            content: "Wait for partner selection",
            trigger: 'div.o_field_many2one_dropdown span:contains("Test Partner")',
            run: "click",
        },
        {
            content: "Click Save",
            trigger: 'button.o_form_button_save',
        },
        {
            content: "Record saved",
            trigger: '.o_notification_manager:contains("Record saved")',
        },
    ]);

    return tour;
});
```

### Run Tour in Test

```python
@tagged('post_install', '-at_install', 'tour')
class TestTours(HttpCase):
    """Test UI tours"""

    def test_my_module_tour(self):
        """Test complete UI tour"""
        self.start_tour('/web', 'my_module_create_record', login='admin')
```

## Common Test Patterns

### Data Setup Pattern

```python
class TestBase(TransactionCase):
    """Base test class with common setup"""

    @classmethod
    def setUpClass(cls):
        super(TestBase, cls).setUpClass()

        # Create common test data
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Partner',
            'email': 'test@example.com',
        })

        cls.product = cls.env['product.product'].create({
            'name': 'Test Product',
            'list_price': 100.0,
        })
```

### Assert Helper Pattern

```python
def assert_record_state(self, record, expected_state, message=None):
    """Assert record state"""
    self.assertEqual(
        record.state,
        expected_state,
        message or f"Expected state {expected_state}, got {record.state}"
    )

def assert_notification(self, notification_type, message=None):
    """Assert notification shown"""
    notification = self.browser.find_element(
        f'.o_notification_manager .o_notification_{notification_type}'
    )
    if message:
        self.assertIn(message, notification.text)
```

## Test Best Practices

### 1. Use Proper Tags

```python
# Tests requiring demo data
@tagged('post_install', '-at_install')

# Tests that require UI
@tagged('post_install', '-at_install', 'ui')

# Tests that require database
@tagged('post_install')

# Tests that can run at install
@tagged('-post_install', 'at_install')
```

### 2. Isolate Tests

```python
def test_method(self):
    """Each test should be independent"""
    # Don't rely on previous test state
    # Clean up after test
    records = self.env['my.model'].search([])
    records.unlink()
```

### 3. Use Meaningful Names

```python
def test_user_can_create_draft_orders(self):
    """Test case name should describe what's being tested"""
    pass

def test_manager_can_delete_cancelled_orders(self):
    """Include expected user and action"""
    pass

def test_validation_fails_for_empty_email(self):
    """Include expected condition"""
    pass
```

### 4. Assert Multiple Conditions

```python
def test_order_creation(self):
    """Test order creation with multiple validations"""
    order = self.env['sale.order'].create({...})

    # Multiple assertions
    self.assertTrue(order.id, 'Order should have ID')
    self.assertEqual(order.state, 'draft', 'Order should be in draft state')
    self.assertEqual(len(order.order_line), 1, 'Order should have one line')
    self.assertAlmostEqual(order.amount_total, 100.0, places=2)
```

### 5. Use setUp Properly

```python
def setUp(self):
    """Create fresh data for each test"""
    super().setUp()
    self.record = self.env['my.model'].create({'name': 'Test'})

@classmethod
def setUpClass(cls):
    """Create shared data once for all tests"""
    super().setUpClass()
    cls.shared_data = cls.env['my.model'].create({'name': 'Shared'})
```

## Troubleshooting Tests

### Common Test Failures

| Issue | Cause | Solution |
|-------|--------|----------|
| Record not found | Test isolation issue | Use setUp for fresh data |
| Access denied | Wrong user context | Use sudo() or with_user() |
| Timeout | Async operation issue | Use promises/correct async handling |
| Element not found | UI element missing | Check DOM structure, add waits |
| Assertion error | Unexpected state | Debug with print/log statements |

### Debug Tests

```python
def test_with_debug(self):
    """Test with debugging enabled"""
    import logging
    _logger = logging.getLogger(__name__)

    _logger.debug('Test starting')
    record = self.env['my.model'].create({'name': 'Test'})
    _logger.debug('Record created: %s', record.id)
    _logger.debug('Record state: %s', record.state)
```

**Remember:** Good tests are isolated, repeatable, fast, and meaningful. They verify behavior, not implementation details.
