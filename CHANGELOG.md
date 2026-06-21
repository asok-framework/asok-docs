# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [0.5.0] - 2026-06-21

### ⚡ Major Release: Zero-Eval Security & Framework-Wide Complexity Reductions

This release focuses on **absolute frontend security** and **long-term framework maintainability**. It introduces the **Zero-Eval Client Directives Engine** (completely eliminating client-side `eval` execution) and completes a comprehensive **Framework-Wide Code Complexity Reduction** campaign. Every core module, validation dispatcher, ORM helper, and template compiler state has been optimized to strictly conform to Grade A cyclomatic complexity metrics, ensuring superior runtime performance and maintainability.

---

### Added
- **Zero-Eval Client Directives Engine**: Introduced a secure client-side reactive directive compiler featuring a custom-built Python-based JavaScript AST scanner and parser (`_js_scanner.py`, `_js_parser.py`, `_expr_validator.py`). This engine parses client expressions, compiles them to clean DOM updates, and eliminates the use of dangerous `eval` calls.
- **Distributed Scheduler & Locks**: Integrated Redis-based distributed locking inside `asok/scheduler.py` to prevent duplicate execution of cron schedules across multiple clustered application instances.
- **Model Relationship & Lifecycle Events**: Decoupled ORM relationship management (`_model_relations.py`) and implemented robust event hooks for model lifecycle events (specifically delete event triggers, enabling clean manual or automatic cascading deletions of database records and linked files).
- **Self-Hosted Webfonts**: Added self-hosted WOFF2 fonts for the admin panel and documentation templates (`/fonts/` subdirectory in both admin and API static directories) to support zero-external-network dependencies.

### Improved
- **Framework-Wide Code Complexity Reductions**: Refactored, simplified, and modularized code across the entire framework (routing engine, forms, ORM database engine, validation dispatchers, WebSocket, templates, and request managers) to ensure every function and method strictly conforms to Grade A cyclomatic complexity, facilitating long-term maintenance and reducing performance overhead.
- **Redis Worker Architecture**: Upgraded the background task worker (`worker.py`) to utilize a concurrent `ThreadPoolExecutor` for parallel execution of task payloads, along with dead-letter queue (DLQ) capabilities and configurable exponential backoff retries.
- **Template Sandbox Isolation**: Refactored the template compiler into discrete components (`_compiler_state.py`, `_preprocess_helpers.py`, `_statement_compiler.py`) to isolate sandbox environments and state compiling, preventing scope leakage.
- **API & GraphQL Authorization**: Integrated explicit `GRAPHQL_AUTHORIZE` and `OPENAI_AUTHORIZE` configuration gates in `graphql.py` and `openapi.py` to secure schema query and API documentation pages.
- **Validation Rules Dispatcher**: Refactored rule validation to use a dedicated dispatch helper (`_rule_dispatch.py`) for clean validation pipelines.

### Fixed
- **SPA Blank Page on Load**: Resolved a template routing/rendering bug in `TemplateMixin._yield_block_item` where using a template context variable named `content` collided with the internal generator argument, resulting in blank pages upon first load.
- **Documentation Code Blocks Parsing**: Fixed a `SyntaxError: Unexpected token ')'` bug in `precompile_directives()` where code blocks containing example `asok-*` attributes in markdown files were incorrectly compiled as active client-side directives; introduced code/pre/script block masking before compilation.
- **WebSocket Mock Compatibility**: Fixed a crash in event listeners where mock WebSocket connections without `_rooms` properties caused error logs.
- **Test Suite Isolation**: Restructured test suites to separate SQLite connection states, preventing lockups and dirty states in test executions.

### Security
- **Session Replay Protection & Revocation**: Added strict session token replay checks and revocation triggers to invalidate old session tokens immediately on reuse or authentication transitions.
- **CSRF Verification Hardening**: Added strict validation of `Origin` and `Referer` headers on write requests inside the CSRF middleware.
- **Static File serving containment**: Enforced absolute canonical path verification on static file routes to completely block traversal outside allowed static and media directories.
- **Directive expression validation**: Integrated expression security validator (`_expr_validator.py`) to enforce safety limits on client directive definitions before compile.


