# Advanced ORM Features

Asok's ORM is designed to be powerful yet lightweight. This guide covers advanced field types and query patterns added for professional applications.

## 1. Advanced Field Types

### JSON Field
Store complex data structures (dicts, lists) transparently.
```python
from asok import Model, Field

class Settings(Model):
    config = Field.JSON(default={})

# Usage
s = Settings.create(config={"theme": "dark", "notifications": True})
print(s.config["theme"]) # "dark" (automatically a dict)
```

### Enum Field
Integrate with Python's standard `enum.Enum` for type-safe choices.
```python
import enum
from asok import Model, Field

class Status(enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"

class User(Model):
    status = Field.Enum(Status, default=Status.PENDING)
```

### Decimal Field
Precise math for financial data (money).
```python
from decimal import Decimal
from asok import Model, Field

class Product(Model):
    price = Field.Decimal(precision=2)

p = Product.create(price=Decimal("19.99"))
```

### UUID Field
Automatically generate unique identifiers.
```python
from asok import Model, Field

class Job(Model):
    uid = Field.UUID() # Auto-generates uuid4 on save
```

### Tel / Phone Field
Store validated phone numbers.
```python
from asok import Model, Field

class User(Model):
    phone = Field.Tel(unique=True)
```

### Rich Text (WYSIWYG)
Upgrade standard textareas to a full-featured editor in the admin panel.
```python
from asok import Model, Field

class Post(Model):
    body = Field.Text(wysiwyg=True) # Enables Quill editor in Admin
```

---

## 2. Advanced Querying

### OR Conditions
```python
User.query().where("status", "active").or_where("is_admin", True).get()
```

### Range & NULL Checks
```python
# Between
Product.query().where_between("price", 10, 50).get()

# NULL checks
User.query().where_null("deleted_at").get()
User.query().where_not_null("email_verified_at").get()
```

### Sorting Shorthands
```python
latest_users = User.query().latest().limit(5).get()
oldest_tasks = Task.query().oldest().get()
```

### Database Indexes
Optimize query performance by adding indexes to frequently filtered columns.

```python
from asok import Model, Field

class User(Model):
    email = Field.String(unique=True)      # Automatic UNIQUE index
    username = Field.String(index=True)    # Regular index for fast lookups
    created_at = Field.DateTime(index=True) # Index for sorting/filtering
    status = Field.String(index=True)      # Index for WHERE clauses
```

**When to use indexes:**
- Columns frequently used in `WHERE` clauses
- Columns used for sorting (`ORDER BY`)
- Foreign keys (for JOIN performance)
- Columns used in `GROUP BY`

**Note:** `unique=True` fields automatically get a UNIQUE index, so don't add `index=True` on them.

### Union Queries
Combine results from multiple queries using SQL UNION (removes duplicates).

```python
from asok import Model, Field

class User(Model):
    role = Field.String(index=True)
    active = Field.Boolean()

# Get all admins OR moderators
admins = User.query().where('role', 'admin')
moderators = User.query().where('role', 'moderator')
staff = admins.union(moderators).get()

# With additional filters and ordering
top_staff = (
    User.query().where('role', 'admin')
    .union(User.query().where('role', 'editor'))
    .order_by('name')
    .limit(10)
    .get()
)
```

**SQL Generated:**
```sql
(SELECT * FROM users WHERE role = ?)
UNION
(SELECT * FROM users WHERE role = ?)
ORDER BY name
LIMIT 10
```

### Intersect Queries
Get only results that appear in both queries using SQL INTERSECT.

```python
# Find users who are BOTH active AND premium
active_users = User.query().where('active', 1)
premium_users = User.query().where('premium', 1)
active_premium = active_users.intersect(premium_users).get()

# SQL: (SELECT * FROM users WHERE active = ?)
#      INTERSECT
#      (SELECT * FROM users WHERE premium = ?)
```

### Subqueries
Use a query as a value in `WHERE IN` clauses for powerful filtering.

```python
from asok import Model, Field

class Post(Model):
    title = Field.String()
    user_id = Field.ForeignKey('User')
    published = Field.Boolean()

# Find all users who have at least one published post
user_ids_with_posts = Post.query().where('published', 1).select('user_id')
authors = User.query().where_in('id', user_ids_with_posts).get()

# SQL: SELECT * FROM users
#      WHERE id IN (SELECT user_id FROM posts WHERE published = ?)
```

