# CLI Reference

> **Keywords:** asok cli commands, create command, database commands, custom cli command, make migration, database migrations, asok migrate

The `asok` command-line tool provides a professional, styled interface to help you create, develop, and manage your project.

## Commands

### `asok create <name>`

Create a new project. Asok features a **Smart Interactive Mode**: if you don't provide any flags, it will guide you through the setup with questions.

```bash
asok create myapp
#   ? Add Tailwind CSS support? [y/N]: y
#   ? Add Admin interface? [y/N]: y
#
# 🚀 Creating Asok project: myapp...
#   ✅ Project 'myapp' created!
```

#### Flags (Direct Mode)
Skip questions by providing flags explicitly:
```bash
asok create myapp --tailwind --admin
```

### `asok createsuperuser`

Create an administrative account. Now uses a conversational, professional prompt system:

```bash
asok createsuperuser
#   CREATE SUPERUSER
#   Enter your email address: admin@example.com
#   Enter your password: 
#   Confirm your password: 
#   ✅ Created 'admin' role with full permissions.
#   ✅ Superuser created: admin@example.com
```

### `asok dev`

Start the development server with auto-reload and **live browser reload**:

```bash
asok dev
#
# DEVELOPMENT SERVER
#   Reloader ● Active (PID: 12345)
#   URL      http://127.0.0.1:8000
#   Tailwind ● Watching...
```

Watches `.py`, `.html`, `.json`, `.css`, `.js` files and **`.env`** across the project (root, `src/`, and `asok/`).

### `asok migrate`

Apply or rollback database migrations. This command manages your database schema version by applying pending migration files or reverting already applied ones.

```bash
asok migrate [options]
```

#### Options

* `--status`: Show the current status of all migrations (applied vs. pending). Displays a checklist where `[X]` indicates applied and `[ ]` indicates pending.
* `--rollback`: Revert migrations. By default, this rolls back the last batch of migrations that were applied together.
* `--steps <N>`: Revert exactly `N` migrations. Must be used in combination with `--rollback`.
* `--to <migration_name>`: Migrate up or down to a specific target migration.
  * If the target migration is not yet applied, all pending migrations up to and including it will be applied.
  * If the target migration is already applied, all migrations applied after it will be rolled back.
* `--reset`: Roll back all applied migrations in the database (reverts the entire schema back to empty/start).
* `--fake`: Update the migrations tracking table without actually running the database schema modification queries.
  * Used to mark pending migrations as applied (when migrating forward).
  * Used to mark applied migrations as reverted (when rolling back).
* `--database <connection_name>`: Specify a specific database routing engine from your configuration (default is the default database connection).

```bash
# Example Usage:
asok migrate                     # Apply all pending migrations
asok migrate --status            # Check which migrations are applied
asok migrate --rollback --steps 2 # Revert the last 2 migrations
asok migrate --to=0002_add_posts # Align schema with migration '0002_add_posts'
```

### `asok make migration <name>`

Detect codebase changes and generate a new declarative database migration file.

```bash
asok make migration <name>
```

Asok includes a **Smart Autodetector** that automatically generates schema migrations for you:
1. **Analyze Codebase:** It imports all model classes defined under `src/models/` to understand the current schema you want.
2. **Reconstruct History:** It reads and executes the operations in all existing migration files inside `src/migrations/` to rebuild the historical state of the database.
3. **Diff Schema:** It compares the current model definitions against the historical state.
4. **Generate File:** If any schema differences (like added tables, new columns, altered fields, or removed indices) are detected, it creates a new versioned migration file (e.g., `src/migrations/0003_add_phone_to_users.py`) containing the declarative operations representing the differences.

If no changes are detected, the command will simply exit with `No changes detected in models.`.


### `asok db <command>`

Introspect database schema and query execution plan details.

* `asok db schema`: List all database tables, columns, data types, and primary/foreign keys.
* `asok db explain "<query>"`: Show the execution/query plan of a given SQL query using the active database engine.

```bash
asok db schema                   # Inspect Default Database Schema
asok db schema --database=replica # Inspect specific database schema
asok db explain "SELECT * FROM users" # Explain query on default database
```

### `asok dumpdata`

Export database records of registered models to a JSON fixture file.

```bash
asok dumpdata                  # Dump all models to stdout
asok dumpdata --output=f.json  # Dump all models to f.json
asok dumpdata User             # Dump only the 'User' model to stdout
```

Binary database column values (e.g. vector blobs or files) are encoded using Base64 with a `"base64:"` prefix.

### `asok loaddata`

Import/restore database records from a JSON fixture file.

```bash
asok loaddata fixtures.json
```

