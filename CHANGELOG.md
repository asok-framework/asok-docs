# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


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
