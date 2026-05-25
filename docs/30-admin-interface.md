# Admin Interface

A Django-style admin interface, auto-generated from your models. Zero config to start, deeply customizable when you need it.

## Quick Start

Scaffold a project with admin enabled:

```bash
asok create myapp --admin
cd myapp
asok createsuperuser
asok dev
```

Open http://127.0.0.1:8000/admin and log in.

The `--admin` flag generates a `User` model with an `is_admin` field and registers `Admin(app)` in `wsgi.py`.

## Adding to an existing project

If you decided to add the Admin interface after your project was created, run:

```bash
asok admin --enable
```

This command will:
1. Update `wsgi.py` to register the `Admin` extension.
2. Create `src/models/user.py` with the default `User` model if it doesn't exist.
3. Guide you through the necessary migrations and superuser creation.

### Customization

```python
Admin(app, site_name="codewithmpia", url_prefix="/gestion", favicon="images/logo.svg")
```

| Param | Default | Description |
|---|---|---|
| `site_name` | `"Asok Admin"` | Brand shown in sidebar / page title |
| `url_prefix` | `"/admin"` | URL prefix for all admin routes |
| `favicon` | `None` | Path to your brand logo / tab icon |

#### Smart Asset Resolution

The `favicon` path resolves intelligently based on its location:
- **Internal Assets**: If you use a simple filename like `logo.svg`, the admin uses its built-in internal version.
- **Project Assets**: If you provide a directory path (e.g. `images/logo.svg` or `uploads/brand.png`), the admin resolves it relative to your project's `src/partials/` folder.

This logo is automatically applied as the browser favicon, the sidebar brand icon, and the login page header.

## Authentication

Admin uses `request.login()` and requires the user to have `is_admin = True` **or at least one assigned Role**. Add the field to your `User` model:

```python
from asok import Model, Field

class User(Model):
    email = Field.String()
    password = Field.Password()
    is_admin = Field.Boolean(default=False)
```

Create the first superuser:

```bash
asok createsuperuser
# or non-interactive:
asok createsuperuser --email=admin@example.com --password=secret
```

### Access rules

| User state | Can log in to admin? |
|---|---|
| `is_admin = True` | ✅ Yes — full access, bypasses all permission checks |
| Has at least one Role | ✅ Yes — filtered access based on role permissions |
| No roles and `is_admin = False` | ❌ No — redirected to login with **"Invalid credentials"** |

> **Security note**: A user without any role receives the same `"Invalid credentials"` message as a wrong password, even if their credentials are correct. This prevents information leakage about account status.

> **Session Security**: By default, an admin session lasts for **30 days**. If you want your administrators to re-authenticate more frequently, change the `SESSION_MAX_AGE` value (in seconds) in your `.env` file.

## Roles & Permissions

Asok Admin ships with a granular role-based access control (RBAC) system. Two models are auto-provisioned when you call `Admin(app)`:

- **User** — the auth model (`email`, `password`, `name`, `is_admin`, `totp_enabled`, `created_at`)
- **Role** — grants permissions to users (`name`, `label`, `permissions`, `created_at`)

Linked by a `role_user` pivot table (a user can have any number of roles).

### Permission format

Permissions are comma-separated strings following `<slug>.<verb>`:

- `posts.view`, `posts.edit`, `users.delete`, `assets.export`
- `posts.*` — all verbs on `posts`
- `*` — superuser (bypass all checks)

The available verbs are: `view`, `add`, `edit`, `delete`, `export`.

### Permission Hierarchy (Why "view" is obligatory)

**IMPORTANT**: The `view` permission is **required** for all other permissions on a model. This is a security-by-design principle that ensures users cannot perform actions on resources they shouldn't see.

#### Why this matters

Think of permissions as building blocks:

```
view ─┬─ add
      ├─ edit
      ├─ delete
      └─ export
```

Without `view` permission, the other permissions make no logical sense:
- How can you **edit** something you cannot see?
- How can you **delete** something you cannot view?
- How can you **add** to a collection you don't have access to view?
- How can you **export** data you shouldn't be able to see?

#### Automatic enforcement

The admin interface **automatically enforces** this hierarchy in two ways:

1. **Frontend**: When you check a permission (add/edit/delete/export) in the permissions matrix, the `view` permission is automatically checked if it wasn't already.

