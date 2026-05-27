# Background Tasks

Run heavy functions in background threads so your pages respond instantly. Asok manages a thread pool automatically for you.

## Usage

The recommended way to dispatch background tasks is via the `app.background()` method. This ensures the tasks are managed by the application's lifecycle and correctly shut down on exit.

```python
# src/pages/order/page.py
def post(request):
    app = request.environ.get("asok.app")
    
    def heavy_task(data):
        # Process payment, send receipt, etc.
        pass

    # Dispatch to background pool
    app.background(heavy_task, data=request.form)
    
    request.flash('success', 'Order processing!')
    request.redirect('/success')
```

## 2. Configuration & Backends

By default, Asok uses a local in-memory thread pool for background tasks (`ASOK_QUEUE_BACKEND=local`).

For production environments, you should switch to the **Redis distributed task queue** backend. This persists tasks in Redis and executes them in separate worker processes, protecting against data loss on web server crashes.

### Configuration Options

| Key | Default | Description |
|---|---|---|
| `ASOK_QUEUE_BACKEND` | `"local"` | Queue backend: `"local"` (thread pool) or `"redis"`. |
| `REDIS_URL` | `None` | Redis connection URL (e.g. `redis://localhost:6379/0`). Also accepts `ASOK_REDIS_URL`. |
| `BG_WORKERS` | `10` | Max threads in local pool (only applies when backend is `local`). |

Example in `.env` for production:
```env
ASOK_QUEUE_BACKEND=redis
REDIS_URL=redis://localhost:6379/0
```

### Running the Worker (Redis Mode Only)

When using the `redis` backend, tasks are sent to Redis. You must start one or more standalone worker processes to execute them:

```bash
asok worker
```

*Note: Only module-level functions can be queued on Redis. Lambda functions or nested (local) functions cannot be serialized and will raise a `ValueError`.*

## 3. Standalone Usage

For legacy support or independent usage, you can still use the `background` factory:

```python
from asok import background

background(my_function, arg1, key=val)
```

## Error handling

Errors in background tasks are **logged**, not raised. The user never sees a 500 error from a background task.

```
[2026-04-04 14:32:01] ERROR asok.background: Background task send_webhook failed: ConnectionError(...)
```

## Common use cases

### Webhook / External API call

```python
from asok import background
import urllib.request
import json

def send_webhook(url, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data, {'Content-Type': 'application/json'})
    urllib.request.urlopen(req)

def render(request: Request):
    background(send_webhook, 'https://hooks.slack.com/...', {'text': 'New signup!'})
    return request.html('page.html')
```

### Image processing after upload

```python
from asok import Request, background

def resize_image(filepath):
    # Use PIL or any library
    from PIL import Image
    img = Image.open(filepath)
    img.thumbnail((800, 800))
    img.save(filepath)

def render(request: Request):
    # Save the uploaded file first
    file = request.files['avatar']
    path = f'uploads/{file["filename"]}'
    with open(path, 'wb') as f:
        f.write(file['content'])

    # Resize in background
    background(resize_image, path)

    request.flash('success', 'Photo uploaded!')
    request.redirect('/profile')
```

### Cache warming

```python
from asok import Request, background, Cache
from models.post import Post

cache = Cache()

def warm_cache():
    posts = Post.all(order_by='-created_at', limit=20)
    cache.set('recent_posts', [p.to_dict() for p in posts], ttl=300)

def render(request: Request):
    # Warm cache after creating a new post
    Post.create(title=request.form['title'], body=request.form['body'])
    background(warm_cache)
    request.redirect('/blog')
```

## Mail is already background

`Mail.send()` uses the same pattern internally. You don't need to wrap it with `background()`:

```python
# This is already non-blocking:
Mail.send(to='user@example.com', subject='Hello', body='World')
```

## When NOT to use background

- **Database reads needed for the response** — you need the result now
- **Validation** — must happen before responding
- **Anything the user expects to see immediately** — e.g. updating a counter shown on the page

## Context propagation: `current_request` in background tasks

When you dispatch a task with `background()` from inside a view, Asok **automatically copies the request context** into the background thread. This means `current_request` works transparently inside your task functions — no extra setup needed.

```python
from asok import Request, background, current_request

def send_confirmation_email():
    # current_request is available even though this runs in a background thread
    user = current_request.user
    lang = current_request.lang
    subject = "Welcome!" if lang == "en" else "Bienvenue !"
    Mail.send(to=user.email, subject=subject, body="...")

def post(request: Request):
    # Register user, then send email in background
    User.create(email=request.form['email'])
    background(send_confirmation_email)     # context is copied automatically
    request.redirect('/success')
```

> **Important**: context propagation only works for tasks dispatched **during a request** (inside a `render()` / `post()` view). Tasks triggered outside a request (e.g., from a scheduled cron job) do not have a request context, and accessing `current_request` will raise a `RuntimeError`.

---
[← Previous: Caching](34-caching.md) | [Documentation](README.md) | [Next: Scheduled Tasks →](36-scheduler.md)