## [0.4.0] - 2026-06-07

### Added
- **Community Extensions System**: Introduced a fully modular plug-and-play extension architecture that allows third-party packages to seamlessly register custom pages/controllers, templates/partials, and static assets. Includes rigorous path safety verification to prevent directory traversal vulnerabilities in extension layouts.
- **Hybrid SSR & Hydration (Islands, SSG & ISR)**: 
  - Selective hydration for islands architecture.
  - Static Site Generation (SSG) to pre-render parameterless pages during compilation (`asok build`).
  - Incremental Static Regeneration (ISR) with background stale-cache warming and revalidation intervals (`REVALIDATE`).
- **Built-in GraphQL Engine**: Seamless GraphQL server integration supporting model-to-schema auto-generation, WebSocket subscriptions, query complexity validation limits, and an embedded GraphQL playground in debug mode.
- **API Versioning Negotiation**: Professional API versioning management supporting URL-based (`/api/v1/`) and header-based versioning, negotiation headers, and deprecation sunset notifications.
- **Advanced WebSockets**: Real-time user presence tracking and status updates, room authorization hooks, direct messaging (DMs), typing indicators, and read receipts.
- **Multi-Database ORM Router**: Advanced ORM database router supporting read replicas, automatic write-master/read-replica query splitting, and sharding strategies.

### Improved
- **Top-level Extension API**: Exposed `AsokExtension` directly at the root of the `asok` package for cleaner third-party imports.
- **SSG Build Imports Isolation**: Wrapped SSG generation in `asok build` with a dynamic `sys.path` injection and cleanup of the build directory, avoiding `ModuleNotFoundError` during compilation of pages containing local imports.

---

## [0.3.0] - 2026-06-01

### Added
- **Async Concurrency & ASGI/WSGI Dual Engine**: Added support for asynchronous programming, including `async def` page controllers, asynchronous middlewares, and non-blocking database queries (via `*_async` ORM methods). Built-in seamless interoperability allows sync and async middlewares/handlers to be mixed freely under both ASGI (Uvicorn) and WSGI (Gunicorn) servers.
- **Config-driven DB Binds (Multi-DB & Cross-Engine)**: Support for connecting models to multiple databases simultaneously across SQLite, PostgreSQL, and MySQL backends by binding model classes to specific environment variables (e.g., `_db_path = "LOGS_DATABASE_URL"`), keeping credentials out of the codebase.
- **Advanced PostgreSQL & MySQL Support**: Built-in support for PostgreSQL connection pooling (via `psycopg_pool`), MySQL thread-safe connections, automatic schema migration handling, full-text GIN indexing, and vector similarity search.
- **Redis Cache & Session Backends**: Introduced native Redis support for high-performance caching and session persistence.
- **S3 Cloud Storage**: Built-in support for AWS S3 file storage with automatic mime-type guessing and region-specific subdomain routing to avoid broken media links.
- **Automatic DB Connection Teardown**: Auto-release database connections back to pools (for PostgreSQL, MySQL, and SQLite) at the end of every ASGI and WSGI request, preventing resource leaks and database locking issues.
- **Database Fixtures Commands**: Added new CLI commands `asok dumpdata` (to dump database records to a JSON fixture file) and `asok loaddata` (to load records from a JSON fixture file), simplifying data seeding and environment migrations.
- **CLI Background Task Worker**: Added `asok worker` command to start a dedicated background task processing worker with built-in Redis connection resilience, automatic reconnection recovery on connection loss, and silent socket timeout handling during idle queue periods.

