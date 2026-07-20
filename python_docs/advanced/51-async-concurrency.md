# Async & Concurrency

> **Keywords:** async await, concurrent queries, async database, asgi wsgi concurrency

Asok supports dual-core ASGI/WSGI operation. This allows you to deploy Asok applications under ASGI servers (like Uvicorn) for high-concurrency workloads, while maintaining 100% backward compatibility with traditional WSGI deployments (like Gunicorn).

Additionally, Asok supports `async def` page controllers, asynchronous middlewares, and non-blocking asynchronous ORM operations.

## Installation

Asynchronous capabilities are optional to keep the core framework lightweight and dependency-free. To install Asok with ASGI support, run:

```bash
pip install "asok[async]"
```

This installs:
- `uvicorn` — A lightning-fast ASGI server.

## Running with Uvicorn (ASGI)

To start the development server using the ASGI interface rather than the default WSGI server, run:

```bash
uvicorn wsgi:app --reload
```

In production, you can deploy your application with:

```bash
uvicorn wsgi:app --host 0.0.0.0 --port 8000 --workers 4
```


## Async Page Controllers

You can write standard synchronous controllers or asynchronous `async def` page controllers. Asok automatically detects if the controller is a coroutine function and handles it appropriately.

```python
# src/pages/users/page.py
from models.user import User

async def get(request):
    # Perform non-blocking database query
    users = await User.all_async()
    
    return request.html("page.html", users=users)
```

## Async Middleware

Middleware functions can also be declared using `async def`. When running under an ASGI server, the middleware will be awaited correctly.

```python
# src/middlewares/02_async_logger.py
import time

async def handle(request, next):
    start = time.time()
    
    # Propagate to next middleware/handler asynchronously
    response = await next(request)
    
    duration = (time.time() - start) * 1000
    print(f"[{request.method}] {request.path} completed in {duration:.2f}ms (async)")
    return response
```

### Sync-Async Middleware Interoperability

Asok automatically handles mixed chains where some middlewares are synchronous (`def`) and others are asynchronous (`async def`). 
- Under ASGI, synchronous middlewares are wrapped so they run on worker threads without blocking the event loop.
- Under WSGI, asynchronous middlewares/controllers are run to completion using an internal event loop wrapper.

## Asynchronous ORM Operations

Asok Models expose async variants of all standard querying and saving methods.

| Synchronous Method | Asynchronous Equivalent | Description |
|---|---|---|
| `Model.all()` | `await Model.all_async()` | Retrieve all records from the database |
| `Model.find(**kwargs)` | `await Model.find_async(**kwargs)` | Find a single record by field criteria |
| `Model.create(**kwargs)` | `await Model.create_async(**kwargs)` | Instantiates and saves a new record |
| `model.save()` | `await model.save_async()` | Saves updates to an existing model instance |
| `model.delete()` | `await model.delete_async()` | Deletes the model instance from the database |

### Example usage:

```python
# src/pages/profile/page.py
from models.user import User

async def get(request):
    user_id = request.query.get("id")
    
    # Non-blocking find
    user = await User.find_async(id=user_id)
    if not user:
        request.status(404)
        return "User not found"
        
    return request.html("page.html", user=user)

async def post(request):
    name = request.form.get("name")
    
    # Non-blocking save
    user = await User.create_async(name=name, email="new@example.com")
    return request.redirect(f"/profile?id={user.id}")
```

### Under the Hood

The `*_async` ORM methods run database operations on a thread pool (via `asyncio.to_thread`) to guarantee compatibility with all supported database engines (SQLite, PostgreSQL, and MySQL) without duplicating the underlying driver-specific queries.
