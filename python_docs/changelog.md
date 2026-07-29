# Changelog

All notable changes to the Asok Framework are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.6.0] - 2026-07-29

### ⚡ Major Release: Zero-JS UI Directives, Automated Database Backup CLI, Admin Graphical RBAC & Trash Bin, Security Audit & Tooling Pipeline

This major release brings extensive enhancements across the entire Asok Framework ecosystem: zero-JS reactive UI directives, an automated database backup system with CLI management, a revamped Admin interface with graphical RBAC permissions, trash bin & soft-delete manager, active session management, strict security hardening, Radon Grade A complexity refactoring, and a complete code audit & analysis pipeline in the Makefile.

---

### Added
- **Automated Database Backup Engine & CLI (`asok/backup.py`, `asok/cli/backup.py`)**:
  - Implemented automated database snapshotting supporting SQLite, PostgreSQL, and MySQL.
  - Added CLI commands: `asok backup create`, `asok backup list`, `asok backup restore`, and `asok backup prune`.
  - Configurable backup management: `DATABASE_BACKUP_ENABLED`, `DATABASE_BACKUP_URL`, `DATABASE_BACKUP_PATH`, `DATABASE_BACKUP_MAX_SNAPSHOTS`, and `DATABASE_BACKUP_INTERVAL`.
- **Zero-JS Reactive UI & Utility Directives Engine (`asok/core/assets/asok_directives.js`)**:
  - **Keyed List Reconciliation**: Added `asok-key` (`asok-key-ref`) for per-item keyed DOM list reconciliation in `asok-for` loops.
  - **Theme Toggle**: Added `asok-theme-toggle` (`data-asok-theme-toggle`, `data-theme-toggle`) with anti-FOUC script and OS preference sync.
  - **Cookie Consent**: Added GDPR compliance attributes: `asok-cookie-banner`, `asok-cookie-accept`, `asok-cookie-reject`, `asok-cookie-reset`, and script-blocking `asok-cookie-script` (`data-cookie-*`).
  - **Dismissible UI**: Added `asok-dismiss` and `asok-dismiss-trigger` (`data-asok-dismiss`, `data-dismiss`, `data-asok-dismiss-trigger`, `data-dismiss-trigger`) with `localStorage` state persistence.
  - **Clipboard Copy**: Added `asok-copy` (`data-asok-copy`, `data-copy`) for code blocks, inputs, and text elements with visual feedback.
  - **Accessible Modals**: Added `asok-modal`, `asok-modal-open`, `asok-modal-close` (`data-asok-modal*`, `data-modal*`) with `Escape` key and backdrop handling.
  - **Smooth Scroll**: Added `asok-scroll-top` and `asok-scroll-to` (`data-asok-scroll-*`, `data-scroll-*`) with position threshold detection.
  - **Character Counter**: Added `asok-char-count` (`data-asok-char-count`, `data-char-count`) for inputs and textareas.
  - **Tabbed Interfaces**: Added `asok-tabs`, `asok-tab`, and `asok-tab-panel` (`data-asok-tab*`, `data-tab*`) with ARIA accessibility.
  - **Page Progress Bar**: Added `asok-progress` (`data-asok-progress`, `data-progress`) for automatic top navigation progress bar updates.
  - **HTML5 Validation Compliance**: Supported `data-asok-*` and `data-*` attribute aliases across all directives.
- **Admin Graphical RBAC & Permissions Matrix (`asok/admin/access_rules.py`, `asok/admin/views/crud.py`)**:
  - Graphical RBAC editor in the Admin panel for visually assigning model and action permissions per role.
  - Column-level & Row-level Scope authorization rules for fine-grained user data isolation.
  - Read-only system models protection and model-level field authorization.
- **Admin Trash Bin & Soft Delete Management (`asok/admin/templates/trash.html`)**:
  - Built-in Trash Bin manager allowing administrators to view, restore, or permanently purge soft-deleted records.
- **Active Session Management (`asok/admin/templates/active_sessions.html`)**:
  - Admin view to list, inspect, and revoke active user sessions in real time.
- **Admin Asset Integrations**:
  - Integrated local Flatpickr date/time pickers and Chart.js for dashboard analytics.

### Improved
- **Radon Cyclomatic Complexity Refactoring**:
  - Refactored `_clean_url_html()` and `_is_dangerous_protocol_html()` in `asok/utils/html_sanitizer.py` to achieve Grade A (complexity 2).
  - 100% of functions and methods across the framework now satisfy Grade A cyclomatic complexity.
- **Declarative Migrations & ORM Improvements**:
  - Enhanced migration auto-detector and schema backfilling for `NOT NULL` columns.
  - Added foreign key auto-accessor methods and automated pivot table provisioning (`role_user`).
- **Template Filters**:
  - Added timestamp filter `epoch` (`{{ timestamp | epoch('%d/%m/%Y %H:%M') }}`) in `asok/templates/filters.py`.

### Security
- **Bandit Security Audit & Non-Cryptographic Hashes**:
  - Remediated all Bandit security findings by adding `usedforsecurity=False` across non-cryptographic `hashlib.md5()` and `hashlib.sha1()` calls (`asok/admin/core.py`, `asok/core/_asset_injector.py`, `asok/core/static.py`, `asok/orm/query.py`, `asok/templates/compiler.py`, `asok/templates/engine.py`, `asok/ws/protocol.py`). High-severity Bandit security issues reduced from 8 to **0**.
- **Hardcoded Secrets & Token Verification**:
  - Integrated `dodgy` secret scanner; verified **0** hardcoded passwords, tokens, or API keys in the codebase (`{"warnings": []}`).
- **Session & Sandbox Hardening**:
  - Session key truncation & payload size limits in `asok/session.py`.
  - Strict CSRF Origin/Referer verification and template sandbox undefined value handling (`asok/templates/undefined.py`).

### Fixed
- **ORM Async Querybuilder Indentation**:
  - Resolved a critical indentation bug in `asok/orm/query.py` where terminal async methods (`get_async()`, `first_async()`, `paginate_async()`, `count_async()`, etc.) were indented inside `_compute_page_counts` after its `return` statement.
- **Dead Code Cleanup (Vulture Audit)**:
  - Removed unused internal helper functions `_collect_config_morph_models` (`asok/admin/forms.py`), `_slugify_name` and `_humanize` (`asok/admin/utils.py`), and `_build_migration_sql` (`asok/cli/generators.py`). Renamed parameter `expected_type` to `_expected_type` in `template.py`.

### Documentation & Tooling
- **Makefile Analysis Pipeline**:
  - Added `bandit`, `audit` (`pip-audit`), `secrets` (`dodgy`), `vulture`, and `pyright` targets to `Makefile` for one-command code quality and security scanning.
- **Documentation Updates**:
  - Documented database backup configuration parameters in Section 9 (Database & ORM) across all documentation suites.
  - Documented `epoch` filter in Section 4 (Templates).
  - Integrated full `CHANGELOG.md` into `python_docs/` suite and added `changelog` to Sphinx `index.md` `toctree`.
  - Cleaned up redundant manual footer navigation links from `python_docs/`.

## [0.5.1] - 2026-06-24

### Fixed
- **CLI createsuperuser Pivot Table Provisioning**: Resolved a database table error/warning in the `createsuperuser` command where attempting to attach the admin role failed if the `role_user` pivot table did not exist.
- **Documentation Roadmap Width**: Converted the Markdown comparison table in `README.md` to HTML with a `100% width` layout to ensure correct full-width rendering in all markdown engines.