### Improved
- **Async Concurrency & Interoperability**:
  - Resolved `TypeError: 'str' object can't be awaited` when async middlewares wrap sync controllers under ASGI by introducing safe async wrappers.
  - Resolved issue where async middlewares under WSGI returned raw, unawaited coroutines; now run seamlessly using a thread-safe `async_to_sync` event-loop bridge.
  - Enhanced ASGI startup/shutdown lifespan hooks to support partial async functions (`functools.partial`) and custom callables returning coroutines.
- **Locale-based GeoIP Fallback**: The GeoIP lookup engine now falls back to request locale (e.g., `fr` -> `FR` / `+33` / `Paris`) when looking up private/localhost IPs.
- **Timezone Mapping**: Added `"CD": "Africa/Kinshasa"` to the country-to-timezone mapping.
- **Client-Side Directives & SPA Reactivity**:
  - Propagated dynamic element initialization (`window.Asok.init`) inside structural directives like `asok-if` and `asok-for`.
  - Preserved cursor focus and selection on active inputs during virtual DOM patches.
  - Avoided circular dependency JSON crashes in client-side state serialization.

### Security
- **Timing Attack Prevention**: Prevented password-reset and login timing attacks by applying a 150ms delay + random jitter on all Magic Link checks.
- **Host Header Injection Protection**: Blocked Host Header injection in production by forcing validation against `APP_URL`.


## [0.1.7] - 2026-05-25

### 🏗️ Major Release: Framework Refactoring & Architecture Overhaul

This release focuses on **long-term maintainability** and **code organization**, transforming Asok from monolithic files into a clean, modular architecture. This major refactoring lays the foundation for future scalability while maintaining 100% backward compatibility.

---

### 🔧 Architecture & Refactoring

**Complete Module Restructuring** - Monolithic files split into organized packages:

#### Core Modules Refactored
- **CLI Module** (`asok/cli/` ← `asok/cli.py`):
  - `main.py` - Main CLI entry point
  - `build.py` - Production build system
  - `database.py` - Database management commands
  - `deploy.py` - Deployment utilities
  - `generators.py` - Code generation tools
  - `runner.py` - Development server
  - `scaffold.py` - Project scaffolding
  - `server.py` - WSGI server management
  - `style.py` - Styling utilities
  - `tools.py` - CLI helper functions

- **Core Engine** (`asok/core/` ← `asok/core.py`):
  - `asok.py` - Main framework class
  - `assets.py` - Asset management and compilation
  - `errors.py` - Error handling
  - `lifecycle.py` - Application lifecycle hooks
  - `loaders.py` - Module and resource loaders
  - `routing.py` - URL routing engine
  - `security.py` - Security middleware
  - `smart_streamer.py` - HTML streaming
  - `static.py` - Static file serving
  - `wsgi.py` - WSGI application interface

- **Forms System** (`asok/forms/` ← `asok/forms.py`):
  - `field.py` - Form field definitions
  - `form.py` - Form class and validation
  - `mixins.py` - Reusable form mixins
  - `render.py` - Form rendering engine
  - `utils.py` - Form utilities

- **ORM Module** (`asok/orm/` ← `asok/orm.py`):
  - `model.py` - Model base class
  - `field.py` - Field types and validation
  - `query.py` - Query builder
  - `relation.py` - Relationship management
  - `migrations.py` - Schema migrations
  - `fileref.py` - File reference handling
  - `list.py` - Model list utilities
  - `proxy.py` - Lazy loading proxies
  - `utils.py` - ORM utilities
  - `exceptions.py` - ORM-specific exceptions

- **Request Handling** (`asok/request/` ← `asok/request.py`):
  - `request.py` - Request object
  - `response.py` - Response handling
  - `auth.py` - Authentication utilities
  - `csrf.py` - CSRF protection
  - `session.py` - Session management
  - `template.py` - Template rendering context
  - `upload.py` - File upload handling
  - `metadata.py` - Request metadata
  - `query_dict.py` - Query string parser
  - `env.py` - Environment utilities
  - `user_agent.py` - User agent parsing

