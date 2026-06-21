# Asok Documentation

> **Latest Version: v0.5.0**
>
> * **Zero-Eval Client Directives**: Advanced, secure client-side reactive directives powered by a custom JavaScript AST scanner and parser (completely eliminating dangerous `eval`).
> * **Framework-Wide Complexity Optimization**: Entire codebase refactored and modularized to strictly satisfy Grade A cyclomatic complexity, maximizing runtime performance and maintainability.
> * **Persistent Workers & Distributed Scheduler**: Distributed lock-protected scheduled tasks (cron) and concurrency-resilient worker instances with background thread pools.
> * **Production-Hardened Security**: ORM delete lifecycle events, session replay protection, strict CSRF Origin/Referer verification, and sandboxed template engines.



Welcome to the Asok Framework documentation. This guide is organized sequentially to take you from a total beginner to an advanced contributor.

## ⚡ Quick Reference: How do I...

If you are looking for a specific topic, here is a quick mapping of common developer tasks to their respective documentation pages:

| Task | Relevant Guide | Key Concepts |
|---|---|---|
| **Create and run a new app** | [Getting Started](01-getting-started.md) | `asok create`, `asok dev` |
| **Define dynamic URLs / routing** | [Routing](02-routing.md) | Dynamic parameters `[id:int]`, request methods |
| **Get query params, cookies or request headers** | [Request Handling](03-request.md) | `request.args`, `request.cookies`, `request.headers` |
| **Define custom pages / extend templates** | [Templates](04-templates.md) | Template inheritance, blocks, standard filters |
| **Protect routes, execute pre/post request logic** | [Middleware](05-middleware.md) | Middlewares, hook system |
| **Configure databases and run SQL queries** | [ORM Basics](07-orm.md) & [Advanced ORM](08-advanced-orm.md) | Models, `Model.filter()`, complex queries, indexes |
| **Manage database schemas & run migrations** | [Migrations](09-migrations.md) | `asok make migration`, `asok migrate` |
| **Perform semantic or vector searches** | [Native Vector Search](10-vector-search.md) | `Field.Vector()`, cosine similarity |
| **Handle form submissions & validation** | [Forms](11-forms.md) & [Validation](14-validation.md) | Declarative forms, `Form.validate()`, rules |
| **Log users in & protect pages** | [Authentication](17-authentication.md) & [Sessions](19-sessions.md) | User authentication, session backend |
| **Implement OAuth2, Magic Links or API Keys** | [Advanced Authentication](18-advanced-authentication.md) | Social login, bearer tokens |
| **Rate limit endpoints to prevent abuse** | [Rate Limit](22-rate-limit.md) | Rate limiting, redis/local bucket |
| **Build dynamic, stateful UI components** | [Reactive Components](24-reactive-components.md) | Live components, reactive state |
| **Implement real-time features (websockets)** | [WebSockets](32-websockets.md) | WebSocket server, custom handlers |
| **Send emails in the background** | [Email Service](33-email-service.md) | SMTP email client, background threads |
| **Run background tasks / cron jobs** | [Background Tasks](35-background-tasks.md) & [Scheduled Tasks](36-scheduler.md) | Background workers, cron scheduler |
| **Configure Gunicorn, Nginx & Nginx TLS** | [Deployment](39-deployment.md) | Production configs, systemd services |
| **Write unit tests for my app** | [Testing](40-testing.md) | `TestClient`, request assertions |


## 🟢 Foundations
01. [Getting Started](01-getting-started.md) — Installation and your first app.
02. [Routing](02-routing.md) — Defining URLs and dynamic parameters.
03. [Request Handling](03-request.md) — Working with headers, queries, and bodies.
04. [Templates](04-templates.md) — The Asok template engine syntax.
05. [Middleware](05-middleware.md) — Intercepting and modifying requests.
06. [Configurations](06-configurations.md) — Managing environment and app settings.

## 📊 Database & ORM
07. [ORM Basics](07-orm.md) — Models and basic Queries.
08. [Advanced ORM](08-advanced-orm.md) — Indexes, Union/Intersect, Subqueries, and complex filtering.
09. [Migrations](09-migrations.md) — Versioned database schema management.
10. [Native Vector Search](10-vector-search.md) — Semantic search with SQLite.

