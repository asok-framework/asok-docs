# Request Context & `current_request`

> **Keywords:** thread safe proxy, request context, thread context, request data

Asok uses a **context-local request proxy** to make the current HTTP request available anywhere in your code — without threading issues and without passing `request` as a function argument everywhere.

## The problem it solves

In a normal Asok view you always have `request` as a parameter:

```python
def render(request: Request):
    user = request.user
    return request.html("page.html", user=user)
```

But as your app grows, you'll have services, helpers, and utilities that need to read request data. Without `current_request` you'd have to thread `request` through every call:

```python
# ❌ Without current_request — cascading parameters
def render(request: Request):
    data = build_dashboard(request)

def build_dashboard(request):
    stats = compute_stats(request)

def compute_stats(request):
    if request.user.is_admin:   # only here do you actually use it
        ...
```

`current_request` eliminates this cascade:

```python
# ✅ With current_request — clean call chain
from asok import current_request

def render(request: Request):
    data = build_dashboard()    # no request parameter

def build_dashboard():
    return compute_stats()

def compute_stats():
    if current_request.user.is_admin:   # direct access
        ...
```

## Import

```python
from asok import current_request
```

`current_request` is the **only** global request proxy in Asok.

## How it works

Internally, Asok stores the active `Request` object in a `contextvars.ContextVar`. Every time the framework receives an HTTP request or a WebSocket message, it sets this variable. `current_request` is a proxy that delegates every attribute access, method call, and assignment to whatever is currently stored in that variable.

This makes it:
- **Thread-safe** — each thread/coroutine has its own context
- **Zero-copy** — the proxy doesn't copy the request, it just delegates

## Where it works

| Context | Available? |
|---|---|
| Inside `render()` / `post()` view functions | ✅ Yes |
| Inside a `Component.render()` method | ✅ Yes (WebSocket context is set up automatically) |
| Inside a `background()` task dispatched from a view | ✅ Yes (context is copied automatically via `contextvars`) |
| Inside a `@ws.on()` WebSocket message handler | ✅ Yes |
| At module level / app startup | ❌ No — raises `RuntimeError` |
| Inside a scheduled cron job | ❌ No — raises `RuntimeError` |

## Checking if a request is active

```python
from asok import current_request

if current_request:         # bool(current_request) → False outside context
    user = current_request.user
```

Or use the context manager directly for manual control:

```python
from asok.context import request_context

with request_context(my_request):
    # current_request is available here
    user = current_request.user
```

## Complete example: layered services

```python
# services/dashboard.py
from asok import current_request
from models import Post, Comment

def get_feed():
    """Returns posts visible to the current user."""
    user = current_request.user
    if user and user.is_admin:
        return Post.all(order_by="-created_at", limit=50)
    return Post.where(public=True).order_by("-created_at").limit(20).all()

def get_unread_count():
    """Returns the number of unread comments for the current user."""
    user = current_request.user
    if not user:
        return 0
    return Comment.where(user_id=user.id, read=False).count()
```

```python
# pages/dashboard/page.py
from asok import Request
from services.dashboard import get_feed, get_unread_count

def render(request: Request):
    feed = get_feed()               # uses current_request internally
    unread = get_unread_count()     # same
    return request.html("dashboard.html", feed=feed, unread=unread)
```

## `current_request` in background tasks

When you dispatch a background task from within a view, the request context is **automatically propagated** to the background thread:

```python
from asok import Request, background, current_request

def notify_admin():
    # This runs in a background thread — but current_request is still valid!
    user = current_request.user
    Mail.send(
        to="admin@example.com",
        subject="New signup",
        body=f"{user.email} just registered."
    )

def post(request: Request):
    User.create(email=request.form['email'])
    background(notify_admin)    # context is copied automatically
    request.redirect('/success')
```

> **Warning**: context propagation only applies to tasks dispatched **inside a request**. If you call `background()` from a cron job or outside any HTTP context, `current_request` will raise a `RuntimeError` inside the task.

## `current_request` in reactive components

Live components re-render on the server when a WebSocket event arrives. `current_request` is available inside `render()` and all `@exposed` methods:

```python
from asok import Component, current_request
from asok.component import exposed

class ShoppingCart(Component):
    item_count = 0

    @exposed
    def add_item(self, product_id: int):
        # Access the current user directly
        user = current_request.user
        Cart.add(user_id=user.id, product_id=product_id)
        self.item_count += 1

    def render(self):
        lang = current_request.lang
        label = "items in cart" if lang == "en" else "articles dans le panier"
        return f"<div>{self.item_count} {label}</div>"
```

## Error reference

| Error | Cause | Fix |
|---|---|---|
| `RuntimeError: Working outside of request context` | Accessed `current_request` outside an HTTP/WS handler | Move the call inside a view, component method, or background task dispatched from a view |

---
[Documentation](README.md) | [← Request Handling](03-request.md) | [← Background Tasks](35-background-tasks.md)
