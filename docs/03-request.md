# Request Handling

> **Keywords:** query params, cookies, request headers, client IP, browser user agent, geolocation, json body, rendering html, partial block swap, redirects, csrf input, internationalization, exception handling, abort 404, global request proxy, current_request, query arguments, client info, redirect back, referer, flash messages, cookies dict

Every `render()` function receives a `Request` object. It handles input, output, auth, and more.

## Reading input

```python
def render(request: Request):
    # URL example: /search?q=hello
    request.args['q']              # "hello"
    or request.args.get('q')
    # POST form data
    request.form['email']          # "user@example.com"

    # JSON body (POST with Content-Type: application/json)
    request.json_body              # {"key": "value"}

    # Route params (/user/[id])
    request.params['id']           # "42"

    # HTTP method
    request.method                 # "GET" or "POST"

    # Current path
    request.path                   # "/contact"
```

## Metadata

Access information about the client and the connection.

```python
def render(request: Request):
    # Client IP address (handles X-Forwarded-For if behind a proxy)
    request.ip                     # "192.168.1.1"

    # Raw User-Agent string
    request.user_agent             # "Mozilla/5.0..."

    # Parsed browser info
    request.browser.name           # "Chrome", "Firefox", "Safari", etc.
    request.browser.os             # "macOS", "Windows", "Linux", "iOS", "Android"
    request.browser.is_mobile      # True or False

    # Geolocation & Geographic metadata
    request.geo['city']            # "Paris"
    request.geo['country']         # "FR"
    request.geo['name']            # "France" (Full country name)
    request.geo['flag']            # "🇫🇷" (Emoji flag)
    request.geo['currency']        # "EUR"
    request.geo['timezone']        # "Europe/Paris"
    request.geo['dial_code']       # "+33"
    request.geo['lat']             # 48.8566
    request.geo['lon']             # 2.3522
    
    # Note: request.location is a legacy alias for request.geo; prefer request.geo in new code
```

## Rendering responses

### HTML template

```python
def render(request: Request):
    return request.html('page.html', name='World', items=[1, 2, 3])
```

The template receives all kwargs as variables.

### JSON response

```python
def render(request: Request):
    return request.json({'status': 'ok', 'count': 42})
```

### Block (partial rendering)

`request.block(filepath, block_name, **context)` renders only a specific `{% block %}` from a template. The `block_name` argument is **required**.

```python
def render(request: Request):
    return request.block('page.html', 'main', form=form)
    #                     ^^^^^^^^     ^^^^
    #                     template     block name (required)
```

This returns only the content inside `{% block main %}...{% endblock %}`, without the surrounding layout (`<html>`, `<head>`, `<nav>`, etc.).

You may also see this described as a block swap or partial swap elsewhere in the docs.

#### Native block swap (no HTMX needed)

Add `data-block` on a `<form>` to enable automatic partial updates. The form will submit via `fetch` and swap only the target block in the DOM — no full page reload.

```html
<!-- The framework finds the target by matching [data-block="main"] or id="main" -->
<form method="POST" data-block="main">
    {{ request.csrf_input() }}
    {{ form.name }}
    <button type="submit">Send</button>
</form>
```

When `data-block="main"` is present:
1. **Client**: JS intercepts the submit, sends via `fetch` with a `X-Block: main` header
2. **Server**: `request.html()` detects the header and calls `request.block()` automatically
3. **Client**: the response replaces the `innerHTML` of `<main>`

This means **the Python code is the same** for both full-page GET and partial POST:

```python
def render(request: Request):
    form = Form({ ... }, request)

    if form.validate():
        request.flash('success', 'Sent!')
        form.reset()

    return request.html('page.html', form=form)
```

For a custom target selector, add `data-target`:

```html
<form method="POST" data-block="main" data-target="#my-container">
```

### Response status code

```python
# Set the status code (method chaining)
request.status_code(201)
return request.json({'created': True})

# Get the current status code as an integer
if request.status_code == 404:
    print("Not found!")
```

### File download

```python
def render(request: Request):
    return request.send_file('/path/to/report.pdf')

    # Or inline (display in browser)
    return request.send_file('/path/to/image.png', as_attachment=False)

    # Custom filename
    return request.send_file('/path/to/file.csv', filename='export.csv')
```

> **Automatic Streaming**: Asok v0.1.4 automatically uses chunked streaming for files larger than **5 MB**. This ensures that large downloads (videos, archives, large reports) don't consume server RAM, as the file is read and sent in small chunks (64 KB) instead of being loaded entirely in memory.

## Redirect

```python
def render(request: Request):
    request.redirect('/dashboard')
    # Raises RedirectException — stops execution, sends 302
```

### Redirect back

Useful for shared forms (newsletter, search) that can be submitted from any page.

```python
def post(request: Request):
    # Process something...
    request.back()  # Redirects to Referer or '/'
    
    # Custom default fallback if Referer is missing
    request.back(default='/home')
```

## Flash messages

```python
# Set a flash message
request.flash('success', 'Your message has been sent!')
request.redirect('/contact')
```

```html
<!-- Display flash messages in template -->
{% for msg in get_flashed_messages() %}
    <div class="flash {{ msg.category }}">{{ msg.message }}</div>
{% endfor %}
```

