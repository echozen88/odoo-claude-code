# Odoo 19 ORM Guide

This skill provides comprehensive guidance on using Odoo's Object-Relational Mapping (ORM) effectively.

## ORM Fundamentals

### Environment (env)

The `env` is your entry point to all ORM operations:

```python
# In model methods
self.env['model.name']  # Get model class

# In controllers
request.env['model.name']  # Get model class
```

### Model Methods

```python
# CRUD Operations
Model.create(vals)           # Create new record
Record.write(vals)            # Update record
Record.unlink()               # Delete record
Model.search(domain)           # Find records
Model.browse(ids)             # Get records by ID
Model.search_count(domain)    # Count records
Model.read(fields)            # Read specific fields
```

## Field Types

### Basic Fields

```python
from odoo import fields

# Character
name = fields.Char(string='Name', required=True, translate=True)
code = fields.Char(string='Code', size=32, copy=False)

# Text
description = fields.Text(string='Description')
notes = fields.Html(string='Notes')  # Rich text

# Boolean
active = fields.Boolean(string='Active', default=True)
is_published = fields.Boolean(string='Published')

# Integer
quantity = fields.Integer(string='Quantity', default=0)
priority = fields.Integer(string='Priority')

# Float
price = fields.Float(string='Price', digits=(14, 2))
rate = fields.Float(string='Rate', digits='Product Price')

# Monetary
amount = fields.Monetary(string='Amount', currency_field='currency_id')
total = fields.Monetary(string='Total', currency_field='currency_id')

# Date & Datetime
date_field = fields.Date(string='Date', default=fields.Date.today)
datetime_field = fields.Datetime(string='DateTime',
                                 default=fields.Datetime.now)

# Binary
image = fields.Binary(string='Image', attachment=True)
file = fields.Binary(string='File')

# Selection
state = fields.Selection([
    ('draft', 'Draft'),
    ('confirmed', 'Confirmed'),
    ('done', 'Done'),
], string='State', default='draft')

priority = fields.Selection([
    ('0', 'Low'),
    ('1', 'Normal'),
    ('2', 'High'),
], string='Priority')

# Reference
reference = fields.Reference(string='Reference',
                          selection=[
                              ('res.partner', 'Partner'),
                              ('sale.order', 'Sale Order'),
                          ])
```

### Relational Fields

```python
# Many2one (Foreign Key)
partner_id = fields.Many2one(
    'res.partner',
    string='Partner',
    ondelete='restrict',  # cascade, restrict, set null
    required=True,
    index=True,
)
company_id = fields.Many2one(
    'res.company',
    string='Company',
    default=lambda self: self.env.company,
)
user_id = fields.Many2one(
    'res.users',
    string='User',
    default=lambda self: self.env.user,
    domain="[('active', '=', True)]",
)

# One2many (Reverse relation)
line_ids = fields.One2many(
    'my.model.line',
    'order_id',  # Related Many2one field
    string='Lines',
)

# Many2many
tag_ids = fields.Many2many(
    'res.partner.category',
    'my_model_category_rel',  # Relation table
    'model_id',  # Column for this model
    'category_id',  # Column for related model
    string='Categories',
)
category_ids = fields.Many2many(
    'res.partner.category',
    string='Categories',
)
```

### Computed Fields

```python
# Simple computed
display_name = fields.Char(
    string='Display Name',
    compute='_compute_display_name',
    store=True,  # Store in database
)

@api.depends('name', 'code')
def _compute_display_name(self):
    for record in self:
        record.display_name = f"[{record.code}] {record.name}"

# Computed with search
my_date = fields.Date(
    string='My Date',
    compute='_compute_my_date',
    search='_search_my_date',
    inverse='_inverse_my_date',
    store=True,
)

@api.depends('date_field')
def _compute_my_date(self):
    for record in self:
        record.my_date = record.date_field

def _search_my_date(self, operator, value):
    if operator == '=':
        return [('date_field', '>=', value),
                ('date_field', '<', value + timedelta(days=1))]
    return []

def _inverse_my_date(self):
    for record in self:
        record.date_field = record.my_date

# Computed related field (shortcut)
partner_name = fields.Char(
    related='partner_id.name',
    string='Partner Name',
    store=True,
)
partner_city = fields.Char(
    related='partner_id.city',
    string='Partner City',
    store=False,  # Don't store, compute on read
)
```

## Search and Browse

### Search

```python
# Basic search
records = self.env['my.model'].search([])  # All records

# With domain
records = self.env['my.model'].search([
    ('active', '=', True),
    ('date', '>=', '2024-01-01'),
])

# Multiple conditions
records = self.env['my.model'].search([
    '&',
    ('active', '=', True),
    '|',
    ('state', '=', 'draft'),
    ('state', '=', 'confirmed'),
])

# With limit and order
records = self.env['my.model'].search(
    [('active', '=', True)],
    limit=10,
    order='date desc, name asc',
)

# With context
records = self.env['my.model'].with_context(
    lang='en_US',
    tz='UTC',
    active_test=False,  # Don't filter by active=True
).search([])
```

