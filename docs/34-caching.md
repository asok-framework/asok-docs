# Caching

Asok comes with a lightning-fast, zero-dependency caching system built natively into the framework. It can drastically speed up your application by caching HTTP responses, database queries, and even template fragments.

## 1. Template Fragment Caching

The template engine supports the `{% cache "key" ttl %}` tag to cache computationally expensive blocks of HTML. This is especially useful for rendering complex loops or menus.

```html
{% cache "sidebar_categories" 3600 %}
    <!-- This loop and any queries inside it are only executed once per hour! -->
    <ul>
    {% for cat in get_categories() %}
        <li>{{ cat.name }}</li>
    {% endfor %}
    </ul>
{% endcache %}
```

## 2. Caching HTTP Pages

The easiest way to cache a full page is to use the `@cache_page` decorator. It will automatically intercept `GET` requests and serve the cached response without executing your view logic.

```python
from asok.cache import cache_page
import time

@cache_page(ttl=60) # Caches the response for 60 seconds
def render(request):
    time.sleep(2) # Simulating heavy computation
    return request.html("dashboard.asok")
```

## 2. Caching Database Queries

You can chain the `.cache(ttl)` method directly onto any ORM query builder. Asok will compute a unique hash based on the exact SQL statement and parameters, completely bypassing the database if the result is already in memory.

```python
from models.post import Post

def get_popular_posts():
    # Only hits the SQLite database once every 5 minutes
    posts = Post.query().order_by('-views').limit(10).cache(ttl=300).get()
    
    return [p.to_dict() for p in posts]
```

> **Note**: `.cache()` is part of the Query Builder. You must call it *before* execution methods like `.get()` or `.first()`. You cannot chain it after `.all()` since `.all()` returns a list immediately.

## 3. Global Configuration

By default, Asok uses a blazing fast **in-memory** cache (`backend="memory"`).

### Production Recommendations

In a production environment (especially when using **Gunicorn** with multiple workers), the `memory` backend is isolated to each process. This means a cache set by Worker A will not be visible to Worker B.

To ensure cache consistency across all worker processes, you **should** use the file-based backend:

```env
# .env
ASOK_CACHE_BACKEND=file
ASOK_CACHE_PATH=.asok/cache
```

### Backend Comparison

| Backend | Speed | Persistence | Multi-process Safe |
|---|---|---|---|
| `memory` | ⚡ Instant | No (Lost on restart) | No |
| `file` | 🚀 Fast | Yes | **Yes** |

---

## Advanced Usage (Manual Caching)

If you need fine-grained control over caching specific variables or logic, you can use the underlying `Cache` class directly.

```python
from asok.cache import Cache

# You can instantiate your own custom cache instance
cache = Cache(backend='file', path='.my_custom_cache')

cache.set('key', 'value', ttl=300)
cache.get('key', default='missing')
cache.has('key')  # True/False
cache.forget('key')
cache.flush()     # Clear all
```

### The `remember` pattern
A very common and elegant pattern to cache variables dynamically:

```python
# If 'api_data' exists, return it. Otherwise, execute fetch_slow_api(), cache it for 60s, and return it.
data = cache.remember('api_data', ttl=60, fn=fetch_slow_api)
```

---
[← Previous: Email Service](33-email-service.md) | [Documentation](README.md) | [Next: Background Tasks →](35-background-tasks.md)
