# Odoo 19 OWL (Odoo Web Library) Guide

This skill provides comprehensive guidance for developing OWL components in Odoo 19. OWL is the primary frontend framework used in Odoo 19 for building interactive UI components.

## OWL Fundamentals

### What is OWL?

OWL (Odoo Web Library) is a reactive JavaScript framework built by Odoo. It features:
- Component-based architecture
- Reactive state management
- Efficient reactivity system with fine-grained updates
- Template syntax for declarative UI
- Built-in hooks for lifecycle management

### File Structure

```javascript
// static/src/js/my_component.js
odoo.define('my_module.MyComponent', function (require) {
    "use strict";

    const { Component, useState, onMounted, onWillUnmount } = owl;
    const { registry } = require('web.core');
    const { useService } = require('web.custom_hooks');

    class MyComponent extends Component {
        setup() {
            // Component setup
        }
    }

    MyComponent.template = 'my_module.MyComponent';
    MyComponent.props = {
        recordId: { type: Number, optional: true },
        mode: { type: String, optional: true },
    };

    registry.category('actions').add('my_module.my_component_action', MyComponent);
    return MyComponent;
});

// static/src/xml/my_component.xml
<templates xml:space="preserve">
    <t t-name="my_module.MyComponent" owl="1">
        <div class="my-component">
            <!-- Component content -->
        </div>
    </t>
</templates>
```

## Component Lifecycle

### Lifecycle Hooks

```javascript
const { Component, useState, onMounted, onWillUnmount, onWillStart, onWillUpdate, onPatched, onWillRender, onRendered, onWillDestroyProps } = owl;

class MyComponent extends Component {
    setup() {
        this.state = useState({
            count: 0,
            loading: false,
        });

        onWillStart(async () => {
            // Called once before first render
            await this.loadData();
        });

        onMounted(() => {
            // Called after first render, DOM is available
            console.log('Component mounted');
        });

        onWillUpdate(() => {
            // Called before each update (after first render)
        });

        onWillRender(() => {
            // Called before each render
        });

        onRendered(() => {
            // Called after each render
        });

        onPatched(() => {
            // Called after DOM is patched
        });

        onWillUnmount(() => {
            // Cleanup before component is unmounted
            this.cleanup();
        });

        onWillDestroyProps(() => {
            // Called when props are about to be destroyed
        });
    }
}
```

### Lifecycle Execution Order

1. **Component creation** → `setup()` is called
2. **Before first render** → `onWillStart()`
3. **Before render** → `onWillRender()`
4. **Render** → Template is rendered
5. **After render** → `onRendered()`
6. **After DOM insertion** → `onMounted()`
7. **On state change** → `onWillRender()` → Render → `onRendered()` → `onPatched()`
8. **On unmount** → `onWillUnmount()` → `onWillDestroyProps()`

## State Management

### useState Hook

```javascript
class MyComponent extends Component {
    setup() {
        // Simple state
        this.state = useState({
            count: 0,
            name: '',
            records: [],
        });

        // Nested state
        this.formState = useState({
            fields: {
                name: '',
                email: '',
            },
            errors: {},
        });
    }

    increment() {
        // State mutations trigger re-render
        this.state.count++;
    }

    updateRecords(newRecords) {
        // Replace entire array
        this.state.records = newRecords;
    }

    addRecord(record) {
        // Add to array (triggers re-render)
        this.state.records.push(record);
    }
}
```

### useStore Hook (Enterprise)

```javascript
const { useStore } = require('web.custom_hooks');

class MyComponent extends Component {
    setup() {
        // Connect to store (Enterprise feature)
        this.store = useStore();

        // Define store fields
        this.modelName = 'my.model';
        this.fields = ['name', 'date', 'state'];
        this.domain = [['active', '=', true]];
    }
}
```

## Props Handling

### Defining Props

