# Scheduled Tasks

Run recurring functions at regular intervals. Asok provides a built-in scheduler integrated into the application lifecycle.

## Quick Start

The recommended way to schedule tasks is via the `app.schedule()` method in your `wsgi.py`. This ensures tasks are automatically stopped when the server shuts down.

```python
from asok import Asok

app = Asok()

def cleanup():
    print("Cleaning up old logs...")

# Schedule every 10 minutes
app.schedule("10m", cleanup)
```

## 2. Timing Syntax

Asok supports human-readable strings for defining intervals:

- `"30s"`: Every 30 seconds
- `"5m"`: Every 5 minutes
- `"2h"`: Every 2 hours
- `"1d"`: Every day
- `"1w"`: Every week (7 days)
- `"1mo"`: Every month (30 days)
- `"1y"`: Every year (365 days)

You can still use raw numbers (seconds) if preferred: `app.schedule(3600, cleanup)`.

## 3. Standalone Usage

For tasks independent of the app lifecycle, use the `schedule` factory:

```python
from asok import schedule

task = schedule("1h", my_function)

# Manually cancel if needed
task.cancel()
```

## 4. Error Handling

Exceptions in scheduled tasks are caught and logged automatically. The task will continue to run at the next scheduled interval even if one execution fails.

## 5. Production & Multi-Process Environments

In a production environment, you typically deploy Asok with a multi-process web server like **Gunicorn** or **Uvicorn** (configured with multiple workers).

> [!WARNING]
> Since the built-in scheduler runs in local background threads (daemon threads), a copy of the scheduler will start inside **each** worker process.
> 
> If you run Gunicorn with 4 workers, your scheduled tasks will run **4 times in parallel** (one in each worker). This can cause duplicate database entries, double emails, or resource conflicts.

### Solution A: System Cron + Custom Command (Recommended)

For tasks that must run exactly once, the best practice is to disable the built-in scheduler in your `wsgi.py` / `asgi.py` for web workers, and instead trigger them via a standard system cron job calling an Asok CLI command.

1. Create a custom command (e.g. `src/commands/cleanup.py`):
```python
def handle():
    # Your cleanup task here
    print("Cleanup completed.")
```
2. Configure a cron job on your server (`crontab -e`):
```cron
# Run every hour
0 * * * * cd /var/www/myapp && ./venv/bin/asok cleanup >> /var/log/asok-cron.log 2>&1
```

### Solution B: Redis Distributed Lock

If your application already uses Redis, you can use a Redis lock (via the `redis` package) to ensure that even if multiple workers attempt to run the task, only one obtains the lock and executes it:

```python
import redis
import os

def cleanup():
    redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    client = redis.Redis.from_url(redis_url)
    
    # Attempt to acquire a lock for 10 minutes
    lock = client.lock("asok:locks:cleanup", timeout=600)
    if lock.acquire(blocking=False):
        try:
            # Perform the cleanup task
            print("Cleaning up old logs...")
        finally:
            lock.release()
```

---
[← Previous: Background Tasks](35-background-tasks.md) | [Documentation](README.md) | [Next: Internationalization (i18n) →](37-internationalization.md)