## 📝 Forms & Data
11. [Forms](11-forms.md) — Declarative HTML forms and model mapping.
12. [Advanced Forms](12-advanced-forms.md) — Enums, JSON, and custom field types.
13. [Form Actions](13-form-actions.md) — Handling submissions without complex routing.
14. [Validation](14-validation.md) — Built-in validation rules and custom logic.
15. [Serialization](15-serialization.md) — Controlling JSON output with Schemas.
16. [File Storage](16-file-storage.md) — Handling uploads and serving files.

## 🔒 Security & Auth
17. [Authentication](17-authentication.md) — Sessions, Login, and Register.
18. [Advanced Authentication](18-advanced-authentication.md) — Magic Links, OAuth2, and API Tokens.
19. [Sessions](19-sessions.md) — Managing persistent user data.
20. [Security Headers](20-security-headers.md) — Production hardening (CSP, HSTS, etc.).
21. [CORS & Gzip](21-cors-gzip.md) — Cross-origin requests and compression.
22. [Rate Limit](22-rate-limit.md) — Protecting your app from brute-force/abuse.
23. [Security Audit](23-security-audit.md) — Current state of framework hardening.

## ✨ Reactive UI
24. [Reactive Components](24-reactive-components.md) — Stateful WebSocket-powered UI.
25. [Transitions](25-transitions.md) — Animations for your UI.
26. [HTML Streaming](26-html-streaming.md) — Optimizing TTFB with chunked delivery.
27. [Scoped JS & CSS](27-scoped-assets.md) — Page-specific, isolated assets.
28. [Intelligent Prefetching](28-intelligent-prefetching.md) — Fast navigation.
29. [Asok Directives](29-asok-directives.md) — Client-side reactivity helpers.

## 🛠️ Internal Tools
30. [Admin Interface](30-admin-interface.md) — 2FA, Roles, Impersonation & Media.
31. [API Development](31-api-development.md) — Building JSON APIs with auto-docs.
32. [WebSockets](32-websockets.md) — Real-time bidirectional communication.
33. [Email Service](33-email-service.md) — Sending SMTP emails in the background.
34. [Caching](34-caching.md) — Performance boost with memory/file caching.
35. [Background Tasks](35-background-tasks.md) — Non-blocking function execution.
36. [Scheduled Tasks](36-scheduler.md) — Recurring cron-like jobs.

## 🚀 Operations & Tools
37. [Internationalization](37-internationalization.md) — Multi-language support (i18n).
38. [CLI Reference](38-cli-reference.md) — All `asok` command-line tools.
39. [Deployment](39-deployment.md) — Production setup (Gunicorn, Nginx, SystemD).
40. [Testing](40-testing.md) — Unit and integration testing with TestClient.
41. [Logging](41-logging.md) — Request and application logs.
42. [Optimization](42-optimization.md) — Minification, WebP, and performance tips.
43. [Static Versioning](43-static-versioning.md) — Cache busting for static assets.
44. [Production Build](44-production-build.md) — Packaging and production distribution.
45. [Data Tables](45-data-tables.md) — Interactive tables.
46. [Developer Toolbar](46-developer-toolbar.md) — Real-time SQL profiler, AJAX/SPA support, and reactive state inspector.

## 📚 References & Advanced
47. [Utilities](47-utilities.md) — Humanize, Minifiers, and Helpers.
48. [Component API](48-component-api.md) — Full reference for Live Components.
49. [SEO Management](49-seo-management.md) — Titles, Meta tags, and Social sharing.
50. [Tailwind CSS](50-tailwind-css.md) — Integrating and customizing Tailwind.
51. [Async Concurrency](51-async-concurrency.md) — Dual ASGI/WSGI and async controller/ORM support.
52. [Request Context](52-request-context.md) — `current_request` proxy: access the active request from anywhere.
53. [SSG & ISR](53-ssg-isr.md) — Static Site Generation and Incremental Static Regeneration.
54. [Extension System](54-extension-system.md) — Reusable packages: custom routes, template directories, assets, and CLI commands.
