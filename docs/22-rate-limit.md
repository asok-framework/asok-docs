# Rate Limit

Protect your application from brute-force attacks and abuse with Asok's built-in rate limiter.

## Quick Start (Decorator)

The easiest way to protect a specific page is using the `@rate_limit` decorator in your `page.py`:

```python
# src/pages/protected/page.py
from asok import rate_limit

@rate_limit("5/m")  # Limit to 5 requests per minute
def render(request):
    return "This page is protected!"
```

## Limit Syntax

Asok supports human-readable strings for defining limits:

- `"10/s"`: 10 requests per second
- `"60/m"`: 60 requests per minute
- `"1000/h"`: 1000 requests per hour
- `"5000/d"`: 5000 requests per day

## Global Middleware

To apply a global rate limit, create `src/middlewares/ratelimit.py`:

```python
from asok import RateLimit

# Use a string limit for simplicity
limiter = RateLimit("100/m")

def handle(request, next):
    return limiter(request, next)
```

## 4. Production Storage (Shared Limit)

By default, the rate limiter works in-memory (per Gunicorn worker) for maximum performance and security against memory leaks when using the default memory cache. 

For production systems with multiple workers or multi-node servers, Asok **automatically scales** the rate limiter when a distributed cache backend is configured:

* If `ASOK_CACHE_BACKEND` is set to `redis` or `file`, the rate limiter automatically resolves and uses the global distributed cache (`default_cache`).
* To prevent collisions between different routes sharing the same cache backend, the `@rate_limit` decorator **automatically prefixes** keys using the module and function name of the decorated view (e.g. `rl:src.pages.home.render:<ip>`).

### Manual Storage & Prefixes

You can also explicitly pass a custom cache instance or prefix:

```python
from asok import RateLimit, Cache

# Explicitly use a custom cache instance and custom prefix prefix
custom_cache = Cache(backend="redis")
limiter = RateLimit("60/m", storage=custom_cache, prefix="my_custom_limit")
```

Or using the decorator:

```python
@rate_limit("10/m", prefix="sensitive_api")
def render(request):
    return "Custom Prefix applied"
```

## Programmatic Rate Limiting (Custom Responses)

If you want to perform custom actions (like flashing an error message) instead of rendering the default 429 page when a limit is exceeded, you can check the rate limit programmatically inside your view function.

To do this, call `request.rate_limit()` inside a `try/except` block and catch `RateLimitExceeded`:

```python
from asok import Request, RateLimitExceeded
from asok.forms import Form
from my_app.models import Contact

def post(request: Request):
    form = Form.from_model(Contact, request)
    try:
        # Check limit programmatically
        request.rate_limit("3/day")
        
        if form.validate():
            Contact.create(**form.data)
            return request.block("page.html", "main", form=form.reset())
    except RateLimitExceeded:
        # Catch and handle it, e.g. using a flash message
        request.flash("error", "You have exceeded the rate limit. Please try again later.")
        
    return request.html('page.html', form=form)
```

> [!NOTE]
> * When using `request.rate_limit()` without a `prefix`, Asok automatically generates a unique prefix based on the calling module and function name (e.g. `rl:src.pages.contact.post`).
> * If `RateLimitExceeded` is raised but not caught inside the view, it bubbles up and automatically triggers the framework's default 429 error page rendering.

## 5. Options

| Option | Type | Description |
|---|---|---|
| `limit` | `str/int` | Maximum requests (e.g., `"60/m"` or `60`). |
| `window` | `int` | Window duration in seconds (if `limit` is an `int`). |
| `key_func`| `func` | Custom function to identify clients (default: IP address). |
| `storage` | `Cache` | Optional `Cache` instance for cross-process persistence (defaults to global cache if `redis` or `file` is active). |
| `prefix` | `str` | Optional custom prefix for the rate-limit cache keys (defaults to `"rl"` for middleware, or automatically generated based on route function for the `@rate_limit` decorator). |

---
[← Previous: CORS & Gzip](21-cors-gzip.md) | [Documentation](README.md) | [Next: Security Audit →](23-security-audit.md)