- **Template Engine** (`asok/templates/` ← `asok/templates.py`):
  - `compiler.py` - Template compilation
  - `engine.py` - Template rendering engine
  - `preprocessor.py` - Template preprocessing
  - `resolver.py` - Variable resolution
  - `filters.py` - Template filters
  - `tests.py` - Template test functions
  - `loop.py` - Loop utilities
  - `safestring.py` - HTML safety
  - `sandbox.py` - Template sandboxing

- **Validation System** (`asok/validation/` ← `asok/validation.py`):
  - `validator.py` - Main validation engine
  - `schema.py` - Schema definitions
  - `rules.py` - Validation rules
  - `registry.py` - Rule registration
  - `interpolation.py` - Error message interpolation

- **WebSocket Module** (`asok/ws/` ← `asok/ws.py`):
  - `server.py` - WebSocket server
  - `connection.py` - Connection management
  - `protocol.py` - WebSocket protocol
  - `live.py` - Live component updates

#### Admin Panel Refactored
- **Admin Architecture** (`asok/admin/`):
  - `core.py` - Admin core functionality
  - `models.py` - Admin model definitions
  - `views/` - Organized view modules
  - `forms.py` - Admin form handling
  - `widgets.py` - Custom form widgets
  - `utils.py` - Admin utilities
  - `rbac.py` - Role-based access control
  - `logs.py` - Admin logging
  - `constants.py` - Admin constants

---

### 📦 Build & Distribution

- **Asset Compilation**:
  - Pre-compiled minified assets for admin, API, toolbar, and core
  - Optimized MANIFEST.in for minimal package size
  - Only minified files included in PyPI distribution
  - Updated package metadata for Python 3.13 support

- **Package Structure**:
  - Cleaner import paths maintained via `__init__.py` exports
  - 100% backward compatibility - all existing imports still work
  - ~20,000 lines of code reorganized into logical modules

---

### 📝 Documentation

- **README Improvements**:
  - Updated framework overview and feature highlights
  - Improved quick start examples
  - Enhanced reactive component examples
  - Better structured documentation links

---

### 🧪 Testing

- **New Test Coverage**:
  - `test_api_static_files.py` - API static file serving
  - `test_csrf_rotation_ajax.py` - CSRF token rotation in AJAX
  - `test_reactive_spa_fixes.py` - SPA navigation and reactivity
  - `test_toolbar_injection.py` - Developer toolbar integration
  - Enhanced file streaming tests

---

### 🔄 Migration Notes

**Breaking Changes**: None - this is a purely internal refactoring.

**What Changed**:
- File structure reorganized from flat files to packages
- All public APIs remain identical
- Imports like `from asok import Asok, Model, Form` still work
- Entry point `asok` CLI unchanged

**Benefits for Developers**:
- Easier to navigate codebase
- Better IDE support for go-to-definition
- Clearer separation of concerns
- Simplified future contributions
- Foundation for plugin system (future)

---

### Performance

- No performance regression - refactoring is purely organizational
- Slightly improved import times due to better module granularity
- Asset compilation reduces runtime overhead

---

### Dependencies

No new dependencies added. Framework remains **100% zero-dependency** with only Python 3.10+ standard library.

---

## [0.1.6] - 2026-05-15

### 🎉 Major Release: Security 10/10 & Enhanced UX

This release focuses on **production-grade security** and **modern UI transitions**, bringing Asok to a perfect **10/10 OWASP security score** and SvelteKit-quality animations.

---

### 🔒 Security Enhancements (Score: 10/10)

**22 Vulnerabilities Fixed** across all severity levels:

#### Critical Fixes (3/3)
- **JavaScript Injection Protection**: Added AST validation for Asok directives (`asok-text`, `asok-on:*`, etc.)
  - Whitelist of allowed AST nodes (Name, Attribute, BinOp, Call, etc.)
  - Blacklist of dangerous functions (`eval`, `exec`, `__import__`, dunder methods)
  - Prevents code injection via template expressions