2. **Backend**: When saving a role, the system validates that all permissions have `view` included. If you somehow bypass the frontend (via API or direct database manipulation), `view` is automatically added.

This is an admin UI guarantee; if you add your own permission checks in custom routes, enforce the same rule there too.

Example:
```python
# If you save a role with these permissions:
role.permissions = "posts.edit,posts.delete"

# The system automatically converts it to:
role.permissions = "posts.view,posts.edit,posts.delete"
```

This prevents security holes where a user might have edit/delete rights but no visibility into the resource.

### View Templates (List, Detail, Edit)

The admin interface provides three distinct views for each model:

1. **List View** (`/admin/<slug>`) — Browse all items with filters, search, pagination
2. **Detail View** (`/admin/<slug>/<id>/view`) — Read-only detailed view of a single item
3. **Edit View** (`/admin/<slug>/<id>`) — Form to create or update an item

#### Permission-based navigation

The available actions depend on the user's permissions:

| Permission | Can access | Sees buttons |
|---|---|---|
| `view` only | List + Detail | View |
| `view` + `edit` | List + Detail + Edit | View, Edit |
| `view` + `delete` | List + Detail | View, Delete |
| `view` + `edit` + `delete` | List + Detail + Edit | View, Edit, Delete |

**Security**: If a user has only `view` permission and tries to access the edit URL directly, they are redirected to the detail view. All buttons are conditionally rendered based on actual permissions.

### Granting access

1. Log in as a superuser (`is_admin = True`) or an existing admin.
2. Go to **Roles** → **New**.
3. Give it a `name` (e.g. `editor`) and a `label` (e.g. `Content Editor`).
4. Tick boxes in the **Permissions** matrix (models × verbs). The "all" column ticks a whole row; the **Superuser** checkbox at the top grants `*`.
5. **Note**: When you check any permission, `view` is automatically checked if it wasn't already.
6. Save.
7. Go to **Users**, edit the target user, tick the role in the **Roles** section. Save.

The user now sees only the models they have `view` permission on. Each action (add / edit / delete / export) is gated by its corresponding verb.

### Common Role Examples

#### Read-only Viewer
Perfect for clients, stakeholders, or auditors who need to see data but not modify it.

```
Role: Viewer
Permissions:
  - posts.view
  - users.view
  - categories.view
```

Users with this role can:
- Browse list views
- View details of individual items
- Cannot create, edit, or delete anything

#### Content Editor
Typical role for content managers who can create and edit content but not delete or manage users.

```
Role: Content Editor
Permissions:
  - posts.view, posts.add, posts.edit
  - categories.view, categories.add, categories.edit
  - assets.view, assets.add (for media uploads)
```

Users with this role can:
- Create and edit posts and categories
- Upload media files
- Cannot delete posts or manage users

#### Moderator
Mid-level role with delete capabilities on specific models.

```
Role: Moderator
Permissions:
  - posts.view, posts.add, posts.edit, posts.delete
  - comments.view, comments.delete
  - users.view
```

Users with this role can:
- Full CRUD on posts
- View and delete comments (moderation)
- View users but not modify them

#### Data Analyst
Role focused on viewing and exporting data for analysis.

```
Role: Data Analyst
Permissions:
  - posts.view, posts.export
  - users.view, users.export
  - orders.view, orders.export
```

Users with this role can:
- View all data across multiple models
- Export data to CSV for analysis
- Cannot modify or delete anything

### Behaviour summary

| User state | Access |
|---|---|
| `is_admin = True` | Full access, bypass all permission checks |
| Has roles with perms | Filtered access based on permissions |
| No roles, `is_admin = False` | Redirected to `/admin/login` with "Invalid credentials" message |

### `user.can(perm)`

The `User.can()` helper is also available in your own code:

```python
if request.user.can("posts.edit"):
    ...
```

Supports exact match, `<slug>.*` wildcards, and `*` superuser.

### Permission-based button visibility

All action buttons in the admin interface are conditionally displayed based on permissions:

**List view buttons:**
- **New** — shown only if user has `add` permission
- **Import** — shown only if user has `add` permission
- **Export** — shown only if user has `export` permission
- **Trash** — shown only if user has `delete` permission

