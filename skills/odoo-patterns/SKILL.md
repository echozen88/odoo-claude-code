# Odoo 19 Development Patterns

This skill provides comprehensive patterns and conventions for Odoo 19 module development.

## Module Structure

### Standard Odoo 19 Module Layout

```
odoo_module/
├── __manifest__.py           # Module manifest
├── __init__.py               # Python package init
├── models/                   # Model definitions
│   ├── __init__.py
│   ├── base_model.py         # Base models if needed
│   └── my_model.py
├── views/                    # XML view definitions
│   ├── my_model_views.xml
│   ├── templates.xml
│   └── menu.xml
├── security/                 # Access control
│   ├── ir.model.access.csv
│   └── security.xml
├── controllers/              # HTTP controllers
│   ├── __init__.py
│   ├── main.py
│   └── api.py
├── static/                  # Assets
│   ├── description/          # Module description
│   │   ├── icon.png
│   │   └── banner.png
│   ├── src/
│   │   ├── css/            # Stylesheets
│   │   ├── js/             # JavaScript
│   │   └── xml/            # QWeb templates
│   └── tests/
│       └── js/
│           └── tests.js
├── data/                    # XML data records
│   └── data.xml
├── demo/                    # Demo data
│   └── demo.xml
├── wizard/                  # Transient models
│   ├── __init__.py
│   └── my_wizard.py
├── report/                  # QWeb reports
│   ├── __init__.py
│   ├── report_template.xml
│   └── report.xml
├── tests/                   # Test modules
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_security.py
│   └── __manifest__.py      # Test manifest
├── i18n/                   # Translations
│   └── zh_CN.po
└── lib/                     # Utility libraries
    └── utils.py
```

## Naming Conventions

### Module Names
- Use lowercase with underscores: `my_custom_module`
- Keep it descriptive and short
- Avoid Odoo core module names

### Model Names
- Format: `module.model_name`
- Example: `sale.order`, `stock.picking`, `hr.employee`

### Field Names
- Many2one: `partner_id`, `user_id`, `company_id`
- One2many: `order_line_ids`, `move_line_ids`
- Many2many: `tag_ids`, `category_ids`
- Boolean: `is_active`, `has_permission`
- Date: `date_order`, `date_start`
- Computed: usually ends with property or specific name

### XML IDs
- Format: `module.resource_type.name`
- Views: `module.view_model_form`
- Menus: `module.menu_main`
- Actions: `module.action_model_action`
- Records: `module.record_name_default`

## Module Manifest Pattern

```python
{
    'name': 'My Custom Module',
    'version': '16.0.1.0.0',
    'category': 'Tools',
    'summary': 'Brief summary (shown in app list)',
    'description': """
        Long description using reStructuredText (RST).

        **Features:**
        - Feature 1
        - Feature 2
        - Feature 3
    """,
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
        'views/my_model_views.xml',
        'views/menu.xml',
        'data/data.xml',
        'wizard/my_wizard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'my_module/static/src/css/my_module.css',
            'my_module/static/src/js/my_module.js',
        ],
        'web.assets_frontend': [
            'my_module/static/src/css/frontend.css',
        ],
        'web.qunit_suite_tests': [
            'my_module/static/tests/js/tests.js',
        ],
    },
    'qweb': [
        'static/src/xml/templates.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
}
```

## Model Definition Patterns

### Basic Model

```python
from odoo import models, fields, api, _

class MyModel(models.Model):
    _name = 'my.model'
    _description = 'My Model'
    _order = 'name'
    _rec_name = 'display_name'

    # Fields
    name = fields.Char(required=True, translate=True, string='Name')
    code = fields.Char(string='Code', copy=False)
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', tracking=True)

    # Relational fields
    partner_id = fields.Many2one('res.partner', string='Partner',
                                  ondelete='restrict', required=True)
    company_id = fields.Many2one('res.company', string='Company',
                                  default=lambda self: self.env.company,
                                  required=True)
    user_id = fields.Many2one('res.users', string='User',
                             default=lambda self: self.env.user,
                             tracking=True)
    line_ids = fields.One2many('my.model.line', 'model_id',
                                string='Lines')
    tag_ids = fields.Many2many('res.partner.category', 'my_model_tag_rel',
                                'model_id', 'tag_id', string='Tags')

    # Computed fields
    display_name = fields.Char(compute='_compute_display_name',
                             store=True)

    @api.depends('name', 'code')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"[{record.code}] {record.name}"

    # SQL Constraints
    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Code must be unique!'),
        ('name_check', "CHECK(name != '')", 'Name cannot be empty'),
    ]

    # Python Constraints
    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_end and record.date_start > record.date_end:
                raise ValidationError(_('Start date must be before end date'))
```

### Model Inheritance

