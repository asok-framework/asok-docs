# Scheduled Tasks

> **Keywords:** scheduled tasks, cron jobs, background scheduler, cron expression, periodic task

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

> Since the built-in scheduler runs in local background threads (daemon threads), a copy of the scheduler will start inside **each** worker process.
> 
> If you run Gunicorn with 4 workers, your scheduled tasks will run **4 times in parallel** (one in each worker). This can cause duplicate database entries, double emails, or resource conflicts.

### Solution A: Built-in Redis Distributed Lock (Automated & Recommended)

If your project is configured to use the **Redis queue backend** (`ASOK_QUEUE_BACKEND=redis`), Asok **automatically handles distributed locking** for you. 

Before running any scheduled task, the scheduler attempts to acquire an exclusive lock on Redis (`asok:lock:scheduler:{module_name}:{func_name}`) using `SETNX` with a TTL equal to 90% of the task's interval (capped at a maximum of 1 hour).
* If the lock is successfully acquired, the task runs in that process.
* If another process/worker holds the lock, the task is skipped in the current cycle.

This ensures that regardless of how many containers or Gunicorn workers you run, each scheduled task executes exactly **once per interval** across the entire cluster without any additional boilerplate.

### Solution B: System Cron + Custom Command (Fallback)

If you do not use Redis, you should disable the built-in scheduler for your web workers and trigger tasks via standard system cron jobs calling an Asok CLI command:

1. Create a custom command (e.g. `src/commands/cleanup.py`):
```python
def handle():
    # Your cleanup task here
    print("Cleanup completed.")
```
2. Configure a cron job on your server (`crontab -e`):
```text
# Run every hour
0 * * * * cd /var/www/myapp && ./venv/bin/asok cleanup >> /var/log/asok-cron.log 2>&1
```