**Row action buttons:**
- **View** (eye icon) — shown if user has `view` permission
- **Edit** (pencil icon) — shown if user has `edit` permission
- **Delete** (trash icon) — shown if user has `delete` permission

**Detail/Edit view buttons:**
- **Edit** — shown if user has `edit` permission
- **Delete** — shown if user has `delete` permission
- **History** — shown **only to admins** (`is_admin = True`), regardless of permissions

This ensures users only see actions they can actually perform, preventing confusion and improving security.

### Audit Logs

All changes made via the admin interface are automatically tracked in the `AdminLog` model. This provides a full history of:
- Who made the change
- When it was made
- What fields were changed (with a diff of old vs new values)

You can view the history of any item by clicking the **History** button on its edit page.

**Security Note**: The History button is only visible to super-admins (`is_admin = True`), regardless of role permissions. This prevents regular users from accessing audit logs, which may contain sensitive information about system changes.

### Common Scenarios & Troubleshooting

#### Scenario 1: User can't see a model in the sidebar

**Cause**: The user lacks the `view` permission for that model.

**Solution**: Grant the role a permission with at least `<model>.view`:
```
# In the Role permissions:
posts.view  # Now the user sees "Posts" in the sidebar
```

#### Scenario 2: User sees the list but can't click "Edit"

**Cause**: The user has `view` permission but not `edit`.

**Solution**: Either:
- Add `edit` permission if the user should be able to edit
- This is working as intended if the user should only view data

```
# Read-only (current state):
posts.view

# Add edit capability:
posts.view, posts.edit
```

#### Scenario 3: User can edit but gets 403 when trying to delete

**Cause**: The user has `edit` permission but not `delete`.

**Solution**: Add the `delete` permission:
```
# Before:
posts.view, posts.edit

# After:
posts.view, posts.edit, posts.delete
```

#### Scenario 4: Trying to give "delete" without "view" fails

**Cause**: The system enforces permission hierarchy — you cannot delete what you cannot see.

**Solution**: This is working as designed. The admin will automatically add `view` when you save:
```
# What you try to save:
posts.delete

# What actually gets saved:
posts.view, posts.delete
```

#### Scenario 5: User gets a blank page instead of a 403 error

**Cause**: This was a bug in earlier versions where SPA navigation didn't properly render error pages.

**Solution**: Update to the latest version. Error pages now correctly display with full design when permission is denied.

#### Scenario 6: Import/Export buttons visible despite no permissions

**Cause**: This was a security gap in earlier versions.

**Solution**: Update to the latest version. These buttons now correctly check for `add` (Import) and `export` (Export) permissions.

#### Scenario 7: Regular user can see "History" button

**Cause**: This was a security oversight in earlier versions.

**Solution**: Update to the latest version. The History button is now restricted to `is_admin = True` users only.

#### Scenario 8: Need to give a user temporary admin access

**Best Practice**: Instead of setting `is_admin = True`, create a comprehensive role:
```
Role: Temporary Admin
Permissions: *  # Superuser wildcard
```

Then assign this role to the user. When the temporary period ends, simply remove the role assignment. This maintains audit trail integrity.

#### Scenario 9: User should manage content but not see user accounts

**Solution**: Grant permissions selectively:
```
Role: Content Manager
Permissions:
  - posts.view, posts.add, posts.edit, posts.delete, posts.export
  - categories.view, categories.add, categories.edit, categories.delete
  - assets.view, assets.add
  # Notice: no "users" permissions at all
```

The user will not see "Users" in the sidebar at all.

#### Scenario 10: Multiple roles with conflicting permissions

**Behavior**: Permissions are **additive**. If a user has multiple roles, they get the **union** of all permissions.

Example:
```
Role A: posts.view
Role B: posts.edit

User with both roles can: view AND edit posts
```

This means you can build granular roles and combine them:
```
Base Role: Dashboard Access
  - posts.view
  - users.view

Editor Add-on: Editing Rights
  - posts.edit
  - categories.edit

Assign both roles → User can view + edit
```

### RBAC Best Practices

#### 1. Principle of Least Privilege

Always grant the minimum permissions necessary for a user to perform their job:

❌ **Bad**:
```
# Giving admin access when they only need to edit posts
Role: Editor
Permissions: *
```

✅ **Good**:
```
# Specific permissions for specific tasks
Role: Editor
Permissions: posts.view, posts.add, posts.edit
```