```python
# Class Extension (adding fields and methods)
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    custom_field = fields.Char(string='Custom Field')

    def action_confirm(self):
        # Add custom logic before/after
        result = super(SaleOrder, self).action_confirm()
        # Custom logic after
        return result

# Prototype Inheritance (adding fields only, same table)
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _name = 'sale.order'

    another_field = fields.Char(string='Another Field')
```

### Abstract Model

```python
class AbstractBase(models.AbstractModel):
    _name = 'abstract.base'
    _description = 'Abstract Base'

    name = fields.Char(string='Name')
    active = fields.Boolean(string='Active', default=True)

    def get_common_value(self):
        return self.name
```

### Transient Model (Wizard)

```python
class MyWizard(models.TransientModel):
    _name = 'my.wizard'
    _description = 'My Wizard'

    model_id = fields.Many2one('my.model', string='Model')
    field1 = fields.Char(string='Field 1')
    field2 = fields.Char(string='Field 2')

    def action_apply(self):
        # Wizard action
        for record in self:
            record.model_id.write({
                'custom_field': record.field1,
            })
        return {'type': 'ir.actions.act_window_close'}
```

## View Definition Patterns

### Tree View

```xml
<record id="view_my_model_tree" model="ir.ui.view">
    <field name="name">my.model.tree</field>
    <field name="model">my.model</field>
    <field name="arch" type="xml">
        <tree string="My Models" multi_edit="1" limit="80">
            <field name="name"/>
            <field name="code"/>
            <field name="partner_id"/>
            <field name="date"/>
            <field name="state" decoration-success="state == 'done'"
                    decoration-warning="state == 'confirmed'"
                    decoration-danger="state == 'cancelled'"/>
            <button name="action_confirm" string="Confirm"
                    type="object" class="btn-primary"
                    states="draft"/>
            <button name="action_cancel" string="Cancel"
                    type="object" class="btn-secondary"
                    states="draft,confirmed"/>
        </tree>
    </field>
</record>
```

### Form View

```xml
<record id="view_my_model_form" model="ir.ui.view">
    <field name="name">my.model.form</field>
    <field name="model">my.model</field>
    <field name="arch" type="xml">
        <form string="My Model">
            <header>
                <button name="action_draft" string="Set to Draft"
                        type="object" states="confirmed,done"/>
                <button name="action_confirm" string="Confirm"
                        type="object" states="draft" class="btn-primary"/>
                <field name="state" widget="statusbar"/>
            </header>
            <sheet>
                <div class="oe_title">
                    <field name="code" placeholder="Code"/>
                    <h1><field name="name" placeholder="Name"/></h1>
                </div>
                <group>
                    <group>
                        <field name="partner_id"/>
                        <field name="date"/>
                        <field name="company_id" groups="base.group_multi_company"/>
                    </group>
                    <group>
                        <field name="user_id"/>
                        <field name="active"/>
                    </group>
                </group>
                <notebook>
                    <page string="Details">
                        <group>
                            <field name="description" nolabel="1"/>
                        </group>
                    </page>
                    <page string="Lines">
                        <field name="line_ids">
                            <tree editable="bottom">
                                <field name="name"/>
                                <field name="value"/>
                            </tree>
                        </field>
                    </page>
                    <page string="Extra Info">
                        <group>
                            <field name="tag_ids" widget="many2many_tags"/>
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
```

### Kanban View

```xml
<record id="view_my_model_kanban" model="ir.ui.view">
    <field name="name">my.model.kanban</field>
    <field name="model">my.model</field>
    <field name="arch" type="xml">
        <kanban default_group_by="state" quick_create="false">
            <field name="name"/>
            <field name="partner_id"/>
            <templates>
                <t t-name="kanban-box">
                    <div class="oe_kanban_card">
                        <div class="oe_kanban_content">
                            <strong><field name="name"/></strong>
                            <div><field name="partner_id"/></div>
                        </div>
                        <div class="oe_kanban_bottom_right">
                            <button name="action_confirm" type="object"
                                    class="btn-primary">
                                Confirm
                            </button>
                        </div>
                    </div>
                </t>
            </templates>
        </kanban>
    </field>
</record>
```

### Pivot View

```xml
<record id="view_my_model_pivot" model="ir.ui.view">
    <field name="name">my.model.pivot</field>
    <field name="model">my.model</field>
    <field name="arch" type="xml">
        <pivot string="My Model Analysis">
            <field name="date" interval="month" type="row"/>
            <field name="partner_id" type="col"/>
            <field name="value" type="measure" sum="1"/>
        </pivot>
    </field>
</record>
```

### Graph View

```xml
<record id="view_my_model_graph" model="ir.ui.view">
    <field name="name">my.model.graph</field>
    <field name="model">my.model</field>
    <field name="arch" type="xml">
        <graph string="My Model Chart">
            <field name="date" type="row"/>
            <field name="value" type="measure"/>
        </graph>
    </field>
</record>
```

## View Inheritance Patterns

### Extending Form View

