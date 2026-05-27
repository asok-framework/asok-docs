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

---
[← Previous: ORM Basics](07-orm.md) | [Documentation](README.md) | [Next: Database Migrations →](09-migrations.md)