#### 2. Use Role Composition

Instead of creating one massive role, create small focused roles and combine them:

❌ **Bad**:
```
Role: Marketing Manager
Permissions: posts.*, categories.*, tags.*, assets.*, users.view, analytics.*
```

✅ **Good**:
```
Role: Content Publisher
Permissions: posts.*, categories.*, tags.*

Role: Media Manager
Permissions: assets.*

Role: Team Viewer
Permissions: users.view

# Assign all three roles to the marketing manager
```

Benefits:
- Easier to maintain
- More flexible reassignment
- Clear separation of concerns

#### 3. Separate View-only from Write Access

Create distinct roles for viewing vs modifying:

```
Role: Viewer
Permissions: posts.view, users.view, orders.view

Role: Editor
Permissions: posts.view, posts.add, posts.edit

Role: Publisher
Permissions: posts.view, posts.edit, posts.delete
```

This makes it easy to give temporary access or onboard new team members safely.

#### 4. Document Your Roles

Add clear labels and internal documentation:

```python
Role:
  name: content_editor
  label: Content Editor - Can create and edit posts and pages
  permissions: posts.view, posts.add, posts.edit, pages.view, pages.add, pages.edit
```

The `label` field is user-facing, so make it descriptive.

#### 5. Regular Permission Audits

Periodically review:
- Which users have which roles
- Whether users still need their assigned permissions
- Remove roles from users who changed positions

Check the **History** feature (admin-only) to see who made what changes.

#### 6. Use Superuser Sparingly

The `*` (superuser) permission bypasses all checks. Reserve it for:
- System administrators
- Emergency break-glass accounts
- Automated backup/maintenance scripts

For regular power users, explicitly grant broad permissions instead:

❌ **Bad**:
```
Role: Senior Manager
Permissions: *
```

✅ **Good**:
```
Role: Senior Manager
Permissions: posts.*, users.view, users.edit, categories.*, tags.*, assets.*
# Still powerful, but doesn't bypass security checks
```

#### 7. Test Permissions Before Deploying

Before giving a role to real users:
1. Create a test user
2. Assign the role
3. Log in as that test user (or use **Impersonation**)
4. Verify they can do what they need and **nothing more**

This prevents security gaps and user frustration.

#### 8. Consider Data Export Carefully

The `export` permission grants CSV downloads of potentially sensitive data:

```
# Allow export for data analysts
Role: Analyst
Permissions: posts.view, posts.export, users.view, users.export

# But maybe NOT for regular editors
Role: Editor
Permissions: posts.view, posts.add, posts.edit
# Notice: no .export
```

#### 9. One Admin, Many Roles

Instead of making everyone an admin (`is_admin = True`), use roles:

```
Admin Users (is_admin = True):
  - Your account
  - One backup account
  - That's it!

Power Users (roles only):
  - Content Manager → posts.*, categories.*, assets.*
  - User Manager → users.view, users.edit
  - Moderator → posts.view, posts.delete, comments.*
```

This maintains better audit trails and allows granular permission management.

#### 10. Protect Critical Models

For sensitive models (users, payments, settings), create separate dedicated roles:

```
Role: User Administrator
Permissions: users.view, users.edit
# Notice: no users.delete

Role: User Moderator
Permissions: users.view, users.add, users.edit, users.delete
# Full access, but tracked in audit logs
```

Then assign these roles very selectively.

### Quick Reference: Permission Verbs

| Verb | What it controls | Frontend visibility | Backend check |
|------|-----------------|---------------------|---------------|
| `view` | Access to list and detail views | Model appears in sidebar, View button in list | Required for all other verbs |
| `add` | Create new items | "New" button, "Import" button | `/admin/<slug>/new` route |
| `edit` | Modify existing items | "Edit" button in list and detail | `/admin/<slug>/<id>` POST route |
| `delete` | Remove items (soft or permanent) | "Delete" button, "Trash" menu | `/admin/<slug>/<id>/delete` route |
| `export` | Download data as CSV | "Export" button in list view | `/admin/<slug>/export` route |

**Remember**: All verbs require `view` as a prerequisite. The system enforces this automatically.

### Quick Reference: Special Permissions

