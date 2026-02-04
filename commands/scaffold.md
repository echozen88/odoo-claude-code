# Scaffold Command

Generate Odoo 19 module scaffolding with proper structure and templates.

## Usage

```
/scaffold <module-name> [options]
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--include-views` | Include tree/form view templates | No |
| `--include-security` | Include access rights and record rules | Yes |
| `--include-tests` | Include test module structure | Yes |
| `--include-controllers` | Include controller templates | No |
| `--dependencies` | Specify module dependencies (comma-separated) | base, web |
| `--model` | Specify initial model name | module_name |
| `--author` | Module author | Your Company |
| `--license` | Module license | LGPL-3 |

## Examples

```
# Basic module
/scaffold my_module

# Module with views
/scaffold my_module --include-views

# Module with everything
/scaffold my_module --include-views --include-controllers --model=custom.model

# Module with specific dependencies
/scaffold my_module --dependencies=sale,purchase,stock --model=sale.order.custom

# Full module specification
/scaffold crm_extended --include-views --include-tests --include-controllers \
    --dependencies=crm,sale,mail --model=crm.lead.extended \
    --author="My Company" --license="LGPL-3"
```

## Generated Structure

```
module_name/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── model_name.py
├── views/
│   ├── model_name_views.xml
│   └── menu.xml
├── security/
│   ├── ir.model.access.csv
│   └── security.xml
├── controllers/
│   ├── __init__.py
│   └── main.py
├── wizard/
│   └── __init__.py
├── report/
│   └── __init__.py
├── data/
│   └── data.xml
├── demo/
│   └── demo_data.xml
├── static/
│   ├── description/
│   │   ├── icon.png
│   │   └── banner.png
│   └── src/
│       ├── css/
│       │   └── module_name.css
│       ├── js/
│       │   └── module_name.js
│       └── xml/
│           └── templates.xml
├── tests/
│   ├── __init__.py
│   ├── test_model_name.py
│   └── test_security.py
└── __pycache__/
```

## Template Files

### __manifest__.py

```python
{
    'name': 'Module Name',
    'version': '19.0.1.0.0',
    'category': 'Tools',
    'summary': 'Brief description of the module',
    'description': '''
Long description of the module
    ''',
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'web',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/module_name_views.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'module_name/static/src/css/module_name.css',
            'module_name/static/src/js/module_name.js',
        ],
        'web.assets_frontend': [
            'module_name/static/src/js/module_name.js',
        ],
    },
    'qweb': [
        'static/src/xml/templates.xml',
    ],
    'images': [
        'static/description/icon.png',
        'static/description/banner.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
```

### models/model_name.py

```python
from odoo import models, fields, api


class ModelName(models.Model):
    _name = 'module.model_name'
    _description = 'Model Name'

    name = fields.Char(string='Name', required=True, translate=True)
    code = fields.Char(string='Code', copy=False, index=True)
    active = fields.Boolean(string='Active', default=True)
    description = fields.Text(string='Description')
    notes = fields.Html(string='Notes')

    date = fields.Date(string='Date', default=fields.Date.today)
    datetime = fields.Datetime(string='Date & Time', default=fields.Datetime.now)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', required=True)

    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        ondelete='restrict',
        required=True,
        index=True,
    )
    user_id = fields.Many2one(
        'res.users',
        string='User',
        default=lambda self: self.env.user,
        index=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True,
        index=True,
    )

    line_ids = fields.One2many(
        'module.model_name.line',
        'model_id',
        string='Lines',
    )
    tag_ids = fields.Many2many(
        'res.partner.category',
        'module_model_name_tag_rel',
        'model_id',
        'tag_id',
        string='Tags',
    )

    # Computed fields
    total = fields.Float(
        string='Total',
        compute='_compute_total',
        store=True,
    )
    line_count = fields.Integer(
        string='Line Count',
        compute='_compute_line_count',
    )

    @api.depends('line_ids.total')
    def _compute_total(self):
        for record in self:
            record.total = sum(line.total for line in record.line_ids)

    def _compute_line_count(self):
        for record in self:
            record.line_count = len(record.line_ids)

    # Constraints
    @api.constrains('code')
    def _check_code(self):
        for record in self:
            if not record.code or len(record.code) < 3:
                raise ValidationError(_('Code must be at least 3 characters'))

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Code must be unique!'),
        ('name_unique', 'UNIQUE(name)', 'Name must be unique!'),
    ]

    # Actions
    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_draft(self):
        self.write({'state': 'draft'})

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('module.model_name')
        return super(ModelName, self).create(vals)

    def write(self, vals):
        return super(ModelName, self).write(vals)

    def unlink(self):
        for record in self:
            if record.state == 'done':
                raise ValidationError(_('Cannot delete done records'))
        return super(ModelName, self).unlink()


class ModelNameLine(models.Model):
    _name = 'module.model_name.line'
    _description = 'Model Name Line'

    name = fields.Char(string='Description', required=True)
    model_id = fields.Many2one(
        'module.model_name',
        string='Model',
        required=True,
        ondelete='cascade',
        index=True,
    )
    sequence = fields.Integer(string='Sequence', default=10)

    product_id = fields.Many2one(
        'product.product',
        string='Product',
    )
    quantity = fields.Float(string='Quantity', default=1.0)
    price = fields.Float(string='Price', digits='Product Price')
    total = fields.Float(
        string='Total',
        compute='_compute_total',
        store=True,
    )

    @api.depends('quantity', 'price')
    def _compute_total(self):
        for line in self:
            line.total = line.quantity * line.price
```