Categories are free-form strings: `success`, `error`, `info`, `warning`, etc.

## CSRF protection

CSRF is enabled by default on POST, PUT, DELETE requests. Add the hidden input in your forms:

```html
<form method="POST">
    {{ request.csrf_input() }}
    <!-- your fields -->
</form>
```

For AJAX requests, send the token as a header:

```javascript
fetch('/api/data', {
    method: 'POST',
    headers: { 'X-CSRF-Token': '{{ request.csrf_token_value }}' }
})
```

## Cookies

```python
request.cookies_dict              # All cookies as dict
request.cookies_dict.get('key')   # Read a cookie
```

## Environment variables

```python
request.env('SECRET_KEY')         # Read from os.environ
request.env('MISSING', 'default') # With default value
request.env('DEBUG')              # Auto-cast: "true" → True
```

## Internationalization

```python
# In Python
request.lang                      # Current language ("en", "fr", ...)
request.__('welcome')             # Translated string

# In templates
{{ __('welcome') }}
{{ request.lang }}
```

The language is detected from: query param `?lang=fr` > cookie > Accept-Language header > config default.

## Variable Sharing

Inject global variables that are available in every template without passing them manually to `request.html()`.

### Global values

```python
# wsgi.py
app.share(site_name="My Blog", version="1.0")

# In any template
<h1>{{ site_name }}</h1>
```

### Dynamic values

If you provide a callable, it is executed per request with the `request` object as its only argument.

```python
# wsgi.py
app.share(user=lambda r: r.user)

# In any template
{% if user %}
  Hello, {{ user.name }}
{% endif %}
```

### Accessing shared variables in Python

Use `request.shared(name)` to retrieve a shared variable's value for the current request context.

```python
def render(request):
    user = request.shared('user')  # Result of the lambda(request)

## Error Handling & Exceptions

Asok provides a structured exception hierarchy for handling errors and controlling the request flow. All framework exceptions inherit from `AsokException`.

### 1. Flow Control

These exceptions are caught by the framework to send a specific HTTP response.

- `request.redirect(url)` raises `RedirectException`.
- `request.abort(code)` raises `AbortException`.

### 2. Semantic HTTP Shortcuts

Instead of using raw status codes, you can raise semantic exceptions:

```python
from asok import NotFoundError, ForbiddenError, UnauthorizedError

def render(request):
    item = Item.find(request.params['id'])
    if not item:
        request.abort_404("Item not found") # Shortcut for raise NotFoundError
    
    if not request.user:
        request.abort_401() # Shortcut for raise UnauthorizedError
    
    if item.user_id != request.user.id:
        request.abort_403() # Shortcut for raise ForbiddenError
```

#### Shortcut Helpers

The `Request` object provides methods that automatically raise the appropriate exception:

- `request.abort(code, message)` -> `AbortException`
- `request.abort_404(message)` -> `NotFoundError`
- `request.abort_403(message)` -> `ForbiddenError`
- `request.abort_401(message)` -> `UnauthorizedError`

### 3. Logical Errors

- **`SecurityError`**: Raised for CSRF violations, tampered sessions, or unauthorized attribute access in templates.
- **`ValidationError`**: Raised when form or data validation fails. It can hold a dictionary of specific field errors.
- **`TemplateError`**: Raised when a template fails to compile or render.

```python
from asok import ValidationError

raise ValidationError("Invalid input", errors={"email": "Invalid format"})
```

## Global Request Proxy: `current_request`

In a view function, you always have the `request` parameter at hand. But when you call helpers, services, or utility functions from within a request, you would normally have to pass `request` as a parameter through every level of the call stack.

`current_request` is a **thread-safe, context-local proxy** that always points to the active `Request` for the current HTTP or WebSocket context — without requiring you to pass anything manually.

```python
from asok import current_request

# --- A service, completely decoupled from your views ---
def get_personalized_greeting():
    user = current_request.user
    lang = current_request.lang
    if user:
        return f"Hello, {user.name}!" if lang == "en" else f"Bonjour, {user.name} !"
    return "Hello, guest!"

# --- Your view stays clean ---
def render(request: Request):
    greeting = get_personalized_greeting()   # no request parameter needed
    return request.html("page.html", greeting=greeting)
```

### When to use `current_request` vs `request`

| Use case | Recommended approach |
|---|---|
| Inside a `render()` / `post()` view | Use the `request` parameter directly |
| In a helper, service, or utility function | Use `current_request` |
| In a `Component.render()` method | Use `current_request` |
| In a background task launched from a view | Use `current_request` (context is propagated automatically) |

### Safety: outside a request context

Accessing `current_request` outside of an active HTTP or WebSocket context raises a clear `RuntimeError`:

```python
from asok import current_request

# At module level, during startup, or in an unmanaged thread:
print(current_request.user)  # RuntimeError: Working outside of request context
```

This prevents silent failures — you always know immediately if you access the proxy at the wrong moment.

> **Note**: `current_request` is the **only** global request proxy in Asok. There is no `request` alias.

---
[← Previous: Routing](02-routing.md) | [Documentation](README.md) | [Next: Templates →](04-templates.md)
