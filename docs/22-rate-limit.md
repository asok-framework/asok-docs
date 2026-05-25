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

By default, the rate limiter works in-memory (per Gunicorn worker). For production systems with multiple workers, use the **`file` storage** to share the limit across processes:

```python
from asok import Asok, RateLimit, Cache

app = Asok()
# Link the rate limiter to the app's cache storage
limiter = RateLimit("60/m", storage=app._cache)
```

## 5. Options

| Option | Type | Description |
|---|---|---|
| `limit` | `str/int` | Maximum requests (e.g., `"60/m"` or `60`). |
| `window` | `int` | Window duration in seconds (if `limit` is an `int`). |
| `key_func`| `func` | Custom function to identify clients (default: IP address). |
| `storage` | `Cache` | Optional `Cache` instance for cross-process persistence. |

---
[← Previous: CORS & Gzip](21-cors-gzip.md) | [Documentation](README.md) | [Next: Security Audit →](23-security-audit.md)