### views/module_name_views.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <!-- Tree View -->
    <record id="view_module_model_name_tree" model="ir.ui.view">
        <field name="name">module.model_name.tree</field>
        <field name="model">module.model_name</field>
        <field name="arch" type="xml">
            <tree string="Model Names"
                  limit="80"
                  default_order="date desc"
                  multi_edit="1">
                <field name="name"/>
                <field name="code"/>
                <field name="partner_id"/>
                <field name="date"/>
                <field name="total" sum="Total"/>
                <field name="state"
                        decoration-success="state == 'done'"
                        decoration-warning="state == 'confirmed'"
                        decoration-danger="state == 'cancelled'"
                        decoration-muted="state == 'cancelled'"/>
                <button name="action_confirm" string="Confirm"
                        type="object" class="btn-primary"
                        icon="fa-check" states="draft"/>
                <button name="action_done" string="Done"
                        type="object" class="btn-primary"
                        icon="fa-check-double" states="confirmed"/>
                <button name="action_cancel" string="Cancel"
                        type="object" class="btn-secondary"
                        icon="fa-times" states="draft,confirmed"/>
            </tree>
        </field>
    </record>

    <!-- Form View -->
    <record id="view_module_model_name_form" model="ir.ui.view">
        <field name="name">module.model_name.form</field>
        <field name="model">module.model_name</field>
        <field name="arch" type="xml">
            <form string="Model Name">
                <header>
                    <button name="action_draft" string="Set to Draft"
                            type="object" states="confirmed,done,cancelled"/>
                    <button name="action_confirm" string="Confirm"
                            type="object" states="draft" class="btn-primary"/>
                    <button name="action_done" string="Done"
                            type="object" states="confirmed" class="btn-primary"/>
                    <button name="action_cancel" string="Cancel"
                            type="object" class="btn-secondary"/>
                    <field name="state" widget="statusbar"
                            statusbar_visible="draft,confirmed,done"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <label for="code" class="oe_edit_only"/>
                        <h1><field name="code" placeholder="Code"/></h1>
                        <h2><field name="name" placeholder="Name"/></h2>
                    </div>
                    <group>
                        <group string="Main Information">
                            <field name="partner_id"/>
                            <field name="date"/>
                            <field name="user_id"/>
                        </group>
                        <group string="Configuration">
                            <field name="company_id"
                                    groups="base.group_multi_company"/>
                            <field name="active"/>
                            <field name="state"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Details">
                            <group>
                                <field name="description"/>
                            </group>
                        </page>
                        <page string="Lines">
                            <field name="line_ids">
                                <tree editable="bottom">
                                    <field name="sequence" widget="handle"/>
                                    <field name="name"/>
                                    <field name="product_id"/>
                                    <field name="quantity"/>
                                    <field name="price"/>
                                    <field name="total" sum="Total"/>
                                </tree>
                            </field>
                        </page>
                        <page string="Extra Info">
                            <group>
                                <field name="tag_ids" widget="many2many_tags"/>
                                <field name="notes" widget="text"/>
                            </group>
                        </page>
                    </notebook>
                </sheet>
                <div class="oe_chatter">
                    <field name="message_ids" widget="mail_thread"/>
                </div>
            </form>
        </field>
    </record>

    <!-- Search View -->
    <record id="view_module_model_name_search" model="ir.ui.view">
        <field name="name">module.model_name.search</field>
        <field name="model">module.model_name</field>
        <field name="arch" type="xml">
            <search string="Search Model Name">
                <field name="name"/>
                <field name="code"/>
                <field name="partner_id"/>
                <field name="date"/>
                <field name="state"/>
                <filter string="Active" name="active"
                        domain="[('active', '=', True)]"/>
                <filter string="Draft" name="draft"
                        domain="[('state', '=', 'draft')]"/>
                <filter string="Confirmed" name="confirmed"
                        domain="[('state', '=', 'confirmed')]"/>
                <filter string="Done" name="done"
                        domain="[('state', '=', 'done')]"/>
                <separator/>
                <filter string="This Month" name="this_month"
                        domain="[('date', '>=', (context_today() - relativedelta(months=1)).strftime('%%Y-%%m-01')),
                                ('date', '<=', (context_today()).strftime('%%Y-%%m-%%d'))]"/>
                <filter string="This Year" name="this_year"
                        domain="[('date', '>=', (context_today()).strftime('%%Y-01-01')),
                                ('date', '<=', (context_today()).strftime('%%Y-12-31'))]"/>
                <separator/>
                <group expand="0" string="Group By">
                    <filter string="Partner" name="group_partner"
                            context="{'group_by': 'partner_id'}"/>
                    <filter string="State" name="group_state"
                            context="{'group_by': 'state'}"/>
                    <filter string="Date" name="group_date"
                            context="{'group_by': 'date:month'}"/>
                    <filter string="User" name="group_user"
                            context="{'group_by': 'user_id'}"/>
                </group>
            </search>
        </field>
    </record>

    <!-- Pivot View -->
    <record id="view_module_model_name_pivot" model="ir.ui.view">
        <field name="name">module.model_name.pivot</field>
        <field name="model">module.model_name</field>
        <field name="arch" type="xml">
            <pivot string="Model Name Analysis">
                <field name="date" interval="month" type="row"/>
                <field name="partner_id" type="col"/>
                <field name="state" type="col"/>
                <field name="total" type="measure"/>
            </pivot>
        </field>
    </record>

    <!-- Graph View -->
    <record id="view_module_model_name_graph" model="ir.ui.view">
        <field name="name">module.model_name.graph</field>
        <field name="model">module.model_name</field>
        <field name="arch" type="xml">
            <graph string="Model Name Chart" type="bar" stacked="1">
                <field name="date" type="row"/>
                <field name="partner_id" type="col"/>
                <field name="total" type="measure"/>
            </graph>
        </field>
    </record>