**Advanced subquery example:**
```python
# Users who have more than 5 published posts
prolific_author_ids = (
    Post.query()
    .where('published', 1)
    .select('user_id')
    .group_by('user_id')
    # Note: HAVING would need to be added for count > 5
)
authors = User.query().where_in('id', prolific_author_ids).get()
```

**Combining techniques:**
```python
# Premium users OR users with published posts
premium = User.query().where('premium', 1)
authors_ids = Post.query().where('published', 1).select('user_id')
authors = User.query().where_in('id', authors_ids)
valued_users = premium.union(authors).order_by('created_at').get()
```

## 3. Native Vector Search (Semantic)

Asok supports storing and searching high-dimensional vectors (embeddings) directly in SQLite using specialized binary storage and custom similarity functions.

### Defining a Vector Field
Specify the dimensions of your embedding (e.g., 1536 for OpenAI, 384 for standard local models).
```python
from asok import Model, Field

class Document(Model):
    content = Field.String()
    embedding = Field.Vector(dimensions=1536)
```

### Proximity Searching
Use `.nearest()` to find rows most similar to a query vector.
```python
query_vec = [0.1, 0.5, ...] # List of floats
docs = Document.query().nearest("embedding", query_vec, metric="cosine", limit=5).get()
```
*Metrics supported: `cosine` (default) and `euclidean`.*

### Admin Integration
You can enable semantic search in the Admin search bar!
1. Add `vector_search_field` to your `Admin` class.
2. Define an `embed_query` method on your model to convert search text into a vector.

```python
from asok import Model, Field

class Product(Model):
    name = Field.String()
    vec = Field.Vector(1536)

    @classmethod
    def embed_query(cls, text):
        # Call OpenAI / Mistral / Local model here
        return [0.1, 0.2, ...] 

    class Admin:
        search_fields = ["name"]
        vector_search_field = "vec"
```

---

## 4. High-Performance Model Methods

### Atomic Increments/Decrements
Safely update counters directly in SQL to avoid race conditions.
```python
post = Post.find(1)
post.increment("views")  # SQL: UPDATE posts SET views = views + 1 ...
```

### Reloading Data
```python
post.refresh() # Reloads attributes from the database
```

### API Error Handling
Perfect for REST controllers:
```python
from asok import Request, ModelError

def get(request: Request):
    try:
        user = User.find_or_fail(request.params["id"])
        return request.api(user.to_dict())
    except ModelError:
        return request.api_error("User not found", status=404)
```

## 5. Nested Eager Loading

Optimize your database queries and avoid $N+1$ problems by eager-loading deeply nested relationships using dot notation:

```python
# Fetches all companies, their departments, and all employees in those departments in only 3 queries
companies = Company.query().with_("departments.employees").get()

for company in companies:
    print(f"Company: {company.name}")
    for dept in company.departments:
        print(f"  Department: {dept.name}")
        for emp in dept.employees:
            print(f"    Employee: {emp.name}")
```

## 6. Polymorphic Relationships

Polymorphic relationships allow a model to belong to more than one other model on a single association.

### MorphTo

Define a `MorphTo` relationship on the child model. The database table requires a string column to store the parent model type (e.g. `commentable_type`) and an integer column to store the parent ID (e.g. `commentable_id`).

```python
from asok import Model, Field, Relation

class Comment(Model):
    body = Field.Text()
    commentable_id = Field.Integer()
    commentable_type = Field.String()

    commentable = Relation.MorphTo()
```

### MorphMany

Define a `MorphMany` relationship on any parent model, specifying the target model name and the name of the relation definition on the target.

```python
class Article(Model):
    title = Field.String()
    comments = Relation.MorphMany("Comment", "commentable")

class Video(Model):
    title = Field.String()
    comments = Relation.MorphMany("Comment", "commentable")
```

### Querying and Eager Loading Polymorphic Relations

Asok supports dynamic and polymorphic eager loading to retrieve relationships in batches:

```python
# Eager load comments and their polymorphic commentables
comments = Comment.query().with_("commentable").get()
for c in comments:
    # Resolves dynamically to either Article or Video instance
    parent = c.commentable 
    print(f"Comment '{c.body}' on {parent.__class__.__name__}: {getattr(parent, 'title', '')}")
```

## 7. Generic Global Scopes

Global scopes allow you to add query constraints automatically to all queries for a given model.

### Defining a Global Scope

