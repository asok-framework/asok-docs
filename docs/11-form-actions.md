# Form Actions

Native Form Actions allow you to handle form submissions without writing complex routing logic. Instead of manually checking `if request.method == "POST"` in your `render` function, you can define specific action functions that Asok will call automatically.

Form Actions follow Asok's philosophy: **simple, explicit, and secure by default**.

## The `action_[name]` Convention

If a page module contains a function named `action_XYZ`, Asok will automatically call it when a `POST` request is received with an action identifier `XYZ`.

The action identifier can be provided in two ways:
1.  **Hidden field**: `<input type="hidden" name="_action" value="XYZ">` (Recommended)
2.  **URL Parameter**: `?action=XYZ`

### Security

Asok validates action names to prevent security exploits:
- ✅ **Allowed**: Alphanumeric characters, underscores, and hyphens (`delete`, `save_draft`, `export-pdf`)
- ❌ **Blocked**: Private actions starting with `_` (`_private`, `__init__`)
- ❌ **Blocked**: Path traversal attempts (`../admin`, `../../etc/passwd`)
- ❌ **Blocked**: Non-alphanumeric characters (`system('rm')`, `<script>`)

## Why use Form Actions?

- **Reduced Boilerplate**: Separate your rendering logic from your data mutation logic.
- **Type Safety**: Your action functions receive the same `Request` object.
- **Clear Intent**: It's obvious what part of the code handles which action.

## Example: Create a Post

`src/pages/new_post.py`:
```python
from asok import Request

# This function only handles the GET / display
def render(request: Request):
    return request.html("new_post.html")

# This function only handles the data submission
def action_create(request: Request):
    title = request.form.get("title")
    content = request.form.get("content")
    
    if not title:
        return request.html("new_post.html", error="Title is required")
    
    # Save to database...
    # DB.posts.create(title=title, content=content)
    
    return request.redirect("/")
```

`src/pages/new_post.html`:
```html
<h1>New Post</h1>

{% if error %}
    <p style="color: red">{{ error }}</p>
{% endif %}

<form method="POST">
    <input type="hidden" name="_action" value="create">
    
    <div>
        <label>Title</label>
        <input type="text" name="title">
    </div>
    
    <div>
        <label>Content</label>
        <textarea name="content"></textarea>
    </div>
    
    <button type="submit">Publish</button>
</form>
```

## Multiple Actions in one Page

You can have multiple actions in the same file to handle different buttons or forms.

`src/pages/posts/[id].py`:

```python
from asok import Request
from models.Post import Post

def get(request: Request):
    """Display post details."""
    post = Post.find(id=request.params.get("id"))
    return request.html("post.html", post=post)

def action_delete(request: Request):
    """Delete a post."""
    post_id = request.form.get("id")
    Post.destroy(id=post_id)
    request.flash("Post deleted successfully", "success")
    request.redirect("/posts")
    # redirect() raises RedirectException - no need to return

def action_publish(request: Request):
    """Publish a draft post."""
    post_id = request.form.get("id")
    post = Post.find(id=post_id)
    post.update(published=True, published_at="NOW()")
    request.flash(f'Post "{post.title}" published!', "success")
    # Return HTML to show updated post
    return request.html("post.html", post=post)

def action_archive(request: Request):
    """Archive a post."""
    post_id = request.form.get("id")
    post = Post.find(id=post_id)
    post.update(archived=True)
    request.flash("Post archived", "info")
    request.redirect("/posts")
```

`src/pages/posts/post.html`:

```html
<div class="post-details">
    <h1>{{ post.title }}</h1>
    <p>{{ post.content }}</p>

    <form method="POST">
        <input type="hidden" name="id" value="{{ post.id }}">

        {% if not post.published %}
            <button type="submit" name="_action" value="publish">
                📤 Publish
            </button>
        {% endif %}

        <button type="submit" name="_action" value="archive">
            📦 Archive
        </button>

        <button type="submit" name="_action" value="delete"
                onclick="return confirm('Delete this post?')">
            🗑️ Delete
        </button>
    </form>
</div>
```

## Best Practices

### ✅ DO: Return a Response

Actions must return either:

- `request.html(template, **context)` - Render HTML
- `request.json(data)` - Return JSON
- `request.redirect(url)` - Redirect (raises exception, no return needed)