</odoo>
```

### views/menu.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <!-- Root Menu -->
    <menuitem id="menu_module_root"
              name="Module Name"
              sequence="10"
              web_icon="module_name,static/description/icon.png"
              groups="base.group_user"/>

    <!-- Models Menu -->
    <menuitem id="menu_module_model_names"
              name="Model Names"
              parent="menu_module_root"
              action="action_module_model_name"
              sequence="10"/>

    <!-- Configuration Menu -->
    <menuitem id="menu_module_configuration"
              name="Configuration"
              parent="menu_module_root"
              sequence="20"
              groups="base.group_system"/>
</odoo>
```

### security/ir.model.access.csv

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_module_model_name_user,module.model.name,model_module_model_name,base.group_user,1,1,1,0
access_module_model_name_manager,module.model.name,model_module_model_name,module_name.group_manager,1,1,1,1
access_module_model_name_line_user,module.model.name.line,model_module_model_name_line,base.group_user,1,1,1,0
access_module_model_name_line_manager,module.model.name.line,model_module_model_name_line,module_name.group_manager,1,1,1,1
```

### security/security.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <data noupdate="1">
        <!-- Security Groups -->
        <record id="group_module_user" model="res.groups">
            <field name="name">Module User</field>
            <field name="category_id" ref="base.module_category_tools"/>
            <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
            <field name="comment">Basic access to Module Name</field>
        </record>

        <record id="group_module_manager" model="res.groups">
            <field name="name">Module Manager</field>
            <field name="category_id" ref="base.module_category_tools"/>
            <field name="implied_ids" eval="[(4, ref('group_module_user'))]"/>
            <field name="comment">Full access to Module Name including delete</field>
        </record>

        <!-- Record Rules -->
        <record id="rule_module_model_name_user_own" model="ir.rule">
            <field name="name">Module Model Name: User Records Only</field>
            <field name="model_id" ref="model_module_model_name"/>
            <field name="domain_force">[('user_id', '=', user.id)]</field>
            <field name="groups" eval="[(4, ref('base.group_user'))]"/>
            <field name="perm_read" eval="True"/>
            <field name="perm_write" eval="True"/>
            <field name="perm_create" eval="True"/>
            <field name="perm_unlink" eval="False"/>
        </record>

        <record id="rule_module_model_name_manager_all" model="ir.rule">
            <field name="name">Module Model Name: Manager All Records</field>
            <field name="model_id" ref="model_module_model_name"/>
            <field name="domain_force">[(1, '=', 1)]</field>
            <field name="groups" eval="[(4, ref('group_module_manager'))]"/>
        </record>

        <!-- Sequence -->
        <record id="seq_module_model_name" model="ir.sequence">
            <field name="name">Module Model Name</field>
            <field name="code">module.model_name</field>
            <field name="prefix">MNO/</field>
            <field name="padding">5</field>
            <field name="number_next">1</field>
            <field name="number_increment">1</field>
        </record>
    </data>
</odoo>
```

