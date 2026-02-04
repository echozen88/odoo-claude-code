# Odoo 19 Coding Style Rules

## Python Code Style (PEP8)

### Indentation and Formatting

- **Use 4 spaces for indentation** (no tabs)
- **Maximum line length**: 100 characters (Odoo preference, not 79)
- **Import order**: Standard library, third-party, local imports
- **Two blank lines** between top-level definitions
- **One blank line** between method definitions

```python
# ✅ Correct
from datetime import datetime

from odoo import models, fields, api

from . import utils


class MyModel(models.Model):
    """My model docstring."""

    _name = 'my.model'

    name = fields.Char(string='Name')


    @api.model
    def my_method(self):
        """Method docstring."""
        return self.search([])

# ❌ Incorrect - single quotes vs double quotes
# Odoo prefers single quotes for strings
name = "Name"
```

### Naming Conventions

**Classes**: PascalCase
```python
class MyModel(models.Model):
    pass
```

**Methods**: snake_case
```python
def calculate_total(self):
    pass
```

**Variables**: snake_case
```python
total_amount = 0
```

**Constants**: UPPER_CASE
```python
DEFAULT_LIMIT = 80
MAX_RETRY = 3
```

**Private methods**: _leading_underscore
```python
def _internal_method(self):
    pass
```

### Docstrings

- **Class docstrings**: Describe what the class does
- **Method docstrings**: Describe parameters, return value, and behavior

```python
# ✅ Correct
class MyModel(models.Model):
    """My Model description.

    This model represents custom data for the application.
    """

    _name = 'my.model'

    @api.model
    def calculate_total(self, records):
        """Calculate total for records.

        Args:
            records (recordset): The records to calculate total for

        Returns:
            float: The calculated total
        """
        return sum(record.value for record in records)

# ❌ Incorrect - no docstring
class MyModel(models.Model):
    _name = 'my.model'

    def calculate_total(self, records):
        return sum(record.value for record in records)
```

## Odoo-Specific Conventions

### Model Definition

```python
# ✅ Correct model structure
from odoo import models, fields, api, _

class MyModel(models.Model):
    _name = 'my.model'
    _description = 'My Model'
    _order = 'name'
    _rec_name = 'display_name'

    name = fields.Char(required=True, translate=True, string='Name')
    active = fields.Boolean(string='Active', default=True)

    @api.model
    def create(self, vals):
        # Call super to create record
        result = super(MyModel, self).create(vals)
        return result

# ❌ Incorrect - missing _description
class MyModel(models.Model):
    _name = 'my.model'
```

### Field Definitions

```python
# ✅ Correct field definition
name = fields.Char(
    required=True,
    translate=True,
    string='Name',
    help='The name of the record',
)

partner_id = fields.Many2one(
    'res.partner',
    string='Partner',
    ondelete='restrict',
    required=True,
)

line_ids = fields.One2many(
    'my.model.line',
    'model_id',
    string='Lines',
)

total = fields.Float(
    string='Total',
    compute='_compute_total',
    store=True,
)

@api.depends('line_ids.price')
def _compute_total(self):
    for record in self:
        record.total = sum(line.price for line in record.line_ids)

# ❌ Incorrect - missing string attribute
name = fields.Char(required=True)
```

### API Decorator Usage

```python
# ✅ Correct decorator usage
@api.model
def model_method(self):
    pass

@api.depends('field1', 'field2')
def _compute_total(self):
    pass

@api.onchange('field')
def _onchange_field(self):
    pass

@api.constrains('date')
def _check_date(self):
    pass

# ❌ Incorrect - missing decorator
def _compute_total(self):
    pass
```

### Translatable Strings

```python
# ✅ Correct - use _() for user-facing strings
from odoo import _

raise UserError(_('This is an error message'))
warning = _('Warning: Invalid value')
description = _('Record description')

# ❌ Incorrect - hardcoded strings
raise UserError('This is an error message')
```

## File Organization

### Module Structure

```
odoo_module/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── my_model.py
├── views/
│   └── my_model_views.xml
├── security/
│   ├── ir.model.access.csv
│   └── security.xml
└── controllers/
    └── main.py
```

### Import Organization

```python
# ✅ Correct import order
# Standard library
from datetime import datetime, timedelta

# Third-party
from dateutil.relativedelta import relativedelta

# Odoo
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

# Local
from . import utils
from . import my_other_model

# ❌ Incorrect - mixed order
from odoo import models
from datetime import datetime
from . import utils
```

