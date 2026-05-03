# Changelog

All notable changes to Asok Framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [0.1.3] - 2026-05-03

### Added
- **Admin Error Pages**: Professional error pages (403, 404, 500) with admin design consistency.
    - Contextual icons per error type (shield-off for 403, search for 404, alert-triangle for 500).
    - Error code badges with color coding.
    - Contextual action buttons (Go Back, Dashboard, Retry, Login).
    - Full internationalization support (English, French, Spanish).
    - Dark/light theme support matching admin interface.
- **ModelAdmin Base Class**: Introduced `asok.ModelAdmin` for professional developer experience.
    - Full IDE autocompletion for inner `Admin` configuration classes in models.
    - Type hints for all supported admin options (list_display, search_fields, fieldsets, etc.).
- **Validation Engine Enhancements**: Added 7 new powerful validation rules.
    - `url`, `slug`, `uuid`, `numeric`, `digits`, `boolean`, `between`.
    - Integrated corresponding i18n keys for all new rules.
- **Enhanced Template Engine**: Added several loop control and utility statements.
    - `{% break %}` and `{% continue %}` for granular loop control.
    - `{% do %}` statement for executing side-effects without output.
    - `{% call %}` block for advanced macros with `caller()` support.
    - `{% with %}` for creating local variable scopes.
- **CSRF Meta Tag**: Added `<meta name="csrf-token">` to admin base template for SPA-style requests.
    - Enables JavaScript AJAX requests to access CSRF token from DOM.
    - Proper integration with admin.js fetch requests.
- **Template Tests**: Comprehensive `is` operator support with 17 built-in tests.
    - Existence tests: `defined`, `undefined`, `none`.
    - Boolean tests: `true`, `false`, `boolean`.
    - Numeric tests: `even`, `odd`, `number`, `integer`, `float`.
    - Type tests: `string`, `sequence`, `mapping`, `iterable`.
    - String case tests: `lower`, `upper`.
    - Support for negation with `is not`.
- **Template Block Assignment**: `{% set variable %}...{% endset %}` for capturing template content.
    - Useful for building complex HTML strings.
    - Enables template fragment reuse.
    - Pass captured content to macros.
- **Filter Blocks**: Apply filters to entire template blocks.
    - Syntax: `{% filter upper %}content{% endfilter %}`.
    - Supports filter chaining in blocks.
- **Autoescape Blocks**: Fine-grained control over HTML escaping.
    - `{% autoescape false %}` to disable escaping for trusted content.
    - `{% autoescape true %}` to re-enable (default behavior).
    - Security warnings in documentation.
- **Admin `_render_error()` Method**: Centralized error page rendering for custom admin extensions.
    - Consistent error page design across all admin routes.
    - Easy integration for custom admin panels.
- **Data Tables Component**: Powerful, automated table generation with `Table` and `TableColumn` classes.
    - Auto-detection of columns from ORM models, lists, and dictionaries.
    - Built-in search functionality across multiple fields.
    - Dynamic filters with dropdown selects.
    - Server-side and client-side pagination.
    - Sortable columns (reactive mode).
    - Row actions (edit, delete, custom) with URL patterns.
    - Bulk selection with master checkbox.
    - Bulk actions (delete multiple items).
    - AJAX actions without page reload.
    - Reactive mode using Asok directives (asok-state, asok-for, asok-model).
    - Custom column rendering with templates or render functions.
    - Responsive design with empty states.
- **Rich Dropdown Component**: Premium searchable dropdown for forms with `Field.Dropdown()`.
    - Fixed choices dropdown with `Field.Dropdown(choices)` for static options.
    - Rich ForeignKey dropdowns with `dropdown=True` parameter.
    - Searchable dropdown with instant client-side filtering.
    - Support for title, subtitle, and image display.
    - Configurable with `dropdown_title`, `dropdown_subtitle`, `dropdown_image` parameters.
    - Click-outside-to-close behavior using Asok directives.
    - Automatic integration with `Form.from_model()`.
    - Reactive state management (asok-state, asok-show, asok-on).