### controllers/main.py

```python
from odoo import http
from odoo.http import request


class ModuleController(http.Controller):

    @http.route('/module/page', type='http', auth='user', website=True)
    def module_page(self, **kwargs):
        values = {}
        records = request.env['module.model_name'].search([
            ('active', '=', True),
        ], limit=10)
        values['records'] = records
        return request.render('module_name.website_template', values)

    @http.route('/module/api/data', type='json', auth='user')
    def module_api_data(self, **kwargs):
        data = kwargs.get('data')
        record = request.env['module.model_name'].create(data)
        return {
            'success': True,
            'record_id': record.id,
        }
```

### static/src/js/module_name.js

```javascript
odoo.define('module_name.MyComponent', function (require) {
    "use strict";

    const { Component, useState, onMounted } = owl;
    const { registry } = require('web.core');
    const { useService } = require('web.custom_hooks');

    class MyComponent extends Component {
        setup() {
            this.orm = useService('orm');
            this.state = useState({
                records: [],
                loading: true,
            });

            onMounted(this.loadRecords.bind(this));
        }

        async loadRecords() {
            this.state.records = await this.orm.searchRead(
                'module.model_name',
                [],
                ['name', 'code', 'date', 'state']
            );
            this.state.loading = false;
        }
    }

    MyComponent.template = 'module_name.MyComponent';
    MyComponent.props = {
        recordId: { type: Number, optional: true },
    };

    registry.category('actions').add('module_name.my_component', MyComponent);
    return MyComponent;
});
```

### static/src/xml/templates.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates xml:space="preserve">
    <t t-name="module_name.MyComponent" owl="1">
        <div class="o_module_component">
            <h2>Module Records</h2>
            <div t-if="state.loading">Loading...</div>
            <ul t-else="">
                <li t-foreach="state.records" t-as="record">
                    <t t-esc="record.name"/>
                    (<t t-esc="record.code"/>)
                </li>
            </ul>
        </div>
    </t>

    <t t-name="module_name.website_template">
        <t t-call="website.layout">
            <div id="wrap" class="oe_structure oe_empty">
                <h1>Module Name</h1>
                <div class="container">
                    <div class="row">
                        <div class="col-md-12">
                            <div class="card">
                                <div class="card-body">
                                    <h5 class="card-title">Recent Records</h5>
                                    <ul class="list-group">
                                        <t t-foreach="records" t-as="record">
                                            <li class="list-group-item">
                                                <a t-attf-href="/module/records/{{ record.id }}">
                                                    <t t-esc="record.name"/>
                                                </a>
                                            </li>
                                        </t>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </t>
    </t>
</templates>
```

### tests/test_model_name.py

```python
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestModelName(TransactionCase):
    """Test Model Name"""

    def setUp(self):
        super(TestModelName, self).setUp()
        self.Model = self.env['module.model_name']

    def test_create_record(self):
        """Test creating a record"""
        record = self.Model.create({
            'name': 'Test Record',
            'code': 'TEST001',
            'partner_id': self.env['res.partner'].create({
                'name': 'Test Partner'
            }).id,
        })
        self.assertTrue(record)
        self.assertEqual(record.name, 'Test Record')
        self.assertEqual(record.code, 'TEST001')
        self.assertEqual(record.state, 'draft')

    def test_state_flow(self):
        """Test state workflow"""
        partner = self.env['res.partner'].create({'name': 'Test Partner'})
        record = self.Model.create({
            'name': 'Test',
            'code': 'TEST',
            'partner_id': partner.id,
        })

        # Draft to Confirmed
        record.action_confirm()
        self.assertEqual(record.state, 'confirmed')

        # Confirmed to Done
        record.action_done()
        self.assertEqual(record.state, 'done')

        # Done back to Draft
        record.action_draft()
        self.assertEqual(record.state, 'draft')

    def test_computed_total(self):
        """Test computed total field"""
        partner = self.env['res.partner'].create({'name': 'Test Partner'})
        record = self.Model.create({
            'name': 'Test',
            'code': 'TEST',
            'partner_id': partner.id,
        })

        # Add lines
        record.write({
            'line_ids': [
                (0, 0, {
                    'name': 'Line 1',
                    'quantity': 2,
                    'price': 10,
                }),
                (0, 0, {
                    'name': 'Line 2',
                    'quantity': 3,
                    'price': 20,
                }),
            ],
        })

        # Check total
        self.assertEqual(record.total, 80)  # 2*10 + 3*20

    def test_code_unique_constraint(self):
        """Test code unique constraint"""
        partner = self.env['res.partner'].create({'name': 'Test Partner'})
        self.Model.create({
            'name': 'Test 1',
            'code': 'UNIQUE',
            'partner_id': partner.id,
        })

        with self.assertRaises(Exception):
            self.Model.create({
                'name': 'Test 2',
                'code': 'UNIQUE',  # Same code
                'partner_id': partner.id,
            })

    def test_cannot_delete_done_records(self):
        """Test that done records cannot be deleted"""
        partner = self.env['res.partner'].create({'name': 'Test Partner'})
        record = self.Model.create({
            'name': 'Test',
            'code': 'TEST',
            'partner_id': partner.id,
        })
        record.action_done()

        with self.assertRaises(Exception):
            record.unlink()
