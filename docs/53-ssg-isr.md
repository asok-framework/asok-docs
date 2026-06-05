# SSG & ISR (Static Site Generation & Incremental Static Regeneration)

Asok supports hybrid rendering strategies, allowing you to pre-render pages into static HTML at build time (SSG) and incrementally regenerate them in the background (ISR) for the ultimate balance between performance and dynamic features.

---

## 1. Static Site Generation (SSG)

Static Site Generation pre-renders pages into static HTML files during the build phase (`asok build`). When a user requests the page, the server returns the cached HTML instantly with zero database queries or Python processing overhead.

### Enabling SSG for Static Routes
To make any page static, define `SSG = True` at the module level in its page controller (`page.py`).

```python
# src/pages/about/page.py
SSG = True

def get(request):
    # This page will only render once during `asok build`
    return request.html("about.html")
```

### Enabling SSG for Dynamic Routes
For routes with dynamic segments (e.g. `/blog/[slug]`), you must define the `get_static_paths()` function to tell Asok which paths to pre-render at build time.

```python
# src/pages/blog/[slug]/page.py
from src.models import Post

SSG = True

def get_static_paths():
    """Returns a list of dicts mapping parameters to pre-render."""
    posts = Post.all()
    return [{"slug": post.slug} for post in posts]

def get(request):
    slug = request.params["slug"]
    post = Post.where("slug", slug).first()
    return request.html("post.html", post=post)
```

---

## 2. Incremental Static Regeneration (ISR)

Incremental Static Regeneration allows you to update static pages after you've built your site. You can serve static content immediately (instant response) and automatically regenerate the page in the background when a request comes in after a specified interval.

### Enabling ISR
To enable ISR, define the `REVALIDATE` variable (in seconds) in your page controller:

```python
# src/pages/blog/[slug]/page.py
from src.models import Post

SSG = True
REVALIDATE = 3600  # Regenerate in the background at most once per hour

def get_static_paths():
    return [{"slug": post.slug} for post in Post.all()]

def get(request):
    slug = request.params["slug"]
    post = Post.where("slug", slug).first()
    return request.html("post.html", post=post)
```

### How ISR Works under the Hood
1. **Cache Hit (Fresh)**: The request is served instantly from the disk cache under `.asok/ssg_cache/`.
2. **Cache Hit (Stale)**: If the cache age is greater than `REVALIDATE` seconds:
   - The browser receives the cached version immediately (stale).
   - Asok spawns a non-blocking background thread to regenerate the fresh page HTML and update the cache.
   - The next visitor receives the updated page.
3. **On-Demand Generation (Cache Miss)**: If a dynamic route hasn't been pre-generated (e.g. a newly created blog post), Asok generates it on the fly, serves it, and caches it for future requests.

---

## 3. Security: Dynamic CSRF & CSP Injection

A common issue with static site cache systems is that user-specific tokens (like **CSRF tokens** and **CSP nonces**) are accidentally baked into the static HTML. This can lead to security vulnerabilities and broken form submissions.

Asok solves this transparently:
1. When generating pages, Asok compiles the raw HTML and registers directives.
2. It saves a **"clean" version** of the HTML to `.asok/ssg_cache/` (without request-specific nonces/tokens).
3. When serving a cached page, Asok dynamically injects the active request's unique **CSRF tokens** and **CSP nonces** at the byte level before serving.
4. This results in **sub-millisecond serving speeds** while keeping your application fully hardened against XSS and CSRF attacks.

---

## 4. Building and Deploying

During compilation, the production pipeline will automatically build your static site:

```bash
asok build
```

This compiles your Python modules to optimized bytecode, minifies static assets, and triggers static site generation for all pages marked with `SSG = True` or defining `get_static_paths()`.

To serve the generated pages in production, ensure the cache directory is preserved across deployments:
- Local cache path: `.asok/ssg_cache/`