- **Secure Component State**: Enhanced state serialization with strict type validation
  - Only JSON-safe types allowed (str, int, float, bool, None, list, dict, tuple)
  - Recursive validation for nested structures
  - Prevents object injection attacks
- **XSS Prevention**: Verified automatic HTML escaping in all template variables
  - All `{{ var }}` expressions are escaped by default via `_html.escape()`
  - SafeString requires explicit opt-in

#### High Priority Fixes (5/5)
- **SQL Injection Protection**: Added comprehensive SQL identifier validation
  - Strict regex validation: `[a-zA-Z_][a-zA-Z0-9_]{0,63}`
  - Blacklist of SQL reserved words (SELECT, DROP, DELETE, etc.)
  - Applied to all dynamic schema operations (tables, columns, indexes, pivot tables)
- **Path Traversal Protection**: Enhanced file serving security
  - Uses `pathlib.Path.resolve(strict=True)` for robust path resolution
  - Validates all parent directories for symlinks
  - Only accepts basename to prevent traversal attacks
  - Returns `403 Forbidden` on escape attempts
- **WebSocket Origin Validation**: Strict origin checks even in debug mode
  - Only localhost/127.0.0.1 allowed in debug with `allowed_origins="*"`
  - Explicit whitelist required in production
  - Prevents CSRF via WebSocket
- **Timing Attack Protection**: Constant-time operations for authentication
  - No early returns in `MagicLink.verify_token()`
  - Random delays (1-5ms) on failure
  - Prevents user enumeration via timing
- **File Upload Security**: Enhanced MIME validation
  - Warnings logged if `allowed_types` not specified
  - Secure filename (UUID) by default
  - Restrictive permissions (0o644) on saved files
- **Subprocess & Confinement Security**: Added path confinement for binary invocations
  - Enforced strict `os.path.commonpath` verification in the image optimizer (`optimize_image`) to restrict binary execution pathways to `.asok/bin`, preventing path traversal attacks.
- **Production Logging Upgrades**: Replaced generic prints and silent swallowed errors
  - Eliminated bare `except Exception: pass` blocks in the GeoIP engine and raw `traceback.print_exc()` calls in the WebSocket server.
  - Implemented standard logging warnings and errors mapped directly to their respective module loggers (`asok.utils.geo` and `asok.ws`) for structured production auditing.

#### Medium & Low Priority Fixes (6/6)
- **Error ID Tracking**: Unique UUID for each error in production
  - Generic messages shown to users
  - Full stack traces logged internally with ID
  - Prevents information disclosure
- **Rate Limiting**: Brute force protection on authentication
  - Max 5 attempts per IP address
  - 15-minute lockout after failed attempts
  - 1-2 second delays to slow attackers
- **CSRF Token Rotation**: Tokens regenerated after login/logout
  - Prevents CSRF token fixation attacks
  - Automatic rotation on session changes
- **Security Headers**: Added `Permissions-Policy` header
  - Restricts access to geolocation, microphone, camera, payment APIs
  - Complements existing headers (CSP, HSTS, X-Frame-Options, etc.)
- **Email Validation**: RFC 5322 compliant regex
  - Validates local part and domain structure
  - Rejects malformed emails
- **Route Parameter Limits**: Max 255 characters per URL parameter
  - Prevents DoS via extremely long URLs
  - Early rejection with debug logging

---

### 🎨 UI/UX Enhancements

#### Enhanced Transitions System
**SvelteKit-Quality Animations** with professional easing curves:

- **6 Built-in Transitions**:
  - `fade` - Smooth opacity (ease-out)
  - `slide` - Horizontal slide + fade (cubic-bezier expo)
  - `scale` - Subtle zoom effect (cubic-bezier quart)
  - `fly` ⭐ NEW - Vertical fly in/out (cubic-bezier expo)
  - `blur` ⭐ NEW - Blur + fade effect (modern, subtle)
  - `bounce` ⭐ NEW - Elastic bounce (cubic-bezier back)