```

### tests/test_security.py

```python
from odoo.tests import TransactionCase, tagged
from odoo.exceptions import AccessError


@tagged('post_install', '-at_install')
class TestSecurity(TransactionCase):
    """Test Module Security"""

    def setUp(self):
        super(TestSecurity, self).setUp()
        self.Model = self.env['module.model_name']

        # Create users
        self.user = self.env['res.users'].create({
            'name': 'Test User',
            'login': 'test@example.com',
            'groups_id': [(6, 0, [self.env.ref('base.group_user').id])],
        })
        self.manager = self.env['res.users'].create({
            'name': 'Test Manager',
            'login': 'manager@example.com',
            'groups_id': [(6, 0, [self.env.ref('module_name.group_manager').id])],
        })

        # Create records
        partner = self.env['res.partner'].create({'name': 'Test Partner'})
        self.user_record = self.Model.sudo().create({
            'name': 'User Record',
            'code': 'USR001',
            'partner_id': partner.id,
            'user_id': self.user.id,
        })
        self.other_record = self.Model.sudo().create({
            'name': 'Other Record',
            'code': 'OTH001',
            'partner_id': partner.id,
        })

    def test_user_can_read_own_records(self):
        """Test users can read their own records"""
        record = self.user_record.with_user(self.user)
        self.assertTrue(bool(record))
        self.assertEqual(record.user_id, self.user)

    def test_user_cannot_read_other_records(self):
        """Test users cannot read other users' records"""
        records = self.Model.with_user(self.user).search([])
        self.assertNotIn(self.other_record.id, records.ids)

    def test_manager_can_read_all_records(self):
        """Test managers can read all records"""
        records = self.Model.with_user(self.manager).search([])
        self.assertIn(self.user_record.id, records.ids)
        self.assertIn(self.other_record.id, records.ids)

    def test_user_cannot_delete_own(self):
        """Test users cannot delete records (unlink permission)"""
        with self.assertRaises(AccessError):
            self.user_record.with_user(self.user).unlink()

    def test_manager_can_delete_records(self):
        """Test managers can delete records"""
        record_id = self.user_record.id
        self.user_record.with_user(self.manager).unlink()
        self.assertFalse(self.Model.search([('id', '=', record_id)]))
```

## Next Steps

After scaffolding:

1. **Rename files and classes** to match your specific module name
2. **Customize the model** fields and methods
3. **Update views** to match your requirements
4. **Configure security** groups and record rules as needed
5. **Add custom controllers** for web routes
6. **Write tests** for your specific functionality
7. **Add custom static assets** (CSS, JS, images)
8. **Update module description** and documentation
9. **Test the module** thoroughly before deployment
10. **Create install guide** and user documentation

## Odoo Naming Conventions

| Type | Convention | Example |
|------|-------------|---------|
| Module directory | `lowercase_with_underscores` | `my_module` |
| Model name | `module.model_name` | `my_module.my_model` |
| Class name | `CamelCase` | `MyModel` |
| XML ID | `module.view_name` | `my_module.view_my_form` |
| Python files | `lowercase.py` | `my_model.py` |
| Python methods | `lowercase_with_underscores` | `my_method` |
| Field names | `lowercase_with_underscores` | `my_field` |
| Many2one | `name_id` | `partner_id` |
| One2many | `name_ids` | `line_ids` |
| Many2many | `name_ids` | `tag_ids` |
