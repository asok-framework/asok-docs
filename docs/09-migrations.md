# Database Migrations

Asok includes a professional, version-controlled migration system that allows you to manage your database schema evolution with confidence. It features **automatic change detection**, batch tracking, and atomic rollbacks.

## 1. Concept

Instead of modifying your database manually or relying solely on automatic schema updates, you define your schema in your **Models**. Asok then detects the differences between your code and the actual database state, generating versioned migration files in `src/migrations/`.

## 2. Generating Migrations

When you add a new model or modify an existing one (adding fields), run the following command:

```bash
asok make migration add_phone_to_users
```

Asok will perform a deep analysis of your models and current database schema, then create a file like `src/migrations/0001_add_phone_to_users.py`.

### What Asok Detects
- **New Tables**: Automatically generates `CREATE TABLE` with all fields, constraints (UNIQUE, NOT NULL), and default values.
- **New Columns**: Detects missing columns in existing tables and generates `ALTER TABLE ADD COLUMN` statements.
- **Indexes**: (Future) detects missing indexes.

### Anatomy of a Migration File
A migration file contains two functions:
- `up(conn)`: The SQL changes to apply.
- `down(conn)`: The SQL changes to revert (rollback).

```python
"""
Asok Migration: add_phone_to_users
Generated at: 2024-05-08 10:00:00
"""

def up(conn):
    """Apply changes."""
    conn.execute("ALTER TABLE users ADD COLUMN phone TEXT DEFAULT ''")

def down(conn):
    """Revert changes."""
    # SQLite has limited DROP COLUMN support in older versions
    # Asok logs a comment here if it cannot safely generate the revert SQL
    pass
```

## 3. Applying Migrations

To apply all pending migrations:

```bash
asok migrate
```

### Specifying a Database

You can apply migrations to a specific database backend by using the `--database` option (accepts a configured database name or a DSN connection string):

```bash
asok migrate --database=read_replica
```

Asok tracks applied migrations in a special `_asok_migrations` table. Migrations are executed in **batches**. All migrations run in a single `asok migrate` call belong to the same batch.

## 4. Checking Status

To see the history of applied migrations and what is pending:

```bash
asok migrate --status
```

Output example:
```text
MIGRATION STATUS
  [X] 0001_initial_schema
  [X] 0002_add_user_bio
  [ ] 0003_create_posts_table
```

## 5. Rolling Back & Target Migrations

Asok provides flexible options to undo schema changes, target specific versions, or reset the database completely:

### Revert the last batch
By default, rolling back reverts the most recent batch of migrations:
```bash
asok migrate --rollback
```
This will execute the `down()` function of every migration in the most recent batch and remove them from the tracking table.

### Revert a specific number of migrations
You can specify exactly how many migrations you want to roll back (regardless of their batch number) using `--steps`:
```bash
asok migrate --rollback --steps 3
```

### Migrate or Rollback to a specific version
You can force the database to align with a specific migration name or prefix using `--to`. If the target migration is currently applied, Asok will roll back any migrations applied *after* it. If it is pending, Asok will apply all migrations *up to and including* it:
```bash
asok migrate --to=0002_add_user_bio
```

### Reset all migrations
To rollback all applied migrations in reverse chronological order and return to an empty database state:
```bash
asok migrate --reset
```

## 6. Advanced Options

### Faking Migrations
If your database is out of sync but the schema is correct, you can "fake" a migration:

```bash
asok migrate --fake
```

This marks pending migrations as applied in the tracking table without actually running the SQL. It also works with `--rollback`.

## 7. Production Workflow (Best Practices)

To ensure the stability and reliability of your production database, always follow this workflow:

1.  **Generate in Dev**: Run `asok make migration` on your development machine.
2.  **Ship in Build**: Run `asok build` to include these migrations in your distribution.
3.  **Apply in Prod**: Run `asok migrate` on your production server.

> **Do not run `asok make migration` in production.** Your distribution should be considered immutable; migrations should be authored in development and deployed as part of your release.

> Always review generated migration files before applying them, especially in production environments.

---
[← Previous: Advanced ORM Features](08-advanced-orm.md) | [Documentation](README.md) | [Next: Native Vector Search →](10-vector-search.md)
