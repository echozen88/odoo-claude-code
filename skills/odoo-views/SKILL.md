# Odoo 19 Views Guide

This skill provides comprehensive guidance on creating and customizing Odoo views.

## View Types

### Tree View (List)

```xml
<record id="view_my_model_tree" model="ir.ui.view">
    <field name="name">my.model.tree</field>
    <field name="model">my.model</field>
    <field name="arch" type="xml">
        <tree string="My Models" multi_edit="1" limit="80"
              editable="bottom" default_order="name">
            <field name="name"/>
            <field name="code"/>
            <field name="partner_id"/>
            <field name="date"/>
            <field name="amount" sum="Total"/>
            <field name="state"
                    decoration-success="state == 'done'"
                    decoration-warning="state == 'confirmed'"
                    decoration-danger="state == 'cancelled'"
                    decoration-muted="state == 'cancelled'"/>
            <button name="action_confirm" string="Confirm"
                    type="object" class="btn-primary"
                    icon="fa-check"
                    states="draft"/>
            <button name="action_cancel" string="Cancel"
                    type="object" class="btn-secondary"
                    icon="fa-times"
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
                <button name="action_done" string="Done"
                        type="object" states="confirmed" class="btn-primary"/>
                <button name="action_cancel" string="Cancel"
                        type="object" class="btn-secondary"/>
                <button name="%(my_module.action_report)d" string="Print"
                        type="action" class="btn-secondary"/>
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
                        <field name="company_id" groups="base.group_multi_company"/>
                        <field name="active"/>
                        <field name="state"/>
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
                                <field name="product_id"/>
                                <field name="quantity"/>
                                <field name="price"/>
                                <field name="total" sum="Total"/>
                                <button name="action_remove" string="Remove"
                                        type="object" icon="fa-trash"/>
                            </tree>
                        </field>
                    </page>
                    <page string="Extra Info">
                        <group>
                            <field name="tag_ids" widget="many2many_tags"/>
                            <field name="note" widget="text"/>
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
        <kanban default_group_by="state" quick_create="false"
               class="o_kanban_small_column">
            <field name="name"/>
            <field name="partner_id"/>
            <field name="date"/>
            <templates>
                <t t-name="kanban-box">
                    <div class="oe_kanban_card">
                        <div class="oe_kanban_content">
                            <div class="oe_kanban_title">
                                <strong><field name="name"/></strong>
                            </div>
                            <div class="oe_kanban_body">
                                <field name="partner_id"/>
                            </div>
                            <div class="oe_kanban_footer">
                                <div class="oe_kanban_left">
                                    <span t-esc="record.date"/>
                                </div>
                                <div class="oe_kanban_right">
                                    <button name="action_confirm" type="object"
                                            class="btn-primary btn-sm">
                                        Confirm
                                    </button>
                                </div>
                            </div>
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
            <field name="state" type="col"/>
            <field name="amount" type="measure"/>
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
        <graph string="My Model Chart" type="bar" stacked="1">
            <field name="date" type="row"/>
            <field name="partner_id" type="col"/>
            <field name="amount" type="measure"/>
        </graph>
    </field>
</record>
```

### Calendar View

```xml
<record id="view_my_model_calendar" model="ir.ui.view">
    <field name="name">my.model.calendar</field>
    <field name="model">my.model</field>
    <field name="arch" type="xml">
        <calendar string="My Calendar" date_start="date_start"
                  date_stop="date_stop" color="state"
                  mode="month" quick_add="True">
            <field name="name"/>
            <field name="partner_id"/>
            <field name="state"/>
        </calendar>
    </field>
</record>
```

### Search View

```xml
<record id="view_my_model_search" model="ir.ui.view">
    <field name="name">my.model.search</field>
    <field name="model">my.model</field>
    <field name="arch" type="xml">
        <search string="Search My Model">
            <field name="name"/>
            <field name="code"/>
            <field name="partner_id"/>
            <field name="date"/>
            <field name="state"/>
            <filter string="Active" name="active" domain="[('active', '=', True)]"/>
            <filter string="Draft" name="draft"
                    domain="[('state', '=', 'draft')]"/>
            <filter string="Confirmed" name="confirmed"
                    domain="[('state', '=', 'confirmed')]"/>
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
            </group>
        </search>
    </field>
</record>
```

## View Inheritance

### Extending Form View

