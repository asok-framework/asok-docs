# Security Headers

In production, Asok automatically adds security headers to every response.

## Default headers

| Header | Value |
|---|---|
| `X-Content-Type-Options` | `nosniff` |
| `X-Frame-Options` | `DENY` |
| `X-XSS-Protection` | `1; mode=block` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` (HTTPS only) |
| `Content-Security-Policy` | `default-src 'self'; script-src 'self' 'nonce-...' 'strict-dynamic'; style-src 'self' 'unsafe-inline'` |

## Configuration

Security headers are only applied in production (`DEBUG=false`).

### Disable entirely

```python
app.config["SECURITY_HEADERS"] = False
```

### Override specific headers

Pass a dict. Set a value to `None` to remove a header:

```python
app.config["SECURITY_HEADERS"] = {
    "Content-Security-Policy": "default-src 'self'; img-src *",
    "X-Frame-Options": None,  # removes this header
}
```

### Zero-Eval Content Security Policy

Asok directives (`asok-*`) and Live Components are built with **Zero-Eval Security**:
- **No `'unsafe-eval'` required**: All expressions are precompiled on the server and safely registered on the client using cryptographically nonced `<script>` elements. Asok does not invoke `eval()` or `new Function()` in the browser for directives or component state synchronization.
- **Strict CSP out-of-the-box**: This allows production applications to use a strict Content Security Policy that can omit `'unsafe-eval'` by default.
- **Manual Control**: If you use external third-party JavaScript libraries that strictly require `eval()`, you can force `'unsafe-eval'` in the CSP via:

```python
# In wsgi.py
app.config["CSP_UNSAFE_EVAL"] = True  # Forces 'unsafe-eval' in script-src
```

Or via `.env`:
```env
CSP_UNSAFE_EVAL=true
```

---
[← Previous: Sessions](19-sessions.md) | [Documentation](README.md) | [Next: CORS & Gzip →](21-cors-gzip.md)
