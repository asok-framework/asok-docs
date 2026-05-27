# Getting Started

Asok is a **zero-dependency** Python framework designed for speed, security, and a unified development experience through intuitive file-based routing and native client-side reactivity.

## Installation

By default, Asok has **zero external dependencies** and works out of the box with SQLite.

```bash
# Default installation (SQLite, zero dependencies)
pip install asok

# Optional backends (PostgreSQL, MySQL, Redis)
pip install "asok[postgres]"
pip install "asok[mysql]"
pip install "asok[redis]"

# Combined optional extras (e.g. Postgres + Redis)
pip install "asok[postgres,redis]"
```

> **💡 Note for VS Code Users:** For the best developer experience, we highly recommend installing the official **[Asok VS Code Extension](https://marketplace.visualstudio.com/items?itemName=AsokFramework.asok-vscode)**. It provides native autocompletion, reactive snippets, and integrated CLI commands directly in your editor.

## Create a project

Asok features a **smart interactive CLI**. Just run the create command and it will guide you through the setup:

```bash
asok create myapp
# ? Add Tailwind CSS support? [y/N]: y
# ? Add Admin interface? [y/N]: y
# ? Add Image Optimization (WebP)? [y/N]: y
```

If you prefer to skip questions, use flags: `asok create myapp --tailwind --admin --image`.

Run the server:

```bash
asok dev
```

Open http://127.0.0.1:8000 — your app is running with **live browser reload**. Edit any file and the browser refreshes automatically.

Want a different port? Use `asok dev -p 3000`. If the port is busy, Asok finds the next free one automatically.

## Project structure

```text
myapp/
├── .env                        # Environment variables
├── src
│   ├── components               # Reactive (Live) Components
│   ├── locales                  # Translation files (en.json, fr.json)
│   │   ├── en.json
│   │   └── fr.json
│   ├── middlewares              # Middleware handlers
│   ├── models                   # Database models
│   │   └── user.py
│   ├── pages                    # Routes (file-based)
│   │   ├── page.html (or .asok)
│   │   └── page.py
│   └── partials                 # Shared assets
│       ├── css
│       │   └── base.css
│       ├── html
│       │   └── base.html
│       ├── images
│       │   └── logo.svg
│       ├── js
│       │   └── base.js
│       └── uploads
└── wsgi.py                   # Entry point
```

## How it works

1. A request arrives at `/contact`
2. Asok looks for `src/pages/contact/page.py` (or `page.html` / `page.asok`)
3. It calls the `render(request)` function
4. Your function returns HTML via `request.html('page.html')`
5. Asok sends the response

That's it. No decorators, no `app.route()`, no configuration file. Your folder structure **is** your routing.

## Minimal example

```python
# src/pages/page.py
from asok import Request

def render(request: Request):
    return request.html('page.html')
```

```html
<!-- src/pages/page.html -->
<h1>Hello, Asok!</h1>
```

## Configuration

All config goes in `.env`:

```env
DEBUG=true
SECRET_KEY=change-me-in-production
```

Access in code:

```python
request.env('SECRET_KEY')
request.env('DEBUG')  # Returns True (auto-cast)
```

## What's included (zero dependencies)

| Feature | How |
|---|---|
| Routing | Folder-based, automatic |
| Database | SQLite ORM built-in (0 dependencies) |
| Templates | Built-in, high-performance engine |
| Forms | Declarative, auto-validated |
| Auth | Login/logout/sessions |
| i18n | JSON locale files |
| Mail | SMTP via stdlib |
| Cache | Memory or file-based |
| CSRF | Automatic protection |
| CLI | Generators, migrations, seeder |
| Testing | WSGI test client |

Everything runs on the Python standard library by default. No `pip install` is needed beyond `asok` itself unless you opt-in to PostgreSQL, MySQL, or Redis backends.

---
[Documentation](README.md) | [Next: Routing →](02-routing.md)