```javascript
class MyComponent extends Component {
    // Define props schema
    static props = {
        // Required prop
        recordId: { type: Number },

        // Optional prop
        mode: { type: String, optional: true },

        // Default value
        readonly: { type: Boolean, optional: true },

        // Complex validation
        config: {
            type: Object,
            optional: true,
            validate: (config) => {
                return config && typeof config === 'object';
            }
        },

        // Array prop
        items: { type: Array, element: String, optional: true },

        // Any type
        data: { optional: true },
    };
}

// Alternative: Using function syntax for complex validation
MyComponent.props = {
    recordId: Number,
    mode: {
        type: String,
        optional: true,
        validate: (m) => ['view', 'edit', 'create'].includes(m),
    }
};
```

### Using Props

```javascript
class MyComponent extends Component {
    setup() {
        // Access props via this.props
        const { recordId, mode = 'view' } = this.props;

        this.state = useState({
            currentMode: mode,
            record: null,
        });
    }
}
```

### Prop Validation

```javascript
class MyComponent extends Component {
    setup() {
        // Props validation happens automatically
        // You can also manually validate
        if (this.props.recordId <= 0) {
            throw new Error('recordId must be positive');
        }
    }
}
```

## Templates and Directives

### Basic Template

```xml
<templates xml:space="preserve">
    <t t-name="my_module.MyComponent" owl="1">
        <div class="my-component">
            <h1 t-esc="props.title"/>
            <p t-if="state.loading">Loading...</p>
            <div t-else="">
                <p>Count: <t t-esc="state.count"/></p>
            </div>
        </div>
    </t>
</templates>
```

### QWeb Directives in OWL

```xml
<t t-name="my_component" owl="1">
    <!-- t-esc: Escape and display value -->
    <p t-esc="state.value"/>

    <!-- t-att: Dynamic attributes -->
    <div t-att-class="{'active': state.isActive, 'disabled': state.isDisabled}"/>
    <a t-att-href="state.url">Link</a>

    <!-- t-if/t-elif/t-else: Conditional rendering -->
    <div t-if="state.count === 0">No items</div>
    <div t-elif="state.count === 1">One item</div>
    <div t-else="">Multiple items</div>

    <!-- t-foreach/t-as: Loops -->
    <div t-foreach="state.records" t-as="record">
        <span t-esc="record.name"/>
        <span>Index: <t t-esc="record_index"/></span>
        <span>First: <t t-esc="record_first"/></span>
        <span>Last: <t t-esc="record_last"/></span>
    </div>

    <!-- t-set: Variable assignment -->
    <t t-set="className" t-value="'my-class'"/>
    <div t-att-class="className"/>

    <!-- t-call: Include another template -->
    <t t-call="my_module.SubTemplate"/>

    <!-- t-on: Event handlers -->
    <button t-on-click="increment">Increment</button>
    <input t-on-input="onInputChange"/>
    <form t-on-submit="onSubmit">
        <!-- Form content -->
    </form>

    <!-- t-model: Two-way binding (custom hook needed) -->
    <input t-model="state.name"/>
</t>
```

### t-on Event Modifiers

```xml
<!-- Basic event -->
<button t-on-click="handleClick">Click</button>

<!-- Prevent default behavior -->
<form t-on-submit.prevent="handleSubmit">Form</form>

<!-- Stop propagation -->
<button t-on-click.stop="handleClick">Click</button>

<!-- Multiple modifiers -->
<button t-on-click.prevent.stop="handleClick">Click</button>

<!-- Keyboard events -->
<input t-on-keyup="onKeyUp"/>
<input t-on-keyup.enter="onEnter"/>
<input t-on-keyup.esc="onEscape"/>

<!-- Capture phase -->
<div t-on-click.capture="handleCapture">
    <button t-on-click="handleClick">Inner</button>
</div>

<!-- Once -->
<button t-on-click.once="handleOnce">Click Once</button>
```

## Event Handling

### Event Handlers

