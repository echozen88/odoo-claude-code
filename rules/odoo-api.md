# Odoo 19 API Development Rules

## Controller Setup

### Basic Controller Structure

```python
from odoo import http
from odoo.http import request

class MyController(http.Controller):

    @http.route('/my/endpoint', type='http', auth='user')
    def my_endpoint(self, **kwargs):
        return "Response content"
```

## Route Configuration

### Authentication Levels

```python
# Public - No authentication required
@http.route('/my/public', type='http', auth='public')
def public_endpoint(self):
    return "Public content"

# User - Requires logged-in user
@http.route('/my/user', type='http', auth='user')
def user_endpoint(self):
    return "User content"

# User API Key - For external API access
@http.route('/my/api', type='json', auth='user_api_key')
def api_endpoint(self, **kwargs):
    return {'result': 'success'}

# None - No user context (for internal use)
@http.route('/my/internal', type='http', auth='none')
def internal_endpoint(self):
    return request.render('my_module.template', {})
```

### Route Types

```python
# HTTP - Return HTML/Text
@http.route('/my/page', type='http')
def page(self):
    return request.render('my_module.template', {})

# JSON - Return JSON object
@http.route('/my/api', type='json')
def api(self):
    return {'success': True, 'data': 'value'}

# HTTP with JSON - Return JSON response
@http.route('/my/json', type='http', auth='user')
def json_response(self):
    return request.make_json_response({'result': 'success'})
```

### HTTP Methods

```python
# GET (default)
@http.route('/my/data', type='http', methods=['GET'])
def get_data(self):
    return "Data"

# POST
@http.route('/my/submit', type='http', methods=['POST'],
            auth='user', csrf=True)
def submit_data(self, **kwargs):
    return "Submitted"

# Multiple methods
@http.route('/my/resource', type='http',
            methods=['GET', 'POST', 'PUT', 'DELETE'])
def resource(self, **kwargs):
    method = request.httprequest.method
    if method == 'GET':
        return "Get"
    elif method == 'POST':
        return "Post"
    elif method == 'PUT':
        return "Put"
    elif method == 'DELETE':
        return "Delete"
```

## Input Handling

### GET Parameters

```python
@http.route('/my/search', type='http', auth='user')
def search(self, **kwargs):
    query = kwargs.get('query', '')
    limit = int(kwargs.get('limit', 20))
    offset = int(kwargs.get('offset', 0))

    records = request.env['my.model'].search([
        ('name', 'ilike', f'%{query}%')
    ], limit=limit, offset=offset)

    return request.render('my_module.search', {
        'records': records,
        'query': query,
    })
```

### POST JSON Data

```python
@http.route('/my/api/data', type='json', auth='user')
def api_data(self, **kwargs):
    data = kwargs.get('data', {})
    name = data.get('name')
    value = data.get('value')

    if not name:
        return {'error': 'Name is required'}

    record = request.env['my.model'].create({
        'name': name,
        'value': value,
    })

    return {'success': True, 'id': record.id}
```

### POST Form Data

```python
@http.route('/my/form', type='http', methods=['POST'],
            auth='user', csrf=True)
def form_submit(self, **kwargs):
    name = kwargs.get('name')
    email = kwargs.get('email')

    if not name or not email:
        return request.redirect('/my/form?error=required')

    record = request.env['my.model'].create({
        'name': name,
        'email': email,
    })

    return request.redirect('/my/form?success=true')
```

## Input Validation

### Required Fields

```python
@http.route('/my/api/create', type='json', auth='user')
def api_create(self, **kwargs):
    data = kwargs.get('data', {})

    required_fields = ['name', 'value']
    for field in required_fields:
        if field not in data:
            return {
                'error': f'Missing required field: {field}',
                'field': field,
            }
```

### Type Validation

```python
@http.route('/my/api/submit', type='json', auth='user')
def api_submit(self, **kwargs):
    data = kwargs.get('data', {})
    value = data.get('value')

    # Validate numeric type
    try:
        value = float(value)
    except (ValueError, TypeError):
        return {
            'error': 'Value must be a number',
            'field': 'value',
        }
```

### Range Validation

```python
@http.route('/my/api/submit', type='json', auth='user')
def api_submit(self, **kwargs):
    data = kwargs.get('data', {})
    value = data.get('value')

    # Validate range
    if value < 0 or value > 100:
        return {
            'error': 'Value must be between 0 and 100',
            'field': 'value',
        }
```

### String Validation

```python
@http.route('/my/api/submit', type='json', auth='user')
def api_submit(self, **kwargs):
    data = kwargs.get('data', {})
    name = data.get('name')

    # Validate length
    if not name or len(name) < 3 or len(name) > 100:
        return {
            'error': 'Name must be between 3 and 100 characters',
            'field': 'name',
        }

    # Validate characters (optional)
    if not name.replace(' ', '').isalnum():
        return {
            'error': 'Name contains invalid characters',
            'field': 'name',
        }
```