```python
def action_save(request: Request):
    # ✅ Good - returns HTML
    return request.html("success.html")

def action_delete(request: Request):
    # ✅ Good - redirect (raises exception)
    request.redirect("/posts")
    # This line won't execute

def action_status(request: Request):
    # ✅ Good - returns JSON
    return request.json({"status": "ok"})
```

### ❌ DON'T: Return None

If your action doesn't call `redirect()`, you **must** return a response:

```python
def action_broken(request: Request):
    Post.destroy(id=request.form.get("id"))
    # ❌ ERROR: Returns None (forgot to redirect or return HTML)
```

This will result in:

```text
500 Internal Server Error
Action handler 'action_broken' returned None.
Ensure your action returns request.html(), request.json(), or calls request.redirect().
```

### ✅ DO: Use Flash Messages

Flash messages provide user feedback after actions:

```python
def action_update(request: Request):
    post = Post.find(id=request.form.get("id"))
    post.update(title=request.form.get("title"))

    # Flash message (stored in session, shown once)
    request.flash("Post updated successfully!", "success")

    # Types: "success", "info", "warning", "danger"
    request.redirect(f"/posts/{post.id}")
```

### ✅ DO: Validate Input

Always validate and sanitize user input:

```python
def action_create(request: Request):
    title = request.form.get("title", "").strip()

    # Validate
    if not title:
        request.flash("Title is required", "danger")
        return request.html("new_post.html", form_data=request.form)

    if len(title) > 200:
        request.flash("Title is too long (max 200 chars)", "danger")
        return request.html("new_post.html", form_data=request.form)

    # Create post
    post = Post.create(title=title)
    request.redirect(f"/posts/{post.id}")
```

### ✅ DO: Use Naming Conventions

Use clear, descriptive action names:

```python
# ✅ Good - clear intent
def action_delete(request): ...
def action_save_draft(request): ...
def action_export_pdf(request): ...
def action_send_email(request): ...

# ❌ Bad - vague or confusing
def action_do_thing(request): ...
def action_x(request): ...
def action_process(request): ...
```

## Common Patterns

### Pattern: Inline Validation

```python
def action_update(request: Request):
    """Update post with inline validation."""
    post_id = request.form.get("id")
    title = request.form.get("title", "").strip()

    errors = {}

    if not title:
        errors["title"] = "Title is required"
    elif len(title) > 200:
        errors["title"] = "Title too long (max 200 chars)"

    if errors:
        # Show form again with errors
        post = Post.find(id=post_id)
        return request.html("edit.html", post=post, errors=errors)

    # Update and redirect
    post = Post.find(id=post_id)
    post.update(title=title)
    request.flash("Post updated!", "success")
    request.redirect(f"/posts/{post.id}")
```

### Pattern: Conditional Actions

```python
def action_publish(request: Request):
    """Publish post - admin only."""
    if not request.user or not request.user.is_admin:
        request.flash("Admin access required", "danger")
        request.redirect("/posts")

    post = Post.find(id=request.form.get("id"))

    if post.published:
        request.flash("Post already published", "warning")
        return request.html("post.html", post=post)

    post.update(published=True)
    request.flash("Post published!", "success")
    request.redirect(f"/posts/{post.id}")
```

## Technical Details

### Execution Order

When a `POST` request is received, Asok checks in this order:

1. **Form Actions** (if `_action` param exists)
   - Look for `action_{name}` function
   - If found, call it and return result
   - If action returns `None`, raise 500 error

2. **HTTP Method Function** (if no action matched)
   - Look for `post()` function
   - If found, call it and return result

3. **Fallback to `render()`** (if no method function)
   - Call `render(request)` function
   - Handles both GET and POST

### Why POST Only?

Form Actions only trigger on `POST` requests for security:

- **GET requests should be safe** - No side effects (RESTful design)
- **POST for mutations** - Create, update, delete operations
- **CSRF protection** - POST requests include CSRF tokens

> [!NOTE]
> Form Actions only trigger for `POST` requests for security reasons (mutation should never happen on GET).

---
[← Previous: Advanced Forms](10-advanced-forms.md) | [Documentation](README.md) | [Next: Validation →](12-validation.md)