```javascript
class MyComponent extends Component {
    setup() {
        this.state = useState({
            value: '',
        });
    }

    // Simple event handler
    handleClick(ev) {
        console.log('Clicked', ev);
        this.state.value = 'clicked';
    }

    // Form submission
    onSubmit(ev) {
        ev.preventDefault();
        const formData = new FormData(ev.target);
        // Process form data
    }

    // Input change
    onInputChange(ev) {
        this.state.value = ev.target.value;
    }

    // Keyboard events
    onKeyUp(ev) {
        if (ev.key === 'Enter') {
            this.handleEnter();
        } else if (ev.key === 'Escape') {
            this.handleEscape();
        }
    }

    handleEnter() {
        // Enter key handling
    }

    handleEscape() {
        // Escape key handling
    }
}
```

### Event Bubbling and Capture

```javascript
class MyComponent extends Component {
    setup() {
        this.state = useState({ count: 0 });
    }

    handleParentClick() {
        console.log('Parent clicked');
    }

    handleChildClick(ev) {
        ev.stopPropagation(); // Stop bubbling
        console.log('Child clicked');
    }

    handleCapture(ev) {
        console.log('Capture phase', ev);
    }
}
```

```xml
<t t-name="my_component" owl="1">
    <div t-on-click.capture="handleCapture" class="outer">
        <div t-on-click="handleParentClick" class="middle">
            <button t-on-click.stop="handleChildClick">Child</button>
        </div>
    </div>
</t>
```

## Service Injection

### Using Odoo Services

```javascript
class MyComponent extends Component {
    setup() {
        // Core services
        this.orm = useService('orm');
        this.rpc = useService('rpc');
        this.dialog = useService('dialog');
        this.notification = useService('notification');
        this.action = useService('action');
        this.router = useService('router');
    }

    async loadData() {
        // Using ORM service
        const records = await this.orm.searchRead(
            'my.model',
            [['active', '=', true]],
            ['name', 'date', 'state']
        );
        this.state.records = records;
    }

    async loadDataRPC() {
        // Using RPC service
        const result = await this.rpc('/my/custom/route', {
            param1: 'value1',
        });
        this.state.data = result;
    }

    showDialog() {
        // Using dialog service
        this.dialog.add(MyDialog, {
            title: 'My Dialog',
            confirm: () => this.onDialogConfirm(),
        });
    }

    showNotification() {
        // Using notification service
        this.notification.add({
            type: 'success',
            message: 'Operation completed successfully',
            sticky: true,
        });
    }

    executeAction() {
        // Using action service
        this.action.doAction({
            type: 'ir.actions.act_window',
            res_model: 'my.model',
            view_mode: 'tree,form',
            domain: [['state', '=', 'draft']],
        });
    }

    navigate() {
        // Using router service
        this.router.navigate({
            path: '/my/page',
            query: { id: this.props.recordId },
        });
    }
}
```

### Custom Services

```javascript
// Define custom service
odoo.define('my_module.myService', function (require) {
    "use strict";

    const { registry } = require('web.core');

    class MyService {
        constructor(env) {
            this.env = env;
            this.data = null;
        }

        async fetch() {
            this.data = await this.env.services.rpc('/my/api/data');
            return this.data;
        }

        get() {
            return this.data;
        }
    }

    registry.category('services').add('myService', MyService);

    return MyService;
});

// Use custom service in component
class MyComponent extends Component {
    setup() {
        this.myService = useService('myService');
    }

    async loadData() {
        await this.myService.fetch();
        this.state.data = this.myService.get();
    }
}
```

## Integration with Odoo Services

### RPC Service

```javascript
class MyComponent extends Component {
    setup() {
        this.rpc = useService('rpc');
    }

    // Call model method
    async callModelMethod() {
        const result = await this.rpc('/web/dataset/call_kw/my.model/method_name', {
            model: 'my.model',
            method: 'method_name',
            args: [this.props.recordId],
            kwargs: {},
        });
        return result;
    }

    // Custom route
    async callCustomRoute() {
        const result = await this.rpc({
            route: '/my/custom/route',
            params: {
                record_id: this.props.recordId,
            },
        });
        return result;
    }
}
```