### Fixed
- **Template Compilation Security**: Fixed incorrect parsing of `is` keyword within string literals.
    - Strings like `'2FA is Enabled'` no longer cause compilation errors.
    - Template compiler now properly distinguishes between `is` tests and quoted text.
    - String literals are protected from keyword interference.
- **CSRF Validation**: Resolved CSRF token validation failures in admin forms.
    - JavaScript now correctly reads CSRF token from meta tag.
    - Token prioritization: header > form field > JSON body.
    - Fixed empty header issue when meta tag was missing.
- **Admin Login CSRF UX**: Fixed a frustration where CSRF expiry showed a 403 page.
    - Catching `AbortException(403)` specifically in admin login.
    - Re-rendering login form with a friendly flash message instead of a hard error page.
- **Admin Dispatch Crash**: Fixed a critical 500 error where `AbortException` bubbled up to WSGI.
    - Wrapped admin dispatch in a safety `try-except` block in `core.py`.
    - Ensures security-related aborts are rendered via app's custom error pages.

### Changed
- **Session Cookie Security**: Enhanced cookie security flags.
    - Changed `SameSite` from `Lax` to `Strict` for session and CSRF cookies.
    - Automatic `Secure` flag on HTTPS connections.
    - `HttpOnly` flag on all sensitive cookies (session, CSRF, flash).
    - CSRF token rotation after successful validation.
- **Admin Error Handling**: Replaced raw HTML errors with template-based error pages.
    - All 404 errors now use `_render_error()`.
    - All 403 errors now use `_render_error()`.
    - Trash unavailable errors use proper error page.

### Documentation
- **Template Documentation**: Comprehensive update to template features guide.
    - Added block set, filter blocks, autoescape documentation.
    - Complete template tests reference with all 17 tests.
    - Clarified `data-block` selector syntax (DOM vs template blocks).
    - Security notes on string literal protection.
- **Admin Interface Documentation**: New error pages section.
    - Error page features and design.
    - Custom error message examples.
    - Integration guide for custom admin panels.
- **Security Audit Documentation**: Expanded comprehensive security review.
    - Detailed SQL injection protection analysis.
    - XSS protection mechanisms documented.
    - CSRF protection with token rotation.
    - Path traversal prevention details.
    - Password hashing (PBKDF2-SHA256, 100k iterations).
    - Session security (HttpOnly, Secure, SameSite flags).
    - Complete security score table (all categories 9-10/10).
    - OWASP compliance confirmation.
- **French & Spanish Translations**: Added error page translations.
    - "Error", "Access Denied", "Page Not Found", etc.
    - All error messages fully localized.

- **ReDoS Protection**: Secured all regex-based validation rules.
    - Enforced `_MAX_REGEX_INPUT_LENGTH` (10,000 characters) on all validation inputs.
    - Prevents Regular Expression Denial of Service attacks on core validation rules.
- **Enhanced CSRF Protection**: Multiple layers of CSRF defense.
    - Token rotation after validation prevents reuse attacks.
    - HMAC validation with constant-time comparison.
    - Origin/Referer validation for HTTPS requests.
    - SameSite=Strict cookies provide additional protection.
- **Template Security**: Protection against template injection attacks.
    - Keyword interference prevention in string literals.
    - Automatic HTML escaping by default.
    - SafeString class for explicit opt-in to raw HTML.
- **Path Traversal Prevention**: Absolute path validation with security checks.
    - `_safe_resolve()` utility ensures paths stay within allowed directories.
    - 403 Forbidden on escape attempts.
    - Static file serving validation.

## [0.1.2] - 2026-04-26

### Added
- **Asok Directives Engine**: A complete client-side reactive system (< 3KB) for "Zero JS" interactivity.
    - `asok-state`: Initializes local reactive state scopes.
    - `asok-text` / `asok-html`: Dynamic content rendering.
    - `asok-show` / `asok-hide`: Visibility toggling with `data-show-active` support.
    - `asok-model`: Two-way data binding for all form elements.
    - `asok-on`: Event handling with modifiers (`.prevent`, `.stop`, `.outside`, `.debounce`).
    - `asok-bind`: Dynamic attribute binding.
    - `asok-class`: Conditional CSS class management.
    - `asok-for`: Reactive loops with index and parent scope access.
    - `asok-if` / `asok-elif` / `asok-else`: Structural DOM conditioning.
    - `asok-teleport`: DOM node relocation with persistent reactivity.
    - `asok-init`: Lifecycle hooks for component initialization.
    - `asok-ref`: Direct element referencing via `$refs`.
    - `asok-cloak`: FOUC prevention with automatic style injection.