### Sanitization

```python
import bleach

@http.route('/my/api/submit', type='json', auth='user')
def api_submit(self, **kwargs):
    data = kwargs.get('data', {})
    name = data.get('name', '')

    # Strip whitespace
    name = name.strip()

    # Remove HTML tags
    name = bleach.clean(name, tags=[], strip=True)

    # Continue with sanitized input
    # ...
```

## Output Formatting

### JSON Response Structure

```python
@http.route('/my/api/data', type='json', auth='user')
def api_data(self):
    # Success response
    return {
        'success': True,
        'data': {
            'id': 123,
            'name': 'Test',
        },
        'message': 'Operation successful',
    }

# Error response
def api_data(self):
    return {
        'success': False,
        'error': {
            'code': 'VALIDATION_ERROR',
            'message': 'Invalid input data',
            'field': 'email',
        },
    }
```

### Pagination Response

```python
@http.route('/my/api/list', type='json', auth='user')
def api_list(self, **kwargs):
    page = int(kwargs.get('page', 1))
    limit = int(kwargs.get('limit', 20))

    offset = (page - 1) * limit
    records = request.env['my.model'].search(
        [('active', '=', True)],
        limit=limit,
        offset=offset,
    )

    total = request.env['my.model'].search_count([('active', '=', True)])

    return {
        'success': True,
        'data': records.read(['name', 'value']),
        'pagination': {
            'page': page,
            'limit': limit,
            'total': total,
            'pages': (total + limit - 1) // limit,
        },
    }
```

## Error Handling

### Standardized Error Responses

```python
@http.route('/my/api/action', type='json', auth='user')
def api_action(self, **kwargs):
    try:
        # Process request
        result = self._process_data(kwargs)
        return {
            'success': True,
            'data': result,
        }

    except ValidationError as e:
        return {
            'success': False,
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': str(e),
            },
        }

    except AccessError as e:
        return {
            'success': False,
            'error': {
                'code': 'ACCESS_DENIED',
                'message': str(e),
            },
        }

    except Exception as e:
        _logger.exception('API error: %s', e)
        return {
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred',
            },
        }
```

### User Error Messages

```python
# Always translatable
from odoo import _

return {
    'success': False,
    'error': {
        'message': _('Invalid input data'),
    },
}
```

## Security

### CSRF Protection

```python
# HTTP POST routes must have CSRF protection
@http.route('/my/form/submit', type='http', methods=['POST'],
            auth='user', csrf=True)
def form_submit(self, **kwargs):
    # CSRF token validated automatically
    data = kwargs.get('data')
    # Process data
    return "Submitted"

# CSRF token for public forms
@http.route('/my/public/form', type='http', auth='public', website=True)
def public_form(self):
    # CSRF token automatically included in template
    return request.render('my_module.public_form', {})
```

### Authentication Check

```python
@http.route('/my/user/endpoint', type='json', auth='user')
def user_endpoint(self):
    # auth='user' ensures user is logged in
    # User is available in request.env.user
    user = request.env.user

    # Check for specific user
    if user == request.env.ref('base.public_user'):
        return {
            'success': False,
            'error': 'Not authenticated',
        }

    return {'success': True, 'user': user.name}
```

### Authorization Check

```python
@http.route('/my/admin/endpoint', type='json', auth='user')
def admin_endpoint(self):
    user = request.env.user

    # Check user has required group
    if not user.has_group('my_module.group_admin'):
        return {
            'success': False,
            'error': 'Insufficient permissions',
        }

    # Process request
    return {'success': True}
```

### Rate Limiting

```python
from collections import defaultdict
import time

_rate_limit_store = defaultdict(list)

@http.route('/my/api/endpoint', type='json', auth='user')
def rate_limited_endpoint(self):
    user_id = request.env.user.id
    key = f"{user_id}:{request.httprequest.remote_addr}"
    now = time.time()

    # Get recent requests
    requests = _rate_limit_store[key]
    requests = [r for r in requests if now - r < 60]  # Last 60 seconds

    # Check limit (10 requests per minute)
    if len(requests) >= 10:
        return {
            'success': False,
            'error': 'Rate limit exceeded',
        }

    # Record this request
    requests.append(now)
    _rate_limit_store[key] = requests

    # Process request
    return {'success': True}
```

## ORM Usage in Controllers

### Reading Data

```python
@http.route('/my/api/data', type='json', auth='user')
def get_data(self):
    # Read with domain
    records = request.env['my.model'].search([
        ('user_id', '=', request.env.user.id),
    ])

    # Read specific fields (don't expose sensitive data)
    data = records.read(['name', 'value', 'date'])

    return {
        'success': True,
        'data': data,
    }
```