| Permission | Description |
|-----------|-------------|
| `*` | Superuser — bypass all permission checks (use sparingly) |
| `<slug>.*` | All verbs on a specific model (e.g., `posts.*`) |
| `assets.view` | Access the Media Manager |
| `assets.add` | Upload files in Media Manager |
| `assets.delete` | Delete files in Media Manager |

### Permission Matrix Example

Here's what a typical organization might look like:

| Role | posts | users | categories | assets | orders |
|------|-------|-------|-----------|--------|--------|
| **Viewer** | view | view | view | view | view |
| **Editor** | view, add, edit | - | view, add, edit | view, add | - |
| **Moderator** | view, add, edit, delete | view | view, add, edit, delete | view, add | view |
| **Admin** | * | * | * | * | * |
| **Analyst** | view, export | view, export | view | - | view, export |

`-` means no permissions (model not visible to that role)

## Two-Factor Authentication (2FA)

Asok Admin supports TOTP-based 2FA (Google Authenticator, Authy, etc.).

### Enabling 2FA
1. Click your profile in the topbar and go to **My Profile**.
2. Click **Enable 2FA**.
3. Scan the QR code with your authenticator app.
4. Enter the 6-digit verification code to confirm.

Once enabled, every login will require a 6-digit code after the password verification.

### Disabling 2FA
You can disable 2FA from your profile page. This requires confirming your current password for security.

## Impersonation

Super-admins (`is_admin = True`) can "act as" any other user to troubleshoot issues or verify permissions.

1. Go to the **Users** list.
2. Click the **Impersonate** button (user icon) on the target user's row.
3. You are now acting as that user. A banner will appear at the top of the admin interface.

### Security
- Only real admins with `is_admin = True` can start impersonation.
- The admin's own session is **preserved** — impersonation does not log you out. You are returned to your account when you stop.
- Impersonation sessions automatically **expire after 1 hour**. When they expire, the session silently reverts to the real admin account.
- The admin's identity is **re-verified on every request** during impersonation. If the admin loses their `is_admin` flag, the session is immediately revoked.
- All actions performed while impersonating are logged under the target user's ID in the audit logs.
- Click **Stop Impersonation** in the banner to return to your admin account at any time.
- You cannot impersonate yourself.

### Translated messages

All impersonation flash messages respect the admin's configured language (English, French, Spanish):

| Event | EN | FR | ES |
|-------|----|----|----|
| Session started | Now acting as {name} | Vous agissez maintenant en tant que {name} | Ahora actuando como {name} |
| Session stopped | Stopped impersonation | Impersonnalisation arrêtée | Suplantación detenida |
| Session expired | Impersonation expired (1 h max.) | Impersonnalisation expirée (1 h max.) | Suplantación expirada (1 h máx.) |
| Unauthorized attempt | Unauthorized impersonation. | Impersonnalisation non autorisée. | Suplantación no autorizada. |

## Media Manager

The Media Manager allows you to manage files uploaded to `src/partials/uploads/`.

### Permissions
Access to the Media Manager is controlled by the `assets` slug:
- `assets.view`: Access the media manager list.
- `assets.add`: Upload new files.
- `assets.delete`: Delete existing files.