Specify global scopes using a `_global_scopes` dictionary mapping names to lambda query builders:

```python
class Product(Model):
    name = Field.String()
    active = Field.Integer(default=1)

    _global_scopes = {
        "active_only": lambda q: q.where("active", 1)
    }

# This automatically filters products where active = 1
active_products = Product.query().get()
```

### Removing Global Scopes

Disable specific or all global scopes when making queries:

```python
# Bypasses the active_only scope to return all products
all_products = Product.query().without_global_scope("active_only").get()

# Bypasses all active global scopes
all_products = Product.query().without_global_scopes().get()
```

### Soft Deletes

A soft delete column automatically adds a built-in `soft_delete` global scope. Use `.with_trashed()` to query soft-deleted records:

```python
class User(Model):
    name = Field.String()
    deleted_at = Field.SoftDelete() # Adds implicit soft_delete scope

# Find only non-deleted users
users = User.query().get()

# Find all users, including soft-deleted ones
all_users = User.query().with_trashed().get()
```

## 8. Savepoint-Based Nested Transactions

Asok supports nested transactions using SQL savepoints. A nested transaction block will register a savepoint, allowing you to rollback or commit child operations independently of the outer transaction:

```python
with Company.transaction():
    Company.create(name="MainCorp")

    try:
        with Company.transaction(): # Uses SAVEPOINT internally
            Company.create(name="SubCorp")
            raise ValueError("Rollback sub-operation")
    except ValueError:
        # Reverts only the creation of "SubCorp"
        pass

    Company.create(name="AnotherCorp")
# Commits "MainCorp" and "AnotherCorp", but not "SubCorp"
```

## 9. PostgreSQL Connection Pooling

For PostgreSQL environments, Asok dynamically integrates connection pooling using `psycopg_pool`. If a connection pool is initialized, database handles are transparently checked out and returned to the pool, optimizing concurrent request handling:

```python
# Configuration in .env
DATABASE_URL=postgresql://user:pass@localhost/db?min_size=5&max_size=20
```

## 10. Database Fixtures (Backup & Restore)

Asok provides fixture commands to serialize and deserialize model data to and from JSON formats. This is extremely useful for database backups, data migrations, and test seeding.

### Exporting Data (`dumpdata`)

Dump database records into a structured JSON fixture:

```bash
# Dump all registered models to output file
asok dumpdata --output=fixtures.json

# Dump a specific model only
asok dumpdata User --output=users.json
```

Binary `bytes` fields are base64-encoded automatically as `"base64:<data>"`.

### Importing Data (`loaddata`)

Load data from a JSON fixture file back into the database:

```bash
asok loaddata fixtures.json
```

* **Updates & Inserts:** `loaddata` checks the database for existing records by matching primary keys. Existing records are updated via ORM `.save()`. Missing records are inserted directly via raw SQL queries to preserve original primary key IDs.
* **Transactions:** The entire import is executed inside an atomic transaction.

## 11. Transparent Multi-Language Support

Asok models automatically support database-backed multi-language fields. When you define language-specific columns using standard suffix notation (e.g., `_fr`, `_en`, `_es`), the ORM dynamically exposes base properties (e.g., `title` and `content`) that automatically route accesses to the active request's language, with smart fallbacks.

### Two Modeling Styles Supported

#### Style A: Base Field + Translation Fields
The base field represents the default language configured in the application (via `app.config['LOCALE']`, which defaults to `'en'`).
```python
class Post(Model):
    title = Field.String()      # Stores English (default language)
    title_fr = Field.String()   # Translation for French
    title_es = Field.String()   # Translation for Spanish
```

#### Style B: Suffixed Fields Only
All translation fields use explicit language suffixes.
```python
class Post(Model):
    title_en = Field.String()   # English
    title_fr = Field.String()   # French
    title_es = Field.String()   # Spanish
```

### Usage
Whether using Style A or Style B, you can access or update the active translation transparently:

```python
post = Post(title="Hello English", title_fr="Bonjour Français")

# 1. Reading values (resolves automatically using current_request.lang)
print(post.title)  # "Hello English" (under English request context)
print(post.title)  # "Bonjour Français" (under French request context)

# 2. Writing values
post.title = "Hi English"  # Updates base column 'title' under English context
post.title = "Salut"       # Updates 'title_fr' under French context
```