## XML File Conventions

### View Definitions

```xml
<!-- ✅ Correct XML structure -->
<odoo>
    <data>
        <record id="view_my_model_form" model="ir.ui.view">
            <field name="name">my.model.form</field>
            <field name="model">my.model</field>
            <field name="arch" type="xml">
                <form string="My Model">
                    <sheet>
                        <group>
                            <field name="name"/>
                        </group>
                    </sheet>
                </form>
            </field>
        </record>
    </data>
</odoo>

<!-- ❌ Incorrect - missing closing tags -->
<odoo>
    <data>
        <record id="view_my_model_form" model="ir.ui.view">
            <field name="name">my.model.form</field>
```

### XML IDs

```xml
<!-- ✅ Correct XML ID format -->
<!-- module.view_name -->
<record id="view_my_model_form" model="ir.ui.view"/>

<!-- module.menu_name -->
<menuitem id="menu_my_root" name="My Module"/>

<!-- module.action_name -->
<record id="action_my_model" model="ir.actions.act_window"/>

<!-- ❌ Incorrect - wrong prefix -->
<record id="my_view" model="ir.ui.view"/>
```

## Code Quality Rules

### Error Handling

```python
# ✅ Correct - specific exception handling
try:
    result = self._external_call()
except ConnectionError as e:
    _logger.error('Connection failed: %s', e)
    raise UserError(_('Connection failed. Please try again.'))
except Exception as e:
    _logger.exception('Unexpected error: %s', e)
    raise UserError(_('An error occurred. Please contact support.'))

# ❌ Incorrect - bare except
try:
    result = self._external_call()
except:
    pass
```

### Logging

```python
# ✅ Correct logging
import logging

_logger = logging.getLogger(__name__)

_logger.info('Processing record %s', record.id)
_logger.warning('Warning: %s', message)
_logger.error('Error: %s', error)
_logger.exception('Exception occurred: %s', error)

# ❌ Incorrect - no logging
pass
```

### Model Methods

```python
# ✅ Correct - always call super()
class MyModel(models.Model):
    _name = 'my.model'

    def create(self, vals):
        # Add default values
        vals['state'] = 'draft'
        # Call super
        return super(MyModel, self).create(vals)

# ❌ Incorrect - not calling super()
class MyModel(models.Model):
    _name = 'my.model'

    def create(self, vals):
        # Missing super() call
        return self.env['my.model'].new(vals)
```

## Performance Considerations

```python
# ✅ Correct - use filtered()
active_records = records.filtered('active')
high_priority = records.filtered(lambda r: r.priority >= 2)

# ✅ Correct - use mapped()
partner_ids = records.mapped('partner_id')
total = sum(records.mapped('value'))

# ❌ Incorrect - loop with search
for record in records:
    line = self.env['my.line'].search([('model_id', '=', record.id)])
```

## Forbidden Patterns

### Never Use Direct SQL Without Justification

```python
# ❌ FORBIDDEN: Direct SQL for simple queries
self.env.cr.execute("SELECT * FROM my_model WHERE id = %s", (id,))

# ✅ Use ORM instead
record = self.env['my.model'].browse(id)
```

### Never Use sudo() Without Justification

```python
# ❌ FORBIDDEN: Unnecessary sudo()
def action_approve(self):
    self.sudo().write({'state': 'approved'})

# ✅ Only sudo for technical operations
def action_cleanup(self):
    # Technical cleanup requiring bypass
    self.sudo()._cleanup_old_records()
```

### Never Hardcode IDs

```python
# ❌ FORBIDDEN: Hardcoded IDs
group_id = 1

# ✅ Use XML ID references
group_id = self.env.ref('base.group_user').id
```

## Code Review Checklist

Before considering code complete:

- [ ] PEP8 compliant (run `pylint --py3k`)
- [ ] All classes have docstrings
- [ ] All public methods have docstrings
- [ ] API decorators used correctly
- [ ] Translatable strings use `_()`
- [ ] No hardcoded secrets
- [ ] Error handling in place
- [ ] Logging for errors
- [ ] Super() called in overrides
- [ ] No bare except clauses
- [ ] No unnecessary sudo()
- [ ] ORM used instead of raw SQL
- [ ] File size under 800 lines
- [ ] Method size under 50 lines