```xml
<record id="view_sale_order_form_inherit" model="ir.ui.view">
    <field name="name">sale.order.form.inherit</field>
    <field name="model">sale.order</field>
    <field name="inherit_id" ref="sale.view_order_form"/>
    <field name="arch" type="xml">
        <!-- Add field after another field -->
        <field name="partner_id" position="after">
            <field name="custom_field"/>
        </field>

        <!-- Use xpath for precise targeting -->
        <xpath expr="//field[@name='order_line']/tree/field[@name='price_unit']"
                 position="after">
            <field name="custom_line_field"/>
        </xpath>

        <!-- Add group inside sheet -->
        <xpath expr="//form/sheet/group" position="inside">
            <group string="Custom Info">
                <field name="another_custom_field"/>
            </group>
        </xpath>

        <!-- Replace element -->
        <xpath expr="//field[@name='state']" position="replace">
            <field name="state" widget="radio"/>
        </xpath>

        <!-- Add before element -->
        <xpath expr="//button[@name='action_confirm']" position="before">
            <button name="action_custom" string="Custom Action"
                    type="object" class="btn-secondary"/>
        </xpath>
    </field>
</record>
```

### Extending Tree View

```xml
<record id="view_sale_order_tree_inherit" model="ir.ui.view">
    <field name="name">sale.order.tree.inherit</field>
    <field name="model">sale.order</field>
    <field name="inherit_id" ref="sale.view_order_tree"/>
    <field name="arch" type="xml">
        <field name="name" position="after">
            <field name="custom_field"/>
        </field>

        <!-- Add button -->
        <field name="state" position="before">
            <button name="action_custom" string="Custom"
                    type="object" icon="fa-star"/>
        </field>
    </field>
</record>
```

## Field Widgets

### Standard Widgets

```xml
<!-- Text widgets -->
<field name="description" widget="text" placeholder="Description"/>
<field name="notes" widget="text" rows="3"/>

<!-- Selection widgets -->
<field name="state" widget="selection"/>
<field name="state" widget="radio" options="{'horizontal': true}"/>
<field name="state" widget="statusbar" statusbar_visible="draft,confirmed,done"/>

<!-- Date widgets -->
<field name="date" widget="date" options="{'picker': {}}"/>
<field name="datetime" widget="datetime"/>

<!-- Relational widgets -->
<field name="partner_id" widget="many2one"/>
<field name="tag_ids" widget="many2many_tags"/>
<field name="user_id" widget="many2one_avatar"/>
<field name="image" widget="image"/>

<!-- Special widgets -->
<field name="website" widget="url"/>
<field name="email" widget="email"/>
<field name="phone" widget="phone"/>
<field name="monetary" widget="monetary" options="{'currency_field': 'currency_id'}"/>
<field name="percent" widget="percentage"/>
<field name="priority" widget="priority"/>
<field name="toggle" widget="boolean_toggle"/>
<field name="handle" widget="handle"/>
<field name="reference" widget="reference"/>
```

### Widget Options

```xml
<!-- Selection widget options -->
<field name="state" widget="selection" options="{'no_open': true}"/>

<!-- Many2one options -->
<field name="partner_id" widget="many2one"
        options="{'no_create': true, 'no_quick_create': true}"/>

<!-- Many2many tags options -->
<field name="tag_ids" widget="many2many_tags"
        options="{'color_field': 'color', 'no_create_edit': true}"/>

<!-- Monetary options -->
<field name="amount" widget="monetary"
        options="{'currency_field': 'currency_id', 'field_digits': [14, 2]}"/>

<!-- Date options -->
<field name="date" widget="date"
        options="{'picker': {'maxDate': '%Y-%m-%d'}}"/>

<!-- Text options -->
<field name="description" widget="text"
        options="{'style-side': 'right', 'max-height': 200}"/>
```

## QWeb Templates

### Basic Template

```xml
<template id="template_my_module" name="My Template">
    <t t-call="website.layout">
        <div id="wrap" class="oe_structure oe_empty">
            <h1>My Module Page</h1>
            <p>Welcome to My Module</p>
            <t t-foreach="records" t-as="record">
                <div>
                    <h2 t-esc="record.name"/>
                    <p t-esc="record.description"/>
                </div>
            </t>
        </div>
    </t>
</template>
```

### QWeb Directives

```xml
<!-- Escape content -->
<t t-esc="value"/>

<!-- Raw content (use carefully) -->
<t t-raw="html_content"/>

<!-- Render if condition -->
<t t-if="condition">
    <p>Content</p>
</t>

<!-- Render else -->
<t t-if="condition">
    <p>If true</p>
</t>
<t t-else="">
    <p>If false</p>
</t>

<!-- Loop -->
<t t-foreach="items" t-as="item">
    <p t-esc="item.name"/>
    <p>Index: <t t-esc="item_index"/></p>
    <p>First: <t t-esc="item_first"/></p>
    <p>Last: <t t-esc="item_last"/></p>
</t>

<!-- Set variable -->
<t t-set="variable" t-value="expression"/>
<p>Variable: <t t-esc="variable"/></p>

<!-- Call another template -->
<t t-call="module.template_name">
    <t t-set="param1" t-value="value1"/>
    <t t-set="param2" t-value="value2"/>
</t>

<!-- Attribute manipulation -->
<a t-att-href="url" t-att-class="{'active': is_active}">Link</a>
<input t-att-value="value" t-att-placeholder="placeholder"/>

<!-- JavaScript execution (website only) -->
<t t-javascript="">
    // JS code here
</t>
```

