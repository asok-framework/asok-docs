# Sessions

> **Keywords:** session store, session cookie, cookie expiration, file session, memory session, session lifespan, session lifetime

Server-side sessions with signed cookie IDs.

## Usage

```python
from asok import Request

def render(request: Request):
    # Read
    username = request.session.get("username")

    # Write
    request.session["username"] = "alice"
    request.session["cart"] = [1, 2, 3]

    return request.html("page.html")
```

Sessions are lazy-loaded on first access. Modified sessions are automatically saved when the response is sent.

`SESSION_MAX_AGE` controls the browser cookie lifetime, while `SESSION_TTL` controls how long the server keeps session data before expiring it.

## Configuration

| Key | Default | Description |
|---|---|---|
| `SESSION_BACKEND` | `"memory"` | `"memory"`, `"file"`, or `"redis"` |
| `SESSION_PATH` | `".sessions"` | Directory for file backend |
| `SESSION_MAX_AGE` | `2592000` | Browser cookie lifetime in seconds |
| `SESSION_TTL` | `86400` | Session lifetime in seconds |
| `REDIS_URL` | `None` | Redis connection URL (e.g. `redis://localhost:6379/0`) |

## Cookie Security

### SameSite attribute

Asok uses two types of session cookies with different security policies:

1. **Primary session cookie (`asok_sid`)**: Uses `SameSite=Strict` for maximum CSRF protection. This is the main session identifier used by the framework.

2. **Public session cookie (`asok_session`)**: Uses `SameSite=Lax` by default, which is appropriate for public-facing applications where users may arrive via external links (email, social media, etc.).

The `Lax` policy allows the cookie to be sent on top-level navigations (e.g., clicking a link from another site), while still preventing it from being sent in most cross-site scenarios. This provides a good balance between security and usability for public applications.

#### Configure SameSite policy

You can override the default `Lax` policy if needed:

```python
# In wsgi.py
app.config["SESSION_SAMESITE"] = "Strict"  # or "Lax" (default) or "None"
```

Or via `.env`:

```env
SESSION_SAMESITE=Strict
```

> **Note**: Using `SameSite=Strict` provides stronger CSRF protection but may break user experience in scenarios where users arrive from external links (they will need to login again). `SameSite=Lax` (default) is the recommended setting for most public-facing applications.

> **Warning**: Setting `SameSite=None` requires the `Secure` flag (HTTPS only) and should only be used in specific cross-site scenarios (e.g., embedded iframes).

### Session Lifetime (TTL)

The `SESSION_TTL` configuration controls how long session data persists on the server before expiring. The default value is **86400 seconds (24 hours)**.

#### Production Security Recommendations

For security-sensitive applications (financial, healthcare, admin panels), reduce the session lifetime to **1-2 hours** to minimize the window of opportunity for session hijacking attacks:

```env
# .env - Recommended for sensitive applications
SESSION_TTL=3600   # 1 hour
# or
SESSION_TTL=7200   # 2 hours
```

Or in `wsgi.py`:

```python
app.config["SESSION_TTL"] = 3600  # 1 hour
```

#### Guidelines by Application Type

| Application Type | Recommended TTL | Reasoning |
|---|---|---|
| **Public websites** | 86400s (24h) | Default - Good balance between UX and security |
| **E-commerce** | 7200s (2h) | Moderate security, prevents abandoned cart session reuse |
| **Banking/Finance** | 1800-3600s (30min-1h) | High security, short exposure window |
| **Admin panels** | 3600s (1h) | High security, administrative privileges require shorter sessions |
| **Healthcare (HIPAA)** | 900-1800s (15-30min) | Compliance requirement, PHI protection |

> **Note**: `SESSION_TTL` differs from `SESSION_MAX_AGE`:
> - `SESSION_TTL`: Server-side session data lifetime (how long data is stored)
> - `SESSION_MAX_AGE`: Client-side cookie lifetime (how long browser keeps the cookie)
>
> For maximum security, set both to the same value. For better UX, you can set `SESSION_MAX_AGE` longer and implement "remember me" functionality separately.

#### Auto-expiration

Sessions automatically expire after `SESSION_TTL` seconds of inactivity. The timer resets on each request that modifies the session. Expired sessions are:
- Removed from memory backend automatically
- Cleaned up from file backend on next access attempt
- Cleaned up natively and automatically by Redis (when using the `redis` backend, which uses native Redis key expiration)

> **Production Tip**: For file-based sessions, implement a cron job to periodically clean up expired session files:

```bash
# Cleanup sessions older than SESSION_TTL
find /run/asok/sessions -type f -mtime +1 -delete
```

### File backend

```python
app.config["SESSION_BACKEND"] = "file"
app.config["SESSION_PATH"] = ".sessions"
```

Sessions are stored as JSON files in the specified directory.

## How it works

1. A signed cookie (`asok_sid`) identifies the session
2. Session data is stored server-side (memory or file)
3. On first `request.session` access, data is loaded from the store
4. If `session.modified` is `True` at response time, data is saved back

## Session API

`request.session` behaves like a regular `dict`:

```python
request.session["key"] = "value"
request.session.get("key", "default")
del request.session["key"]
request.session.pop("key")
request.session.clear()
```

All mutating operations automatically set `session.modified = True`.

## Production Persistence

> In production environments using multi-worker servers like **Gunicorn**, you **must** use either the `file` or the `redis` backend. 
> 
> The default `memory` backend stores sessions in the RAM of the specific worker process. Since requests are distributed across multiple workers, a user will "lose" their session as soon as their request is handled by a different worker.

### Option A: Redis backend (Recommended)
Redis stores sessions in-memory, sharing them instantly across all worker processes and even multiple servers, while remaining extremely fast.

To use Redis, install the optional extra:
```bash
pip install "asok[redis]"
```

Configure your `.env` file:
```env
SESSION_BACKEND=redis
REDIS_URL=redis://localhost:6379/0
```

### Option B: File backend
To ensure persistence across workers using files, configure the `file` backend in your `.env` or `wsgi.py`:

```env
# .env
SESSION_BACKEND=file
SESSION_PATH=/run/asok/sessions
```

> **Note**: If you are using SystemD `RuntimeDirectory=asok`, the path `/run/asok` is automatically managed and has the correct permissions for the web server user.

Adjust `SESSION_MAX_AGE` and `SESSION_TTL` separately if you want the cookie lifetime and server-side lifetime to differ.

For RHEL/AlmaLinux servers, see the [Deployment](39-deployment.md) guide for handling SELinux permissions.

---
[← Previous: Advanced Authentication](18-advanced-authentication.md) | [Documentation](README.md) | [Next: Security Headers →](20-security-headers.md)
