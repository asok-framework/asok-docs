# Changelog

All notable changes to Asok Framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


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

[0.1.1]: https://github.com/asok-framework/asok/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/asok-framework/asok/releases/tag/v0.1.0