- **Professional Easing Curves**:
  ```css
  --ease-out-quart: cubic-bezier(0.25, 1, 0.5, 1);
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out-back: cubic-bezier(0.68, -0.6, 0.32, 1.6);
  ```

- **SPA Page Transitions**: Full-page animations on navigation
  - `data-asok-page-transition="page"` for automatic transitions
  - Custom duration support: `data-asok-page-transition="fade 400"`
  - Automatic scroll-to-top on navigation

- **Performance**: GPU-accelerated (transform + opacity only), <3KB minified

#### MIME Type Validation
**Automatic File Upload Protection** with magic bytes detection:

- **50+ Supported Formats**:
  - 🖼️ Images (11): JPEG, PNG, GIF, WebP, BMP, TIFF, ICO, SVG
  - 🎵 Audio (8): MP3, WAV, FLAC, OGG, AAC, M4A
  - 🎬 Video (6): MP4, WebM, MKV, AVI, MOV, 3GP
  - 📄 Documents (10+): PDF, ZIP, DOCX, XLSX, PPTX, RTF, Office files, Archives

- **Smart Detection**:
  - Magic bytes validation (actual file content, not extension)
  - Handles ambiguous formats (RIFF → WebP/WAV/AVI, ftyp → MP4/M4A/MOV/3GP)
  - Extension matching enforcement
  - Sub-signature detection for complex formats

- **Security Features**:
  ```python
  # Secure by default
  photo.save("uploads/", allowed_types=['image/jpeg', 'image/png'])

  # Security warnings if misconfigured
  file.save("uploads/")  # ⚠️ Warning: no allowed_types specified
  ```

---

### Added

- **Deep UI Customization (Prefix Targeting)**:
    - Unified `prefix__attribute` syntax across Forms, Tables, ORM Fields
    - Granular Tailwind CSS targeting: `dropdown__menu__class`, `table__header__class`, `pagination__link__class`
    - Automatic attribute propagation from ORM Field definitions to UI components

- **Enhanced Developer APIs**:
    - Added `@app.rate_limit()`, `@app.cache_page()`, `@app.schedule()`, `@app.background()` decorators
    - Exported `cache_page` globally in `asok` package

- **Unified Exception Hierarchy**:
    - Centralized all framework errors under `AsokException`
    - Integrated `MailError` for consistent email error handling
    - Automatic HTTP status mapping for semantic exceptions

- **Fail-Fast Mail Service**:
    - Added `raise_on_error=True` to synchronous email dispatch

---

### Improved

- **Table Module Architecture**:
    - Refactored `Table` and `TableColumn` for arbitrary kwargs and deep UI customization
    - Shared rendering utilities (`_extract_nested_attrs`, `_render_attrs`) across framework

- **Documentation**:
    - Complete MIME validation guide in File Storage docs
    - Enhanced Transitions documentation with all 6 types
    - Updated Security Audit with all fixes
    - README.md highlights for v0.1.6 features

---

### Fixed

- **Security**: 22 vulnerabilities fixed (3 Critical, 5 High, 3 Medium, 7 Low, 4 Info)
- **Linting**: Import sorting compliance in `asok/request.py`
- **Code Quality**: Cleaned up duplicate imports and residual code

---

### Migration Notes

**Breaking Changes**: None - all changes are backward compatible.

**Recommended Actions**:
1. Update file upload code to use `allowed_types` parameter
2. Add `data-asok-page-transition` to main content containers for smooth navigation
3. Review security warnings in logs and add MIME type whitelists

**Security Baseline**: Asok v0.1.6 achieves **10/10 OWASP Top 10 compliance** and is production-ready for security-critical applications.

---

### Performance

- Transitions: <3KB minified JavaScript, GPU-accelerated
- MIME Validation: Only reads first few bytes (magic bytes), minimal overhead
- Rate Limiting: In-memory cache, negligible latency

---

### Dependencies

No new dependencies added. All security and UX features use Python stdlib and existing dependencies.

