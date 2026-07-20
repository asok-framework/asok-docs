# Static Versioning

> **Keywords:** cache busting, static assets hash, assets versioning, version query param

In production, `static()` appends a content hash to static URLs for cache busting.

## Usage

In templates:

```html
<link rel="stylesheet" href="{{ static('css/app.css') }}">
```

**Development** output: `/css/app.css`

**Production** output: `/css/app.css?v=a1b2c3d4`

The hash is the first 8 characters of the file's MD5 digest. It's computed once and cached for the lifetime of the process.

The query string (`?v=...`) is ignored by the static file server since it uses `PATH_INFO`, not `QUERY_STRING`.

## S3 / CDN Cloud Serving ⭐ NEW in v0.1.7

If you want to host your static assets on S3 or a CDN in production, Asok can automatically rewrite your static URLs.

1. Configure your S3 storage backend in `.env` (see [File Storage](../user-guide/16-file-storage.md) for details).
2. Enable static S3 serving:
```bash
ASOK_SERVE_STATIC_FROM_S3=true
```

When enabled, the `static()` helper prefixes URLs with your S3 bucket or CDN domain:
* **Without custom domain**: `https://my-bucket.s3.us-east-1.amazonaws.com/css/app.css?v=a1b2c3d4`
* **With custom CDN domain**: `https://cdn.myapp.com/css/app.css?v=a1b2c3d4`
