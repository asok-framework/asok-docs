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

---
[← Previous: Background Tasks](35-background-tasks.md) | [Documentation](README.md) | [Next: Internationalization (i18n) →](37-internationalization.md)
