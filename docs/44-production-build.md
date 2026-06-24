# Production Build System

> **Keywords:** production bundle, compile static assets, packaging, asset build

Asok provides a build pipeline for generating optimized distributions for production environments. The `asok build` command handles asset minification and bytecode compilation.

## The `asok build` Command

To generate a production distribution of your project, run:

```bash
asok build
```

This command creates a new directory (default: `dist/`) containing an optimized version of your project.

### What happens during the build?

1.  **Cloning**: The project structure is replicated into the output directory, excluding development artifacts like `venv`, `.git`, or `.asok`.
2.  **Asset Minification**: All JS and CSS files within `src/partials` are recursively minified using `esbuild`.
3.  **HTML Optimization**: Templates are minified to remove unnecessary whitespace and comments, significantly reducing TTFB.
4.  **Bytecode Compilation**: All Python source files are compiled into `.pyc` files. By default, the original `.py` files are removed from the build output.
5.  **Image Optimization**: If `IMAGE_OPTIMIZATION=true` is set, all project images are converted to WebP and originals are removed.
6.  **Migration Preservation**: The `src/migrations` directory is kept as source code (`.py`) to allow database synchronization in production.
7.  **Production Config**: A `.env.production` file is generated with `DEBUG=false` and security defaults.

## Production Migration Workflow

For maximum safety, you should follow a strict migration lifecycle:

1.  **Generate in Dev**: Run `asok make migration` on your development machine.
2.  **Ship in Build**: Run `asok build` to include these migrations in your distribution.
3.  **Apply in Prod**: Run `asok migrate` on your production server.

> **Do not run `asok make migration` in production.** Your distribution should be considered immutable; migrations should be authored in development and deployed as part of your release.

## Command Options

| Option | Description | Default |
| :--- | :--- | :--- |
| `--output`, `-o` | Specify the output directory name. | `dist` |
| `--keep-source` | Keep original `.py` files alongside `.pyc` files. | `False` |
| `--with-db` | Include the current `db.sqlite3` in the build. | `False` |

> **Portfolio Tip**: Use `--with-db` if you want to ship a pre-populated database (e.g., for a portfolio) without running an admin or seeders in production.

### Note on `.gitignore`
During the build, Asok automatically **removes** your development `.gitignore` from the `dist/` folder. This prevents built assets (like `base.build.css`) from being accidentally ignored if you use Git-based deployment for your distribution.

## Deployment Workflow

Once the build is complete, your `dist/` folder is ready for deployment. You can preview it locally using:

```bash
cd dist
asok preview
```

> The `asok preview` command in the build folder correctly identifies `wsgi.pyc` as the entry point. In production environments (Gunicorn/Uvicorn), you should point your WSGI server to `wsgi:app`.

## Performance Benefits

By using `asok build`, you gain several performance advantages:

- **Zero Runtime Minification**: In production mode (`DEBUG=false`), Asok detects that templates are already optimized and skips on-the-fly minification, saving CPU cycles.
- **Fast Startup**: Bytecode compilation (`.pyc`) allows the Python interpreter to load modules faster.
- **Optimized Assets**: Small JS/CSS bundles and WebP images ensure faster page loads and lower bandwidth usage.
- **Security**: Shipping bytecode instead of source code reduces exposure of application source files.

## Requirements

The build system requires `esbuild` for asset minification. If not present, run:

```bash
asok assets --install
```

---
[← Previous: Static Versioning](43-static-versioning.md) | [Documentation](README.md) | [Next: Data Tables →](45-data-tables.md)
