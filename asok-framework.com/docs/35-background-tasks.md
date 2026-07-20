# Background Tasks

> **Keywords:** non blocking tasks, task worker, background queue, thread pool, async execution

Run heavy functions in background threads so your pages respond instantly. Asok manages a thread pool automatically for you.

## Usage

The recommended way to dispatch background tasks is via the `app.background()` method. This ensures the tasks are managed by the application's lifecycle and correctly shut down on exit.

```python
# src/pages/order/page.py
def post(request):
    app = request.environ.get("asok.app")
    
    # Dispatch to background pool
    app.background(heavy_task, data=request.form)
    
    request.flash('success', 'Order processing!')
    request.redirect('/success')
```

### Advanced Dispatching (Redis Backend Only)

When using the Redis backend, you can fine-tune how tasks are processed:

* **Queues / Priorities**: Route tasks to specific queues using the `_queue` argument (e.g. `_queue="high"`). By default, `"default"` routes to the standard queue `asok:queue`. Other queues map to `asok:queue:{queue_name}`.
* **Automatic Retries**: Enable automatic retries on failure using the `_retries` argument (e.g. `_retries=3`).
* **Backoff Multiplier**: Configure retry delay spacing using `_backoff` (default: `2`). Retries use exponential backoff: `delay = backoff ** retry_count` seconds.

Example:
```python
# Dispatch task to the high-priority queue with 3 retries and 3s exponential backoff base
app.background(heavy_task, data, _queue="high", _retries=3, _backoff=3)
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
| `ASOK_WORKER_CONCURRENCY` | `1` | Number of concurrent execution threads in the Redis worker pool. |
| `ASOK_WORKER_QUEUES` | `"high,default,low"` | Comma-separated list of queue names to pull from (in order of priority). |

Example in `.env` for production:
```env
ASOK_QUEUE_BACKEND=redis
REDIS_URL=redis://localhost:6379/0
ASOK_WORKER_CONCURRENCY=4
ASOK_WORKER_QUEUES=high,default,low
```

### Running the Worker (Redis Mode Only)

When using the `redis` backend, tasks are sent to Redis. You must start one or more standalone worker processes to execute them:

```bash
asok worker
```

#### Inspecting the Queue Status

You can check the status of the Redis queue at any time (e.g., number of pending tasks, next jobs to process) using the `status` command:

```bash
asok worker status
```

This connects to Redis and prints the total number of pending tasks and a list of the next tasks to be processed in execution order.

*Note: Only module-level functions can be queued on Redis. Lambda functions or nested (local) functions cannot be serialized and will raise a `ValueError`.*

### Production Deployment with Systemd

In a production environment, running the worker in the foreground of a terminal is not suitable. Instead, you should manage it as a background service supervised by SystemD.

When you run `asok deploy`, it automatically generates a `{your_project}-worker.service` file for your background worker. To deploy and run it:

1. Copy the generated service file to the SystemD system directory:
   ```bash
   sudo cp deployment/{your_project}-worker.service /etc/systemd/system/
   ```
2. Reload SystemD and enable the service to start on boot:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable {your_project}-worker
   ```
3. Start the worker service:
   ```bash
   sudo systemctl start {your_project}-worker
   ```

The service is configured to automatically restart if it encounters an unexpected error or crash. You can monitor the worker's real-time logs using:
```bash
journalctl -u {your_project}-worker -f
```

## 3. Standalone Usage

For legacy support or independent usage, you can still use the `background` factory:

```python
from asok import background

background(my_function, arg1, key=val)
```

## Error handling & Job Tracking

### Result Backend

When you dispatch a background task using the Redis backend, the task's future holds a `job_id` property. You can use this ID to inspect the status of the job in Redis:

```python
future = app.background(my_heavy_task)
job_id = future.job_id  # UUID of the job
```

Each job has a corresponding Redis key `asok:job:{job_id}` containing status metadata with a 24-hour expiration (TTL). The state transitions through the following lifecycle:
* `pending`: The task is enqueued and waiting to be picked up by a worker.
* `running`: A worker has started executing the task.
* `completed`: The task finished successfully. The key stores the return value of the task function in the `result` field.
* `retrying`: The task failed, and has been scheduled for a retry (stored in `asok:delayed_tasks`).
* `failed`: The task failed permanently (all retries exhausted). The key stores the exception traceback in the `error` field.

Errors in background tasks are **logged**, not raised to the user. The user never sees a 500 error from a background task:

```
[2026-04-04 14:32:01] ERROR asok.background: Background task send_webhook failed: ConnectionError(...)
```

### Dead Letter Queue (DLQ)

If a task fails repeatedly and runs out of retry attempts, Asok automatically routes the job payload to the **Dead Letter Queue** (`asok:dlq`). This isolates failing jobs and prevents them from clogging up active processing queues.

You can inspect the status of all queues, including the DLQ, at any time using the status command:
```bash
asok worker status
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