### Search Operators

```python
# Equality
('field', '=', value)
('field', '!=', value)

# Comparison
('field', '>', value)
('field', '>=', value)
('field', '<', value)
('field', '<=', value)

# Pattern matching
('field', 'like', '%pattern%')  # LIKE
('field', 'ilike', '%pattern%')  # Case-insensitive LIKE
('field', '=like', 'prefix%')  # Starts with
('field', '=ilike', 'prefix%')  # Case-insensitive starts with
('field', 'in', [value1, value2])
('field', 'not in', [value1, value2])

# Null checks
('field', '=', False)
('field', '!=', False)

# Set operations
('field', 'child_of', record_id)  # Recursive search

# Domain operators
'&'  # AND (default, implicit)
'|'  # OR
'!'  # NOT
```

### Browse

```python
# By ID
record = self.env['my.model'].browse(123)
record = self.env['my.model'].browse([123, 456, 789])

# By XML ID
record = self.env.ref('my_module.record_id')

# Empty recordset (for new records)
new_record = self.env['my.model'].browse([])

# From search
records = self.env['my.model'].search([])
# records is already browsed
```

### Search vs Browse

```python
# ❌ Wrong: Search then browse for single record
record = self.env['my.model'].browse(
    self.env['my.model'].search([('code', '=', 'ABC')]).id
)

# ✅ Correct: Search then browse for multiple
ids = self.env['my.model'].search([('code', '=', 'ABC')]).ids
records = self.env['my.model'].browse(ids)

# ✅ Or just use search
records = self.env['my.model'].search([('code', '=', 'ABC')])
# First record: records[0] or records.ensure_one()
```

## CRUD Operations

### Create

```python
# Single record
record = self.env['my.model'].create({
    'name': 'Test',
    'partner_id': partner.id,
    'line_ids': [
        (0, 0, {'name': 'Line 1', 'value': 100}),
        (0, 0, {'name': 'Line 2', 'value': 200}),
    ],
})

# Multiple records
records = self.env['my.model'].create([
    {'name': 'Record 1'},
    {'name': 'Record 2'},
])

# Using context for defaults
record = self.env['my.model'].with_context(
    default_active=True,
    default_partner_id=partner.id,
).create({'name': 'Test'})
```

### Write

```python
# Single record
record.write({'name': 'Updated'})

# Multiple records
records.write({'state': 'confirmed'})

# Conditional write
records.filtered(lambda r: r.state == 'draft').write({
    'state': 'confirmed',
})

# Writing relational fields
record.write({
    'partner_id': new_partner.id,  # Replace
    'tag_ids': [(6, 0, [tag1.id, tag2.id])],  # Replace all
    'tag_ids': [(4, tag1.id), (4, tag2.id)],  # Add without removing
    'tag_ids': [(3, tag1.id)],  # Remove one
    'line_ids': [
        (0, 0, {'name': 'New Line'}),  # Create
        (1, line.id, {'name': 'Updated'}),  # Update
        (2, old_line.id),  # Remove
        (4, existing_line.id),  # Add existing
    ],
})
```

### Unlink

```python
# Single record
record.unlink()

# Multiple records
records.unlink()

# Conditional
records.filtered(lambda r: not r.active).unlink()

# With check for related records
if records.mapped('line_ids'):
    raise UserError(_('Cannot delete records with lines'))
records.unlink()
```

### Copy

```python
# Copy record
new_record = record.copy({
    'name': _('(copy) %s') % record.name,
})

# Copy without default values
new_record = record.copy(default=False)
```

## Recordset Operations

```python
# Filtering
active_records = records.filtered('active')
high_priority = records.filtered(lambda r: r.priority >= 2)

# Mapping
partner_ids = records.mapped('partner_id')
line_ids = records.mapped('line_ids')

# Iteration
for record in records:
    print(record.name)

# Sorted
sorted_by_name = records.sorted('name')
sorted_by_date = records.sorted(lambda r: r.date, reverse=True)

# Checking membership
if record in records:
    print('Record exists')

# Length
count = len(records)

# Check if empty
if not records:
    print('No records')

# Single record
try:
    record = records.ensure_one()
except ValueError:
    print('Expected single record, got %s' % len(records))
```

## Context Manipulation

```python
# Suppress active filter
records = self.env['my.model'].with_context(active_test=False).search([])

# Switch company
records = self.env['my.model'].with_context(
    allowed_company_ids=[company1.id, company2.id]
).search([])

# Set user
records = self.env['my.model'].sudo(user.id).search([])

# Suppress access rights (USE CAREFULLY)
records = self.env['my.model'].sudo().search([])

# Add custom context
records = self.env['my.model'].with_context(
    custom_key='value',
).search([])
```

## Compute and Onchange

### Computed Fields

```python
@api.depends('field1', 'field2', 'line_ids.price')
def _compute_total(self):
    for record in self:
        record.total = record.field1 + record.field2
        record.total += sum(line.price for line in record.line_ids)
```