### ORM Service

```javascript
class MyComponent extends Component {
    setup() {
        this.orm = useService('orm');
    }

    // Search records
    async searchRecords() {
        const ids = await this.orm.search(
            'my.model',
            [['active', '=', true]],
            { limit: 100 }
        );
        return ids;
    }

    // Read records
    async readRecords(ids) {
        const records = await this.orm.read(
            'my.model',
            ids,
            ['name', 'date', 'state']
        );
        return records;
    }

    // Search and read combined
    async searchReadRecords() {
        const records = await this.orm.searchRead(
            'my.model',
            [['state', '=', 'draft']],
            ['name', 'date', 'state'],
            { limit: 100, order: 'date desc' }
        );
        return records;
    }

    // Create record
    async createRecord(values) {
        const id = await this.orm.create('my.model', values);
        return id;
    }

    // Write record
    async updateRecord(id, values) {
        await this.orm.write('my.model', [id], values);
    }

    // Unlink record
    async deleteRecord(id) {
        await this.orm.unlink('my.model', [id]);
    }
}
```

### Dialog Service

```javascript
// Define a dialog component
odoo.define('my_module.MyDialog', function (require) {
    "use strict";

    const { Component, useState } = owl;
    const { _t } = require('web.core');

    class MyDialog extends Component {
        static template = 'my_module.MyDialog';
        static props = {
            title: { type: String, optional: true },
            confirm: { type: Function, optional: true },
            cancel: { type: Function, optional: true },
        };

        setup() {
            this.state = useState({
                value: '',
            });
        }

        onConfirm() {
            if (this.props.confirm) {
                this.props.confirm(this.state.value);
            }
            this.props.close();
        }

        onCancel() {
            if (this.props.cancel) {
                this.props.cancel();
            }
            this.props.close();
        }
    }

    return MyDialog;
});

// Use dialog in component
class MyComponent extends Component {
    setup() {
        this.dialog = useService('dialog');
    }

    showDialog() {
        this.dialog.add('my_module.MyDialog', {
            title: 'My Dialog',
            confirm: (value) => this.handleDialogConfirm(value),
            cancel: () => this.handleDialogCancel(),
        });
    }

    handleDialogConfirm(value) {
        console.log('Confirmed with:', value);
    }

    handleDialogCancel() {
        console.log('Dialog cancelled');
    }
}
```

### Notification Service

```javascript
class MyComponent extends Component {
    setup() {
        this.notification = useService('notification');
    }

    showSuccess() {
        this.notification.add({
            type: 'success',
            message: 'Operation completed successfully',
            sticky: true,
        });
    }

    showError() {
        this.notification.add({
            type: 'danger',
            message: 'An error occurred',
            sticky: true,
        });
    }

    showWarning() {
        this.notification.add({
            type: 'warning',
            message: 'Warning message',
            sticky: false,
        });
    }

    showInfo() {
        this.notification.add({
            type: 'info',
            message: 'Information message',
            buttons: [
                {
                    text: 'View',
                    onClick: () => console.log('View clicked'),
                },
            ],
        });
    }

    closeAll() {
        this.notification.close();
    }
}
```

### Action Service

```javascript
class MyComponent extends Component {
    setup() {
        this.action = useService('action');
    }

    // Open form view
    openFormView(recordId) {
        this.action.doAction({
            type: 'ir.actions.act_window',
            res_model: 'my.model',
            res_id: recordId,
            view_mode: 'form',
            view_type: 'form',
            views: [[false, 'form']],
        });
    }

    // Open tree view
    openTreeView() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            res_model: 'my.model',
            view_mode: 'tree',
            domain: [['state', '=', 'draft']],
            context: { default_active: true },
        });
    }

    // Execute server action
    executeServerAction(actionId) {
        this.action.doAction(actionId);
    }

    // Execute client action
    executeClientAction(tag) {
        this.action.doAction({
            type: 'ir.actions.client',
            tag: tag,
        });
    }

    // Reload current view
    reloadCurrentView() {
        this.action.reload();
    }

    // Close current action
    closeAction() {
        this.action.doAction({ type: 'ir.actions.act_window_close' });
    }
}
```