### QWeb Asset Bundles

```xml
<template id="assets_frontend" inherit_id="web.assets_frontend" name="My Module Assets">
    <xpath expr="." position="inside">
        <link rel="stylesheet"
              href="/my_module/static/src/css/my_module.css"/>
        <script type="text/javascript"
                src="/my_module/static/src/js/my_module.js"/>
    </xpath>
</template>

<template id="assets_backend" inherit_id="web.assets_backend" name="My Module Backend Assets">
    <xpath expr="." position="inside">
        <link rel="stylesheet"
              href="/my_module/static/src/css/my_module.css"/>
        <script type="text/javascript"
                src="/my_module/static/src/js/my_module.js"/>
    </xpath>
</template>
```

## Actions

### Window Action

```xml
<record id="action_my_model" model="ir.actions.act_window">
    <field name="name">My Models</field>
    <field name="res_model">my.model</field>
    <field name="view_mode">tree,form,pivot</field>
    <field name="view_id" ref="view_my_model_tree"/>
    <field name="domain">[('active', '=', True)]</field>
    <field name="context">{'default_active': True, 'search_default_draft': 1}</field>
    <field name="limit">80</field>
    <field name="target">current</field>
</record>
```

### Server Action

```xml
<record id="action_my_model_compute" model="ir.actions.server">
    <field name="name">Compute My Model</field>
    <field name="model_id" ref="model_my_model"/>
    <field name="state">code</field>
    <field name="code">
# Check for records to process
records = env['my.model'].search([('state', '=', 'to_process')])
if records:
    records.action_process()
    # Send notification
    message = records._message_post(
        body=f'{len(records)} records processed',
        message_type='notification',
    )
    </field>
</record>
```

### Client Action

```xml
<record id="action_my_module_client" model="ir.actions.client">
    <field name="name">My Module Client Action</field>
    <field name="tag">reload</field>
    <field name="params">
        <key name="menu_id">my_module.menu_main</key>
    </field>
</record>
```

### URL Action

```xml
<record id="action_my_module_url" model="ir.actions.url">
    <field name="name">Open Website</field>
    <field name="url">https://www.example.com</field>
    <field name="target">new</field>
</record>
```

### Report Action

```xml
<report id="report_my_model_pdf"
        name="my.model.report.pdf"
        model="my.model"
        report_type="qweb-pdf"
        string="My Model Report"
        file="my_model_report"
        attachment_use="True"
        attachment="(object.state == 'done' and ('PDF-' + object.code + '.pdf'))"/>
```

## Menus

### Menu Structure

```xml
<menuitem id="menu_my_root"
          name="My Module"
          sequence="10"
          web_icon="my_module,static/description/icon.png"
          groups="base.group_user"/>

<menuitem id="menu_my_models"
          name="My Models"
          parent="menu_my_root"
          action="action_my_model"
          sequence="10"/>

<menuitem id="menu_my_reports"
          name="Reports"
          parent="menu_my_root"
          sequence="20"/>

<menuitem id="menu_my_report1"
          name="Report 1"
          parent="menu_my_reports"
          action="action_my_report1"
          sequence="10"/>
```

## View Best Practices

1. **Use proper groups** - Restrict fields/groups based on user roles
2. **Enable multi-edit** - Use `multi_edit="1"` for commonly modified fields
3. **Use decorations** - Color-code records for better UX
4. **Add states** - Show/hide buttons based on record state
5. **Use placeholders** - Guide users on expected input
6. **Optimize tree views** - Only show essential columns, use detail views for more
7. **Use proper widgets** - Choose widgets that match field purpose
8. **Handle empty states** - Show helpful messages when no records
9. **Test responsive design** - Ensure views work on different screen sizes
10. **Use QWeb properly** - Always escape user content with `t-esc`

## View Performance Tips

1. **Limit tree view records** - Use `limit` attribute
2. **Use default_order** - Sort efficiently at database level
3. **Avoid expensive fields** - Computed fields without store=True in lists
4. **Use field views** - Create detail views for complex records
5. **Optimize search domains** - Use indexed fields
6. **Cache results** - Use context for frequently used values