### Creating Data

```python
@http.route('/my/api/create', type='json', auth='user')
def create_data(self, **kwargs):
    data = kwargs.get('data', {})

    record = request.env['my.model'].create({
        'name': data.get('name'),
        'value': data.get('value'),
        'user_id': request.env.user.id,  # Set user automatically
    })

    return {
        'success': True,
        'id': record.id,
    }
```

### Updating Data

```python
@http.route('/my/api/update', type='json', auth='user')
def update_data(self, **kwargs):
    data = kwargs.get('data', {})
    record_id = data.get('id')

    # Verify user can modify
    record = request.env['my.model'].search([
        ('id', '=', record_id),
        ('user_id', '=', request.env.user.id),
    ], limit=1)

    if not record:
        return {
            'success': False,
            'error': 'Record not found or access denied',
        }

    record.write({
        'value': data.get('value'),
    })

    return {'success': True}
```

### Deleting Data

```python
@http.route('/my/api/delete', type='json', auth='user')
def delete_data(self, **kwargs):
    data = kwargs.get('data', {})
    record_id = data.get('id')

    # Verify user can delete
    record = request.env['my.model'].search([
        ('id', '=', record_id),
        ('user_id', '=', request.env.user.id),
    ], limit=1)

    if not record:
        return {
            'success': False,
            'error': 'Record not found or access denied',
        }

    record.unlink()

    return {'success': True}
```

## File Uploads

### Basic File Upload

```python
@http.route('/my/api/upload', type='http', methods=['POST'],
            auth='user', csrf=True)
def upload_file(self, **kwargs):
    file = kwargs.get('file')

    if not file:
        return request.redirect('/my/upload?error=no_file')

    # Validate file type
    allowed_types = ['image/jpeg', 'image/png', 'application/pdf']
    if file.content_type not in allowed_types:
        return request.redirect('/my/upload?error=invalid_type')

    # Validate file size (10MB max)
    max_size = 10 * 1024 * 1024
    if file.content_length > max_size:
        return request.redirect('/my/upload?error=file_too_large')

    # Save attachment
    attachment = request.env['ir.attachment'].create({
        'name': file.filename,
        'datas': base64.b64encode(file.read()),
        'res_model': 'my.model',
        'res_id': kwargs.get('record_id'),
    })

    return request.redirect('/my/upload?success=true')
```

## Response Helpers

### JSON Response

```python
def make_json_response(self, success=True, data=None, error=None):
    """Standardized JSON response"""
    response = {'success': success}
    if data is not None:
        response['data'] = data
    if error is not None:
        response['error'] = error
    return request.make_json_response(response)
```

### Error Response

```python
def make_error_response(self, code, message):
    """Standardized error response"""
    return request.make_json_response({
        'success': False,
        'error': {
            'code': code,
            'message': message,
        },
    }, status=400)
```

## API Documentation

### Route Documentation in Docstring

```python
@http.route('/my/api/records', type='json', auth='user')
def get_records(self, **kwargs):
    """Get list of records.

    Query Parameters:
        page: int (default: 1) - Page number
        limit: int (default: 20) - Records per page
        search: str (optional) - Search query

    Returns:
        JSON response with:
            - success: bool
            - data: array of records
            - pagination: object with page/limit/total/pages
    """
    page = int(kwargs.get('page', 1))
    limit = int(kwargs.get('limit', 20))
    search = kwargs.get('search', '')

    # ... implementation
```

## API Best Practices

1. **Always validate input** - Check presence, type, range, format
2. **Use proper auth** - user, public, user_api_key
3. **CSRF protection** - Required for POST routes
4. **Standardize responses** - Consistent JSON structure
5. **Don't expose internal IDs** - Use display names where appropriate
6. **Rate limit public APIs** - Prevent abuse
7. **Log errors** - Not for users, but for debugging
8. **Use descriptive error codes** - Help clients handle errors
9. **Pagination** - Support large result sets
10. **Version your APIs** - Use /v1/, /v2/ prefixes

## API Testing

### Test Controller

```python
from odoo.tests import HttpCase, tagged

@tagged('post_install', '-at_install')
class TestMyController(HttpCase):
    """Test MyController HTTP endpoints"""

    def test_index_page_loads(self):
        """Test main index page loads"""
        response = self.url_open('/my/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('My Module', response.text)

    def test_json_endpoint(self):
        """Test JSON API endpoint"""
        self.authenticate('admin', 'admin')
        response = self.url_open(
            '/my/api/data',
            data=json.dumps({'param': 'value'}),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('result', data)

    def test_authenticated_endpoint(self):
        """Test endpoint requires authentication"""
        response = self.url_open('/my/protected')
        self.assertEqual(response.status_code, 401)
```