## [0.1.4] - 2026-05-09

### Added
- **Developer Toolbar (Premium Console)**:
    - Real-time SQL Profiler with AJAX/SPA support (dynamic update via `X-Asok-SQL-Log`).
    - Cross-request persistence for SQL logs during redirects and `request.block` renders.
    - Reactive State Monitor to inspect Asok Directives and Live Components in real-time.
    - Session & Request Payload inspector with forced text wrapping for large data.
    - Template Rendering Pipeline viewer to debug block rendering.
    - High-contrast "Premium" design with glassmorphism and automatic visibility on all backgrounds.
- **Advanced Form Engine**:
    - 18+ new UI fields: `dropdown` (searchable), `image` (preview), `tags`, `daterange`, `toggle`, `otp`, `month`, `rating`, `timerange`, `files` (multi-upload), `autocomplete`, `cascading` (dependent selects), `phone` (flags), `wysiwyg` (rich text), `dropzone`, `signature` (canvas), `transfer`, and `treeselect`.
    - Full CSP compliance for all reactive form components (no inline scripts/styles).
- **ORM & Migrations**:
    - **Zero-Config Auto-Migrations**: Automatic database schema evolution (automatic `ALTER TABLE` to add columns on Model changes).
    - **Migration Tracking**: Dedicated `_asok_migrations` table to track applied migration batches.
    - **CLI Support**: New `asok make migration <name>`, `asok migrate --fake`, `asok migrate --rollback`, and `asok migrate --status` commands for database version management.
    - Database indexes support: `Field.String(index=True)`.
    - Set operations support: `Query.union()` and `Query.intersect()`.
    - Subqueries support in `WHERE IN` clauses for complex filtering.
    - Improved table naming strategy with `snake_case` pluralization (e.g., `OrderItem` -> `order_items`).
    - Added `group_by()` and `select()` methods to the Query builder.
- **Real-time & Serialization**:
    - **Real-time Live Data**: `data-subscribe` directive for automatic DOM updates when database records change via WebSockets.
    - **Serialization Context**: `Schema` now automatically detects request context via `contextvars`, simplifying absolute URL generation in API responses.
- **Validation System**:
    - 12 new validation rules: `url`, `boolean`, `slug`, `uuid`, `alpha`, `alpha_num`, `tel`, `color`, `month`, `base64`, `json`, `between`.
    - Global **ReDoS protection**: all regex validators now check input length against `_MAX_REGEX_INPUT_LENGTH`.
- **Developer Experience (DX)**:
    - New `ModelAdmin` base class for structured administration with full IDE autocompletion and simplified field overrides.
    - Enhanced OpenAPI generator with support for tags, summaries, and better schema resolution.
- **Template Engine**:
    - Added support for `{% break %}`, `{% continue %}`, `{% do %}`, `{% with %}`, and `{% call %}` tags.
    - New `decode_base64` filter for displaying binary data (avatars, signatures) directly in HTML.
- **SEO Management**:
    - Automatic suppression of SPA markers in `title` and `description` blocks for clean browser tab names.

### Fixed
- Fixed SQL Log persistence failure during `RedirectException` and `request.block`.
- Fixed missing padding in Debug Suite time column.
- Fixed horizontal scrollbar issues in Debug Suite for large payloads.
- Fixed floating trigger visibility on white backgrounds with a high-contrast glow effect.
- Fixed Admin security: Improved CSRF handling and global error catching for production stability.

### Changed
- Refactored `DeveloperToolbar` into a decoupled module for better maintainability.
- Standardized all UI components to use the new "Premium Admin" design system tokens.


## [0.1.3] - 2026-05-03

### Added
- **Admin Interface**: Professional dashboard for managing models and media.
- **Translations (i18n)**: Multi-language support with JSON locales.
- **WebSockets**: Real-time bidirectional communication engine.
- **Background Tasks**: Non-blocking function execution.

### Changed
- Improved Hot Reloading performance in DEBUG mode.