### Cascade Fallback Order
If the translation for the active request's language is empty or not defined, the getter falls back in this order:
1. Active request language column (e.g., `title_fr`).
2. Default application locale (configured via `app.config['LOCALE']`, default is `'en'`).
3. English (`'en'`), then French (`'fr'`) column.
4. Any first populated translation column found.
5. The base column value (`title`).

### Bypassing During DB Loading
When models are populated from database query results, all setters are bypassed to load the database columns exactly as they are without side-effects.

---

## 12. Multiple Database Connections

Asok's ORM natively supports connecting different models to different database engines. Rather than needing a global registry or routing rules, you simply specify the database target directly on the model class.

### 1. Model-Level Database Paths

By default, all models share the main application database (`DATABASE_URL`). To bind a model (or a subset of models) to a separate database, override the class-level `_db_path` attribute:

```python
from asok import Model, Field

# Uses default DATABASE_URL from .env
class User(Model):
    __tablename__ = "users"
    name = Field.String()

# Uses a separate SQLite database file for logs
class SystemLog(Model):
    __tablename__ = "system_logs"
    _db_path = "sqlite:///logs.db"
    
    message = Field.Text()
```

When you query or save instances of `SystemLog`, the ORM automatically routes all SQL operations to the `logs.db` connection.

### 2. Environment Variable Resolution

To avoid committing sensitive credentials (passwords, hosts) or hardcoding paths directly in your source code, you can set `_db_path` to the **name** of an environment variable. The framework will automatically resolve its value at runtime:

**Fichier `.env`**:
```env
DATABASE_URL=sqlite:///db.sqlite3
LOGS_DATABASE_URL=postgresql://user:pass@localhost:5432/logs_db
```

**Modèles Python**:
```python
from asok import Model, Field

class SystemLog(Model):
    __tablename__ = "system_logs"
    
    # Asok automatically detects that "LOGS_DATABASE_URL" is an env variable
    # and resolves its value securely from the environment.
    _db_path = "LOGS_DATABASE_URL"
    
    message = Field.Text()
```

---

### 3. Read Replicas (Read/Write Splitting)

Asok supports separating read and write traffic by routing writes to a primary database and reads to a pool of read replicas.

**Configuration in `.env`**:
```env
DATABASE_URL=postgresql://primary-db-host/prod_db
DATABASE_REPLICAS=postgresql://replica-1-host/prod_db,postgresql://replica-2-host/prod_db
DATABASE_LOAD_BALANCING_STRATEGY=round-robin
```

* **Read replicas**: Set `DATABASE_REPLICAS` to a comma-separated list of DSN connection URLs.
* **Load Balancing**: Set `DATABASE_LOAD_BALANCING_STRATEGY` to either `round-robin` (default) or `random` to specify how read traffic is distributed across replicas.
* **Transaction Pinning**: When inside an active transaction (e.g., `with Model.transaction():`), all read queries are automatically pinned to the primary database to ensure consistency and prevent replication lag issues.

---

### 4. Database Sharding

Database sharding distributes your data across multiple distinct databases (shards). Asok provides both configuration and programmatic API targeting for shards.

**Configuration in `.env`**:
```env
# Define shards as a JSON string mapping shard name to connection URL and replicas
DATABASE_SHARDS='{"shard1": {"url": "sqlite:///shard1.db", "replicas": ["sqlite:///shard1_replica.db"]}, "shard2": "sqlite:///shard2.db"}'
```

Alternatively, you can configure shards using prefix-based environment variables:
```env
DATABASE_SHARD_SHARD1_URL=sqlite:///shard1.db
DATABASE_SHARD_SHARD1_REPLICAS=sqlite:///shard1_replica.db
```

**Targeting Shards in Code**:
Use the `.on(shard_name)` builder method on models or queries to target a specific shard:

```python
# Create an object on a specific shard
user = User.on("shard1").create(name="Alice", email="alice@example.com")

# Query records on a specific shard
users = User.on("shard1").where("active", 1).get()

# Save/Update/Delete operations preserve the shard on the model instance
user.name = "Alice Updated"
user.save()  # Automatically routes to shard1
```

**Relation Shard Propagation**:
When accessing relationship properties on a model instance targeted to a shard, Asok automatically routes the relation queries to the same shard:

```python
user = User.on("shard1").find(id=1)

# Fetches posts from shard1 automatically!
user_posts = user.posts
```

---
[← Previous: ORM Basics](07-orm.md) | [Documentation](README.md) | [Next: Database Migrations →](09-migrations.md)