### Onchange Methods

```python
@api.onchange('partner_id')
def _onchange_partner_id(self):
    """Update fields when partner changes"""
    if self.partner_id:
        self.user_id = self.partner_id.user_id
        self.payment_term_id = self.partner_id.property_payment_term_id
        return {
            'warning': {
                'title': 'Partner Updated',
                'message': 'User and payment terms updated from partner',
            }
        }
    else:
        self.user_id = False
        self.payment_term_id = False

@api.onchange('product_id')
def _onchange_product_id(self):
    """Update price when product changes"""
    if self.product_id:
        self.price = self.product_id.list_price
        self.name = self.product_id.name
```

### Constraint Methods

```python
@api.constrains('date_start', 'date_end')
def _check_dates(self):
    for record in self:
        if record.date_end and record.date_start > record.date_end:
            raise ValidationError(_('Start date must be before end date'))

@api.constrains('code')
def _check_code(self):
    for record in self:
        if not record.code or len(record.code) < 3:
            raise ValidationError(_('Code must be at least 3 characters'))
```

## SQL Constraints

```python
_sql_constraints = [
    ('code_unique', 'UNIQUE(code)', 'Code must be unique!'),
    ('name_code_unique', 'UNIQUE(name, code)', 'Name+Code combination must be unique!'),
    ('positive_amount', 'CHECK(amount >= 0)', 'Amount must be positive!'),
]
```

## Default Values

```python
# Static default
active = fields.Boolean(string='Active', default=True)

# Computed default
@api.model
def _default_company(self):
    return self.env.company

company_id = fields.Many2one(
    'res.company',
    string='Company',
    default=_default_company,
)

# Lambda default (simpler)
company_id = fields.Many2one(
    'res.company',
    string='Company',
    default=lambda self: self.env.company,
)

user_id = fields.Many2one(
    'res.users',
    string='User',
    default=lambda self: self.env.user,
)

date_today = fields.Date(
    string='Date',
    default=fields.Date.today,
)
```

## Inheritance Patterns

### Class Extension

```python
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Add new field
    custom_field = fields.Char(string='Custom Field')

    # Extend existing method
    def action_confirm(self):
        # Add custom logic
        result = super(SaleOrder, self).action_confirm()
        # Post-processing
        return result
```

### Prototype Inheritance

```python
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _name = 'sale.order'

    # Add new field (same table)
    another_field = fields.Char(string='Another Field')
```

### Delegation Inheritance

```python
class MyModel(models.Model):
    _name = 'my.model'
    _inherits = {'partner_id': 'res.partner'}

    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        required=True,
        ondelete='cascade',
    )

    # Inherits all fields from partner_id
```

## Common ORM Patterns

### Get or Create

```python
@api.model
def get_or_create_by_code(self, code):
    record = self.search([('code', '=', code)], limit=1)
    if not record:
        record = self.create({'code': code})
    return record
```

### Update or Create

```python
@api.model
def update_or_create_by_external_id(self, external_id, vals):
    record = self.search([('external_id', '=', external_id)], limit=1)
    if record:
        record.write(vals)
    else:
        vals['external_id'] = external_id
        record = self.create(vals)
    return record
```

### Copy with Related Records

```python
def copy_data(self, default=None):
    if default is None:
        default = {}
    default['line_ids'] = [(0, 0, line.copy_data()) for line in self.line_ids]
    return super(MyModel, self).copy_data(default)
```

### Batch Processing

```python
@api.model
def _cron_process_records(self):
    """Process records in batches"""
    batch_size = 100
    offset = 0

    while True:
        records = self.search(
            [('state', '=', 'to_process')],
            limit=batch_size,
            offset=offset,
        )
        if not records:
            break

        for record in records:
            try:
                record.action_process()
            except Exception as e:
                _logger.error('Failed to process record %s: %s', record.id, e)

        offset += batch_size
```

## Performance Tips

1. **Use `search_read()` for specific fields** - Reduces data transfer
2. **Prefetch relational fields** - Odoo does this automatically
3. **Use `browse()` with IDs** - More efficient than search for known IDs
4. **Batch operations** - Process records in batches for large datasets
5. **Avoid loops with searches** - Use filtered() and mapped()
6. **Use `with_context()` carefully** - Don't nest too deep
7. **Use `sudo()` sparingly** - Only when absolutely necessary

## ORM Best Practices

1. **Always use ORM** - Avoid raw SQL unless performance critical
2. **Use proper decorators** - @api.model, @api.depends, etc.
3. **Handle empty recordsets** - Check `if not records` before operations
4. **Use `ensure_one()`** - When expecting exactly one record
5. **Translate strings** - Use `_()` for user-facing messages
6. **Use `write()` over single assignment** - Triggers only one write
7. **Consider `store=True` for computed fields** - Improves read performance
8. **Use `copy=False` on auto-increment fields** - Prevent duplicate values
