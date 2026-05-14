# Logging

Asok provides a centralized, configuration-aware logging system out of the box.

## 1. Application Logger

The recommended way to log messages is via the `app.logger` instance. This logger is automatically configured to respect your application's settings (`LOG_LEVEL`, `LOG_FILE`, etc.).

```python
from asok import Asok

app = Asok()

# Standard logging
app.logger.info("Application initialized")
app.logger.warning("Low disk space")

# Convenient shortcuts
app.log_info("Hello Asok!")
app.log_error("Something went wrong")
```

### Usage in a page

In your `src/pages/page.py`, you can access the app logger via the request environment:

```python
# src/pages/page.py
def render(request):
    app = request.environ.get("asok.app")
    if app:
        app.log_info("User visited the home page")
    return "Welcome to Asok!"
```

## 2. Request Logger Middleware

To log every incoming HTTP request, create `src/middlewares/logger.py`:

```python
from asok import RequestLogger

# Uses app.logger settings automatically
log = RequestLogger()

def handle(request, next):
    return log(request, next)
```

**Output example:**
```text
[2026-05-14 12:00:01] INFO asok.request: GET / 200 OK 3.2ms
[2026-05-14 12:00:02] INFO asok.request: POST /contact 302 Found 12.5ms
```

## 3. Configuration

You can configure logging via your `.env` file or directly in `app.config`.

| Key | Default | Description |
|---|---|---|
| `LOG_LEVEL` | `DEBUG` | Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`). |
| `LOG_FILE` | `None` | Optional path to a file for persistent logging. |
| `LOG_FORMAT`| `text` | Format of logs: `text` or `json`. |

**Example `.env`:**
```env
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
LOG_FORMAT=json
```

## 4. Standalone Logger

For logging in modules where `app` is not available, you can still use `get_logger()`:

```python
from asok import get_logger

logger = get_logger("my_module")
logger.info("Standalone log message")
```

---
[← Previous: Testing](40-testing.md) | [Documentation](README.md) | [Next: Optimization →](42-optimization.md)