Existing records are updated (matched by primary key) using standard ORM `.save()`. Non-existent records are inserted using raw SQL statements to preserve the original primary key ID. The entire loading process is wrapped in a database transaction for performance and atomicity.

### `asok seed`

Populate the database with test data:

```bash
asok seed
#
# SEEDING DATA
#   ✅ Seeding complete.
```

### `asok routes`

List all registered routes in a clean, tabular format:

```bash
asok routes
#
# ROUTES
#   URL          HANDLER
#   -----------   ---------------
#   /             page.py
#   /about        page.html
#   /blog/[slug]  page.py
```

### `asok shell`

Open an interactive Python shell with the `app` instance and all your models pre-imported:

```bash
asok shell
#
# Asok Shell (Interactive Python)
# ℹ️ All models and 'app' instance pre-imported.
#
# Output: Asok shell with models loaded (User, Post, Comment)
# Python 3.12
# >>> User.count()
```

### `asok image`

Manage your Image Optimization system (WebP conversion).

- `asok image --install`: Download the `cwebp` standalone binary.
- `asok image --enable`: **Enable optimization on an existing project**. Installs binary and sets `IMAGE_OPTIMIZATION=true` in `.env`.
- `asok image --optimize`: **Full project scan**. Converts all existing JPG/PNG images in `src/partials/` and `src/uploads/` to WebP.

### `asok tailwind`

Manage your Tailwind CSS integration.

- `asok tailwind --install`: Download the binary.
- `asok tailwind --build`: Run a one-shot build.
- `asok tailwind --enable`: **Setup Tailwind on an existing project** (adds imports to CSS and links to HTML).

### `asok admin`

Manage the Admin interface.

- `asok admin --enable`: **Retro-fit the Admin interface** into an existing project. Handles `wsgi.py` updates and `User` model scaffolding.

### `asok make <type> <name>`

Scaffold new project components:
- `asok make model User`
- `asok make middleware Auth`
- `asok make page Dashboard`
- `asok make component SearchBar`

> To generate database migrations, use the specialized [asok make migration <name>](#asok-make-migration-name) command instead.


### `asok build`

Generate an optimized production distribution in the `dist/` folder:

```bash
asok build                     # Standard optimized build
asok build --with-db           # Include current database
asok build --output my-dist    # Custom output folder
asok build --keep-source       # Keep .py files alongside .pyc
```

The build process includes:
- **Minification**: Recursive JS/CSS and HTML minification.
- **Bytecode**: Compilation of all Python files to `.pyc` (sources removed).
- **Images**: Automatic WebP conversion if enabled.
- **Production Config**: Generation of `.env.production`.

### `asok preview`

Run the application in production mode locally:

```bash
asok preview
#
# PREVIEW SERVER (PRODUCTION MODE)
#   URL  http://127.0.0.1:8000
# ℹ️ No auto-reload — restart manually after changes
```

### `asok worker [action]`

Start the background task queue worker process, or view queue status (only when using the `redis` background queue backend):

* `asok worker` (or `asok worker run`): Starts the worker process. It listens to queues defined by the `ASOK_WORKER_QUEUES` environment variable (default: `high,default,low`).
* `asok worker status`: Connects to Redis and displays the pending task count and details for each queue (`high`, `default`, `low`, and the Dead Letter Queue `asok:dlq`).

```bash
asok worker status
#
# ASOK QUEUE STATUS
#   Backend: redis
#   Redis URL: redis://localhost:6379/0
# --------------------------------------------------
#   Queue: asok:queue:high | Pending tasks: 0
#     ✓ No pending tasks.
#
#   Queue: asok:queue:default | Pending tasks: 2
#     Next tasks to process:
#
#      1. src.tasks.send_email('user@example.com')
#      2. src.tasks.generate_report(42)
#
#   Queue: asok:queue:low | Pending tasks: 0
#     ✓ No pending tasks.
#
#   Queue: asok:dlq | Pending tasks: 0
#     ✓ No pending tasks.
```

### `asok test [path]`

Discover and run unit tests in your project using the built-in test runner.

```bash
asok test            # Run all tests in the 'tests/' directory
asok test tests/unit # Run tests in a specific directory or file
```

### `asok deploy`

Generate production deployment configuration files (Nginx, Gunicorn, SystemD, setup script) for your project.

```bash
asok deploy                     # Standard configuration setup
asok deploy --prod-dir=/var/www # Custom production directory path
```

### `asok assets`

Manage JavaScript and CSS assets in your project.

* `asok assets --install`: Download the `esbuild` standalone binary for asset minification.
* `asok assets --minify`: Minify JS/CSS assets in `src/partials` recursively.

---
[← Previous: Internationalization (i18n)](37-internationalization.md) | [Documentation](README.md) | [Next: Deployment →](39-deployment.md)