## Custom Hooks

### useAutoFocus Hook

```javascript
const { onMounted } = owl;

function useAutoFocus(refName) {
    onMounted(() => {
        const element = this[refName];
        if (element) {
            element.focus();
        }
    });
}

class MyComponent extends Component {
    setup() {
        useAutoFocus.call(this, 'inputRef');
        this.inputRef = owl.hooks.useRef('input');
    }
}
```

### useDebounce Hook

```javascript
function useDebounce(func, wait) {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

class MyComponent extends Component {
    setup() {
        this.state = useState({ searchTerm: '' });

        this.debouncedSearch = useDebounce(this.search.bind(this), 300);
    }

    onSearchInput(ev) {
        this.state.searchTerm = ev.target.value;
        this.debouncedSearch(this.state.searchTerm);
    }

    async search(term) {
        if (term.length < 2) return;
        // Perform search
    }
}
```

### useAsync Hook

```javascript
function useAsync(asyncFn) {
    const Component = owl.Component;
    class AsyncComponent extends Component {
        setup() {
            this.state = useState({
                loading: true,
                error: null,
                data: null,
            });

            onWillStart(async () => {
                try {
                    this.state.data = await asyncFn.call(this);
                } catch (error) {
                    this.state.error = error;
                } finally {
                    this.state.loading = false;
                }
            });
        }
    }
    return AsyncComponent;
}

// Usage
class MyComponent extends useAsync(async function () {
    return await this.orm.searchRead('my.model', [], ['name']);
}) {
    // Component logic
}
```

## OWL Patterns

### Container/Presenter Pattern

```javascript
// Container component handles data
class MyContainer extends Component {
    setup() {
        this.orm = useService('orm');
        this.state = useState({ records: [] });
    }

    async loadRecords() {
        this.state.records = await this.orm.searchRead(
            'my.model',
            [],
            ['name', 'date']
        );
    }
}

// Presentational component handles UI
class MyList extends Component {
    static props = {
        records: { type: Array },
        onRecordClick: { type: Function, optional: true },
    };
}
```

### Higher Order Components

```javascript
function withData(WrappedComponent) {
    class DataWrapper extends Component {
        setup() {
            this.orm = useService('orm');
            this.state = useState({ data: null, loading: true });
        }

        async loadData() {
            this.state.data = await this.orm.searchRead(
                this.props.model,
                this.props.domain || [],
                this.props.fields || []
            );
            this.state.loading = false;
        }
    }

    DataWrapper.template = 'my_module.DataWrapper';
    DataWrapper.components = { WrappedComponent };
    return DataWrapper;
}
```

## OWL Testing

### Component Testing

```javascript
// tests/js/components/my_component_tests.js
odoo.define('my_module.MyComponentTests', function (require) {
    "use strict";

    const { Component, xml } = owl;
    const { makeView, setupViewRegistries } = require('web.test_utils');

    const { mount, nextTick } = owl.hooks;
    const MyComponent = require('my_module.MyComponent');

    QUnit.module('MyComponent', {
        beforeEach: function () {
            this.target = document.createElement('div');
            document.body.appendChild(this.target);
        },
        afterEach: function () {
            this.target.remove();
        },
    });

    QUnit.test('component renders correctly', async function (assert) {
        const component = await mount(MyComponent, {
            target: this.target,
            props: { recordId: 1 },
        });

        assert.ok(component);
        assert.strictEqual(component.state.count, 0);

        component.unmount();
    });

    QUnit.test('clicking button increments count', async function (assert) {
        const component = await mount(MyComponent, {
            target: this.target,
            props: { recordId: 1 },
        });

        const button = this.target.querySelector('button');
        await button.click();
        await nextTick();

        assert.strictEqual(component.state.count, 1);

        component.unmount();
    });

    QUnit.test('loads data on mount', async function (assert) {
        const component = await mount(MyComponent, {
            target: this.target,
            props: { recordId: 1 },
        });

        // Wait for async operation
        await nextTick();
        await nextTick();

        assert.ok(component.state.records.length > 0);

        component.unmount();
    });
});
```