- **Deep Reactive Proxies**: Nested state tracking for transparent synchronization across complex objects.
- **Keyboard Modifiers**: Added `.enter`, `.escape`, `.tab`, and `.space` to `asok-on`.
- **Automatic CSP Nonce Injection**: Automatic security handling for all `<script>` tags using `strict-dynamic` policies.
- **Magic Variables**: Introduction of `$el`, `$event`, `$refs`, `$store`, and `$nextTick`.
- **Global Reactive Store**: Cross-component state synchronization via `window.Asok.store`.
- **Production Build Engine**: New `asok build` command for generating optimized distributions.
    - **Bytecode Packaging**: Automatic `.pyc` compilation with recursive `.py` source removal for protected, faster distributions.
    - **Universal Minification**: Recursive JS and CSS minification across `src/partials` using `esbuild`.
    - **HTML Template Optimization**: Build-time HTML minification to reduce file size and runtime CPU overhead.
    - **Smart WebP Conversion**: Automatic project-wide image optimization to WebP (originals removed) during build.
- **Enhanced CLI Entry Points**: Updated `asok preview` and other commands to support `wsgi.pyc` entry points, allowing projects to run without source files.
- **Runtime Performance Optimization**: Disabled redundant on-the-fly HTML minification in production mode (when using `dist/`).

### Fixed
- **Teleport Recursion**: Resolved infinite rendering loops in teleported elements.
- **Outside Click Race Condition**: Stabilized closure logic for modals and dropdowns.
- **Cursor Jumping**: Fixed focus/selection loss in two-way bound inputs.
- **Initial Loop Rendering**: Fixed visibility of text content in newly added loop items.

## [0.1.1] - 2026-04-22

### Added
- **Svelte-style Transitions**: Opt-in animations via `asok-transition` attribute (fade, slide, scale).
- **Unified Swap Engine**: Centralized `Asok.swap` API for both SPA navigation and WebSocket updates.
- **Admin UI Modernization**: New glassmorphism design, blurred modals, and refined impersonation banner.
- **Scoped Assets**: Dynamic, condition-based injection of page-specific CSS and JS files.
- **Alive Engine (WebSockets)**: Enhanced real-time synchronization for server-side reactive components.
- **Confirmation Modals**: Replaced native browser dialogs with premium, animated glassmorphism modals.
- **HTML Streaming**: Support for chunked delivery via `request.stream("page.html")` for improved TTFB.

### Changed
- Refactored `core.py` to support modular, independent asset injection.
- Standardized Admin icons with a consistent `1.75px` stroke weight.
- Improved SPA engine to handle full-page swaps and partial block updates via the same logic.
- Optimized WebSocket handshake for lower latency in Alive components.

### Fixed
- Fixed reliability of Scoped CSS/JS injection, especially when using the streaming engine.
- Fixed JS syntax errors in the Alive Engine's connectivity helper.
- Resolved issues where soft-deleted items remained visible in certain admin views.
- Corrected CSS collisions between admin styles and user-defined scoped assets.

## [0.1.0] - 2026-04-20

### Added
- **Initial Release**: The zero-dependency Python web framework.
- **File-based Routing**: Automatic route discovery based on `src/pages` directory.
- **Native ORM**: Simple SQLite-based ORM with migrations and model registry.
- **Template Engine**: Built-in Jinja2-compatible engine with zero external dependencies.
- **Admin Interface**: Auto-generated administrative dashboard for registered models.
- **Security First**: Automatic CSRF protection, secure cookies, and security headers.
- **CLI Tool**: Scaffolding, migrations, and development server management.

### Documentation
- Full framework overview and philosophy.
- Routing, Templates, and ORM guides.
- Deployment best practices.

[0.1.3]: https://github.com/asok-framework/asok/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/asok-framework/asok/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/asok-framework/asok/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/asok-framework/asok/releases/tag/v0.1.0