```xml
<record id="view_sale_order_form_inherit" model="ir.ui.view">
    <field name="name">sale.order.form.inherit</field>
    <field name="model">sale.order</field>
    <field name="inherit_id" ref="sale.view_order_form"/>
    <field name="arch" type="xml">
        <field name="partner_id" position="after">
            <field name="custom_field"/>
        </field>

        <xpath expr="//field[@name='order_line']/tree/field[@name='price_unit']" position="after">
            <field name="custom_line_field"/>
        </xpath>

        <xpath expr="//form/sheet/group" position="inside">
            <group string="Custom Info">
                <field name="another_custom_field"/>
            </group>
        </xpath>
    </field>
</record>
```

### Position Values
- `after` - Insert after target
- `before` - Insert before target
- `inside` - Insert inside target
- `replace` - Replace target
- `attributes` - Modify target attributes

## Controller Patterns

### Basic HTTP Controller

```python
from odoo import http
from odoo.http import request

class MyController(http.Controller):

    @http.route('/my/page', type='http', auth='public', website=True)
    def my_page(self, **kwargs):
        values = {
            'user': request.env.user,
            'is_public': request.env.user == request.env.ref('base.public_user'),
        }
        return request.render('my_module.template', values)

    @http.route('/my/api/data', type='json', auth='user')
    def my_api(self, **kwargs):
        data = kwargs.get('data')
        result = self.env['my.model'].search([])
        return {
            'success': True,
            'data': result.read(['name', 'value']),
        }

    @http.route('/my/action', type='http', methods=['POST'],
                auth='user', csrf=True)
    def my_action(self, **kwargs):
        # CSRF protected POST action
        result = request.params.get('result')
        return request.redirect('/my/page')
```

## Action Patterns

### Window Action

```xml
<record id="action_my_model" model="ir.actions.act_window">
    <field name="name">My Models</field>
    <field name="res_model">my.model</field>
    <field name="view_mode">tree,form</field>
    <field name="view_id" ref="view_my_model_tree"/>
    <field name="domain">[('active', '=', True)]</field>
    <field name="context">{'default_active': True}</field>
    <field name="limit">80</field>
</record>
```

### Server Action

```xml
<record id="action_my_model_compute" model="ir.actions.server">
    <field name="name">Compute My Model</field>
    <field name="model_id" ref="model_my_model"/>
    <field name="state">code</field>
    <field name="code">
records.search([]).action_compute()
    </field>
</record>
```

### Client Action

```xml
<record id="action_my_module_client" model="ir.actions.client">
    <field name="name">My Module Client Action</field>
    <field name="tag">reload</field>
</record>
```

## Menu Patterns

```xml
<menuitem id="menu_my_root"
          name="My Module"
          sequence="10"
          web_icon="my_module,static/description/icon.png"/>

<menuitem id="menu_my_models"
          name="My Models"
          parent="menu_my_root"
          action="action_my_model"
          sequence="10"/>

<menuitem id="menu_my_reports"
          name="Reports"
          parent="menu_my_root"
          sequence="20"/>
```

## Common Patterns

### Workflow State Machine

```python
class MyModel(models.Model):
    _name = 'my.model'
    state = fields.Selection([...], default='draft', tracking=True)

    def action_draft(self):
        for record in self:
            if record.state != 'cancelled':
                raise UserError(_('Only cancelled records can be reset to draft'))
        self.write({'state': 'draft'})

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_done(self):
        for record in self:
            if not record.partner_id:
                raise UserError(_('Partner is required'))
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})
```

### Chatter Integration

```python
class MyModel(models.Model):
    _name = 'my.model'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Now has message_ids, message_follower_ids, activity_ids
```

### Multi-Company Support

```python
class MyModel(models.Model):
    _name = 'my.model'

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True,
    )

    @api.model
    def _read_group_company_field(self):
        return 'company_id'

    # Record rules automatically respect company_id
```

### Sequences

```python
class MyModel(models.Model):
    _name = 'my.model'

    name = fields.Char(string='Reference', required=True, copy=False,
                    readonly=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('my.model')
        return super(MyModel, self).create(vals)
```

### Attachments

```python
class MyModel(models.Model):
    _name = 'my.model'

    attachment_ids = fields.One2many(
        'ir.attachment',
        'res_id',
        domain=lambda self: [('res_model', '=', self._name)],
        string='Attachments',
    )
```

## Best Practices

1. **Always use ORM** - Avoid raw SQL unless absolutely necessary
2. **Use decorators** - @api.model, @api.depends, @api.constrains
3. **Translate user strings** - Use _() for translatable strings
4. **Follow naming conventions** - Model, field, view names
5. **Plan security first** - Access rights and record rules
6. **Test thoroughly** - Unit tests, security tests, integration tests
7. **Document code** - Docstrings for public methods
8. **Handle errors** - Try/except with user-friendly messages
9. **Use proper inheritance** - _inherit for extensions, _inherits for delegation
10. **Think multi-company** - Company field and rules when needed