### Integration Testing with Views

```javascript
QUnit.module('MyComponent Integration Tests', function (hooks) {
    let serverData;
    let target;

    hooks.beforeEach(async function () {
        target = document.createElement('div');
        document.body.appendChild(target);

        serverData = {
            models: {
                'my.model': {
                    fields: {
                        name: { string: 'Name', type: 'char' },
                        date: { string: 'Date', type: 'date' },
                    },
                    records: [
                        { id: 1, name: 'Record 1', date: '2024-01-01' },
                        { id: 2, name: 'Record 2', date: '2024-01-02' },
                    ],
                },
            },
        };

        setupViewRegistries();
    });

    hooks.afterEach(function () {
        target.remove();
    });

    QUnit.test('component works in list view', async function (assert) {
        assert.expect(1);

        const list = await makeView({
            type: 'list',
            resModel: 'my.model',
            serverData,
            arch: '<list><field name="name"/><field name="date"/></list>',
            viewRegistry: MyComponent,
        });

        assert.containsOnce(list, '.my-component');
    });
});
```

## Best Practices

### Performance

1. **Use computed state sparingly** - Heavy computations should be memoized
2. **Avoid deep nesting** - Keep component structure shallow
3. **Use `t-key` in loops** - Help OWL track elements efficiently
4. **Lazy load services** - Only inject services when needed
5. **Cleanup subscriptions** - Remove event listeners in `onWillUnmount`

### Code Organization

1. **Keep components small** - Single responsibility principle
2. **Separate container and presentational components**
3. **Use hooks for reusable logic**
4. **Type check props for better debugging**
5. **Document component purpose and props**

### Testing

1. **Test component behavior, not implementation**
2. **Test async operations properly**
3. **Test edge cases (empty states, errors)**
4. **Test user interactions**
5. **Mock services appropriately**

## Common OWL Patterns in Odoo

### Record List Component

```javascript
class RecordList extends Component {
    static props = {
        model: { type: String },
        domain: { type: Array, optional: true },
        fields: { type: Array, optional: true },
    };

    setup() {
        this.orm = useService('orm');
        this.state = useState({
            records: [],
            loading: true,
            error: null,
        });

        onWillStart(this.loadRecords.bind(this));
    }

    async loadRecords() {
        try {
            this.state.records = await this.orm.searchRead(
                this.props.model,
                this.props.domain || [],
                this.props.fields || ['name']
            );
        } catch (error) {
            this.state.error = error;
        } finally {
            this.state.loading = false;
        }
    }

    onRecordClick(record) {
        this.trigger('record-clicked', { record });
    }
}
```

### Form Field Component

```javascript
class FormField extends Component {
    static props = {
        value: { optional: true },
        readonly: { type: Boolean, optional: true },
        required: { type: Boolean, optional: true },
        onChange: { type: Function, optional: true },
    };

    setup() {
        this.state = useState({
            value: this.props.value,
        });
    }

    onChange(ev) {
        this.state.value = ev.target.value;
        if (this.props.onChange) {
            this.props.onChange(this.state.value);
        }
    }
}
```

## OWL in Odoo 19

### New Features in Odoo 19

1. **Enhanced reactivity** - Faster state updates
2. **Improved error handling** - Better error boundaries
3. **TypeScript support** - Better IDE integration
4. **Built-in components** - More reusable OWL components
5. **Performance optimizations** - Smaller bundle sizes

### Migration from OWL 1 to OWL 2

- `t-set` now uses `t-value` for expressions
- Component API changes in hooks
- Template syntax improvements
- Service API changes

Remember: OWL is the primary frontend framework for Odoo 19. Mastering OWL is essential for creating modern, interactive Odoo modules.