### Organization
Files are automatically grouped into subdirectories based on their type:
- **images/**: `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.svg`
- **pdfs/**: `.pdf`
- **others/**: All other file types

### Usage
You can upload multiple files at once using drag & drop or the file picker. Images feature a live preview and one-click copy of their public URL.

## Global Search

The admin interface features a powerful global search (accessible via `Cmd+K` or the search icon in the sidebar).

- **Multi-model**: Searches across all registered models simultaneously.
- **Permission-aware**: Only shows results from models the user has `view` permission on.
- **Customizable**: Control which fields are searchable for each model using `search_fields`.

## Dashboard Widgets

You can extend the dashboard with custom widgets to show stats, charts, or quick actions.

```python
from asok.admin import Admin
from asok.utils.html import SafeString

admin = Admin(app)

@admin.widget("Recent Sales", size="medium")
def recent_sales(request):
    sales = Sale.query().order_by("-id").limit(5).get()
    html = "<ul>"
    for s in sales:
        html += f"<li>{s.amount}€ - {s.created_at}</li>"
    html += "</ul>"
    return html

# Or return a dict for more control
@admin.widget("System Status", size="small")
def system_status(request):
    return {
        "html": '<div class="text-success">All systems operational</div>',
        "footer": '<a href="/admin/logs">View logs</a>'
    }
```

### Widget Options
- **title**: The display title.
- **size**: `small`, `medium`, or `large`.
- **permission**: Optional `slug.verb` string. The widget will be hidden if the user lacks this permission.

## Tailwind CSS customization of model fields

Admin form fields defined via `Field.*` accept extra keyword arguments that are forwarded to the generated widget. Use the `element__attribute` convention to target nested sub-elements.

### Dropdown (`Field.Dropdown`)

```python
from asok import Model, Field

class Project(Model):
    status = Field.Dropdown(
        choices=[("active", "Active"), ("archived", "Archived")],
        option__class="text-indigo-600 font-medium",  # Styles each option
        menu__class="shadow-2xl rounded-xl border-none",  # Styles the dropdown menu
        trigger__class="btn-primary",                    # Styles the trigger button
    )
```

### Boolean as Toggle Switch (`Field.Boolean` with `form_type="toggle"`)

By default, `Field.Boolean()` renders as a **checkbox**. Use `form_type="toggle"` to render a **sliding switch** instead:

```python
class Project(Model):
    is_public = Field.Boolean(
        form_type="toggle",              # Renders as a switch, not a checkbox
        slider__class="bg-indigo-500",   # Styles the sliding circle
        container__class="p-4 bg-gray-50 rounded-lg",  # Styles the wrapper
    )
```

> **Note**: `Form.toggle()` and `Field.Boolean(form_type="toggle")` produce identical switch components. Both are consistent in appearance and behavior.

### Targeting nested sub-elements

All field kwargs follow the `prefix__attribute` convention:

| Prefix | Target element |
|--------|---------------|
| `menu__` | Dropdown menu container |
| `option__` | Individual dropdown options |
| `trigger__` | Dropdown trigger button |
| `slider__` | Toggle switch slider |
| `container__` | Toggle/field wrapper |
| `item__` | Dropdown/list items |

Any standard HTML attribute is supported: `class`, `style`, `data-*`, etc.

## Per-model configuration

Customize how a model appears in admin by adding a nested `Admin` class:

```python
from asok import Model, Field, ModelAdmin

class Post(Model):
    title = Field.String()
    body = Field.Text()
    slug = Field.Slug(source='title')
    published = Field.Boolean(default=False)
    author_id = Field.ForeignKey('users')
    content = Field.Text(wysiwyg=True) # Rich Text Editor

    author = BelongsTo('users')
    tags = BelongsToMany('tags')

    class Admin(ModelAdmin):
        label = "Posts"
        list_display = ['title', 'author', 'published', 'created_at']
        search_fields = ['title', 'body']
        list_filter = ['published', 'author_id']
        readonly_fields = ['created_at']
        form_exclude = ['slug']  # Hide from create/edit forms
        fieldsets = [
            ('Content', ['title', 'slug', 'body']),
            ('Publishing', ['published', 'author_id']),
        ]
        per_page = 25
        can_delete = True
        actions = ['publish_selected']

    @classmethod
    def publish_selected(cls, ids):
        cls.where('id', 'in', ids).update(published=True)
```

> Use **`asok.ModelAdmin`** as a base class for your inner `Admin` class to get full IDE autocompletion for all configuration options.

```python
from asok import Model, Field, ModelAdmin

class MyModel(Model):
    # ...
    class Admin(ModelAdmin):
        list_display = ["id", "name"]
        # Your IDE will now suggest all available options!
```

### Field visibility control

Control which fields appear in forms:

```python
class Category(Model):
    name = Field.String()
    slug = Field.Slug(populate_from='name')
    created_at = Field.CreatedAt()

    class Admin(ModelAdmin):
        form_exclude = ['slug', 'created_at']  # Completely hidden from forms
        readonly_fields = ['created_at']       # Shown but not editable
```

**Difference:**
- `form_exclude` — Field is **completely hidden** from create/edit forms
- `readonly_fields` — Field is **shown but disabled** (useful for auto-generated fields)

Use `form_exclude` for fields that auto-populate (like slugs) or timestamps. Use `readonly_fields` when you want users to see the value but not change it.

### All options

| Option | Type | Description |
|--------|------|-------------|
| `hidden` | `bool` | Hide this model from admin (`hidden = True`) |
| `slug` | `str` | URL slug (defaults to table name) |
| `label` | `str` | Display name in sidebar |
| `group` | `str` | Group models together in the sidebar |
| `list_display` | `list` | Columns in the list view |
| `search_fields` | `list` | Fields searched by the search box (multi-field OR-LIKE) |
| `list_filter` | `list` | Fields exposed as filters in the sidebar |
| `readonly_fields` | `list` | Fields displayed but not editable |
| `form_exclude` | `list` | Fields to exclude completely from create/edit forms |
| `fieldsets` | `list` | Group fields into labeled cards: `[(label, [fields]), ...]` |
| `per_page` | `int` | Pagination size (default 20) |
| `inlines` | `list` | Related models to display below the form (`['comments', ...]`) |
| `can_add` | `bool` | Allow creation (default `True`) |
| `can_edit` | `bool` | Allow editing (default `True`) |
| `can_delete` | `bool` | Allow deletion (default `True`) |
| `actions` | `list` | Names of `@classmethod`s exposed as bulk actions |

## Display helper

Foreign keys and relations are displayed using the related model's `__str__()` method, falling back to `name`, `title`, `label`, `email`, `username`, `slug`, then `#<id>`.

Define `__str__` to control the display:

```python
class User(Model):
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
```

## Features

- **Search** — multi-field LIKE across `search_fields`
- **Filters** — sidebar filter panel for `list_filter` fields
- **Sort** — click any column header
- **Pagination** — preserves search, filters, and sort
- **Separate detail view** — read-only view (`/view`) distinct from edit form, with permission-based button visibility. `Field.Text()` and WYSIWYG fields automatically span the **full width** of the detail grid instead of being split in two columns.
- **Bulk actions** — select rows and delete or run a custom action
- **Soft delete & trash** — restore or permanently delete from the trash view
- **CSV export** — exports the current filtered/sorted view
- **BelongsToMany editor** — checkbox grid for many-to-many relations
- **Rich Text Editor (WYSIWYG)** — supported on `Text` fields with `wysiwyg=True`
- **Inlines** — view related `HasMany` rows below the parent form, with edit links
- **Date / datetime / file pickers** — auto-detected from field types
- **Image preview** — preview uploaded images on the edit form
- **Breadcrumbs** — context-aware navigation
- **Save variants** — Save / Save and continue / Save and add another
- **Dark mode** — toggle in the topbar, persisted in localStorage
- **Empty values** — `—` shown for null/empty cells
- **Boolean badges** — colored Yes/No badges for boolean columns
- **Password protection** — password fields never displayed in detail view
- **Error pages** — beautiful 403, 404, and 500 error pages with admin design
- **Permission-aware UI** — all buttons and actions conditionally displayed based on user permissions

## Error Pages

The admin interface includes beautifully designed error pages that match the admin theme:

### Built-in Error Pages

- **403 Forbidden** — Access denied with login option
- **404 Not Found** — Page or item not found
- **500 Internal Server Error** — Server error with retry option

All error pages:
- Match the admin theme (light/dark mode support)
- Display contextual icons and messages
- Provide relevant action buttons (Go Back, Dashboard, Retry, Login)
- Are fully internationalized (English, French, Spanish)
- Show helpful messages without exposing sensitive information

### Custom Error Messages

To customize error messages in your admin extensions, use the `_render_error()` method:

```python
from asok.admin import Admin

class MyAdmin(Admin):
    def custom_check(self, request):
        if not some_condition:
            return self._render_error(
                request,
                403,
                self.t(request, "Custom Access Denied"),
                self.t(request, "You need special permission for this action."),
            )
```

The error page template automatically handles:
- Error code badge display
- Appropriate icons per error type
- Contextual action buttons
- Multi-language support

## Templates and static files

Templates and CSS/JS are bundled inside the `asok` package. To override a template, drop a file with the same name into `src/templates/admin/` (e.g., `src/templates/admin/list.html`) — your template wins.

The admin CSS is self-contained (no Tailwind required) and supports light/dark themes via CSS variables.

---
[← Previous: Asok Directives](29-asok-directives.md) | [Documentation](README.md) | [Next: API Development →](31-api-development.md)
