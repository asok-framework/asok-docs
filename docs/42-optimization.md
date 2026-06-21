# Optimization

> **Keywords:** minify css, webp optimization, performance tips, assets optimization, compression

Asok includes a built-in optimization engine for production builds.

### Build-Time Optimization
While Asok can minify HTML at runtime during development, the recommended approach for production is to use the `asok build` command. This performs a one-shot minification of all your templates so the production server can skip this processing.

## 2. Image Optimization (WebP)

Asok can automatically convert your images to the modern **WebP** format.

### How it works
- **On-the-fly serving**: The `static()` helper automatically redirects to the `.webp` version if it exists.
- **Auto-Conversion**: Images uploaded via the Admin are automatically optimized.
- **Standalone Binary**: Uses Google's `cwebp` binary (downloaded into `.asok/bin/`).

### Naming Convention & Rationale (Double Extension)

When an image like `photo.png` is optimized, Asok saves it with a double extension (e.g., `photo.png.webp`). This specific design choice provides several key benefits:
- **Collision Prevention**: If a directory contains both `avatar.png` and `avatar.jpg`, compiling both simply to `avatar.webp` would result in a naming conflict. Retaining the original extension (producing `avatar.png.webp` and `avatar.jpg.webp`) ensures each optimized file remains unique.
- **Source Format Traceability**: The framework can instantly identify the original image format from the filename alone. This is essential for serving the original file as a fallback to older clients that do not support WebP, or when `IMAGE_KEEP_ORIGINAL=true` is enabled.
- **Stateless Mapping**: It avoids the need for an external database or metadata mapping file to link an optimized asset back to its source file.

### Quick Start
Enable it during project creation:
```bash
asok create myapp --image
```

Or add it later:
```bash
asok image --enable
```

### Full Scan
Optimize all existing images in your project:
```bash
asok image --optimize
```

To clean up disk space by removing original files after conversion:
```bash
asok image --optimize --delete-originals
```

### Automatic File cleanup
In production, you can tell Asok to delete original assets right after they are converted during upload:
```env
IMAGE_KEEP_ORIGINAL=false
```

## 3. JS & CSS Minification (Esbuild)

Asok uses the official standalone **Esbuild** binary to provide ultra-fast minification for your JavaScript and CSS files located in `src/partials/`.

### How it works
- **Performance**: Esbuild is written in Go and is significantly faster than Node-based tools.
- **Auto-serving**: In production (`DEBUG=false`), the `static()` helper automatically redirects to the `.min.js` or `.min.css` version if it exists.
- **Standalone Binary**: Downloads into `.asok/bin/` with no Node.js required.

### Quick Start
Install the binary:
```bash
asok assets --install
```

### Manual Minification
```bash
asok assets --minify
```

### Automatic Build
The `asok preview` command automatically runs a minification pass before starting the production server, ensuring all your assets are optimized.

## 4. Tailwind CSS Minification

If you use Tailwind CSS, Asok uses the official standalone binary to minify your CSS during production builds.

```bash
asok preview
#   Building CSS (minified)...
```

This runs a one-shot minified build of your `src/partials/css/base.css` into `base.build.css`.

## 5. Gzip Compression

Asok includes a built-in Gzip middleware to compress HTML, CSS, JS, and JSON responses.

### Configuration
```env
GZIP=true
GZIP_MIN_SIZE=500  # Minimum size in bytes to trigger compression
```

## 6. Smart Conditional Asset Injection

Asok automatically reduces the JavaScript and CSS payload of your pages by only loading the reactive engines and widget-specific assets when they are actually needed.

### How it works
- **Scan**: During the final rendering phase, Asok performs a lightning-fast scan of your HTML content.
- **Triggers**: It looks for specific attributes like `data-block`, `data-sse`, `ws-*`, or `data-asok-component`.
- **Injection**: 
  - The **Reactive Engine** is only injected if `data-*` attributes are found.
  - The **Alive Engine** (WebSockets) is only injected if `ws-*` or component attributes are found.
- **Result**: Static pages remain purely static with zero JavaScript overhead, while reactive pages maintain full functionality automatically.

### Directives & Widgets Code-Splitting
To keep reactive pages as lightweight as possible, Asok splits the assets of the reactive directives runtime:
- **Core Directives Engine** (`asok_directives.min.js` and `asok_directives.min.css`): Contains only the core reactivity runtime and minimal directive-specific styling (like `asok-cloak`).
- **Form Helper Widgets** (`asok_widgets.min.js` and `asok_widgets.min.css`): Contains all functions and styles for advanced form widgets (signatures, file dropzones, autocompletes, multi-select tags, tree items, toggles, tables, etc.).
- **Conditional Loading**: The form widgets bundle (both JS and CSS) is dynamically injected only if any helper function (e.g. `Asok.`) or specific widget class/tag (e.g. `asok-dropdown`, `asok-table`, `asok-toggle`, `asok-badge`, `asok-pagination`) is detected in the page content. This ensures pages using simple reactive directives do not download the larger widgets bundle.

## 7. Scoped Assets (Page-specific Optimization)

Asok allows you to reduce your global CSS and JS payload by isolating page-specific logic and styles.

### How it works
- **Granular Loading**: Assets are only loaded for the specific page that needs them.
- **Inlining**: Scoped assets are inlined directly into the HTML response, reducing the number of HTTP requests and improving Time to First Meaningful Paint.
- **Isolation**: Prevents side-effects and style leakage, ensuring that optimizations on one page don't break others.

See the [Scoped Assets Guide](27-scoped-assets.md) for detailed usage.

## 8. Production Bytecode (.pyc)

While Asok disables bytecode generation during development to keep your project structure clean, it leverages full bytecode compilation for production deployments via the `asok build` system.

### How it works
- **Pre-compilation**: The `asok build` command compiles all `.py` files into optimized `.pyc` files (using `optimize=2`).
- **Source Protection**: Original `.py` files are removed by default in the `dist/` folder, creating a locked distribution.
- **Fast Execution**: Pre-compiled bytecode allows for faster module loading and slightly improved runtime performance.
- **Stealth Mode**: By running entirely from bytecode, your production environment remains clean and free of source code.

### Configuration
If you specifically need to enable bytecode generation (e.g. for mission-critical performance in production), set the following environment variable:

```bash
ASOK_WRITE_BYTECODE=true
```

## Deployment (Production)

Don't forget to install the required binaries on your production server:

```bash
asok image --install
asok tailwind --install
```

---
[← Previous: Logging](41-logging.md) | [Documentation](README.md) | [Next: Static Versioning →](43-static-versioning.md)
