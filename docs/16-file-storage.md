# File Storage

## UploadedFile

Multipart file uploads are parsed into `UploadedFile` objects available on `request.files`.

```python
from asok import Request

def render(request: Request):
    photo = request.files.get("photo")
    if photo:
        print(photo.filename)  # "avatar.jpg"
        print(photo.size)      # 102400
        saved = photo.save("avatar.jpg")
        # Returns actual path (may differ if conflict)
```

### Properties

| Property | Type | Description |
|---|---|---|
| `filename` | `str` | Original upload filename |
| `content` | `bytes` | Raw file content |
| `size` | `int` | File size in bytes |

### `save(destination)`

Saves the file to disk. By default, relative paths are resolved relative to **`src/partials/uploads/`**.

```python
photo.save("avatar.jpg")        # saves to src/partials/uploads/avatar.jpg
photo.save("imgs/avatar.png")   # saves to src/partials/uploads/imgs/avatar.png
```

Features:
- Auto-creates parent directories
- Handles name conflicts: `photo.jpg` → `photo_1.jpg` → `photo_2.jpg`
- Returns the actual saved absolute path

## MIME Type Validation ⭐ NEW in v0.1.6

Asok provides **automatic MIME type validation** using magic bytes detection to prevent malicious file uploads. This security feature validates files based on their actual content, not just their extension.

### Basic Usage

```python
from asok import Request

def render(request: Request):
    photo = request.files.get("photo")
    if photo:
        try:
            # Validate and save - only allow images
            photo.save("uploads/", allowed_types=['image/jpeg', 'image/png'])
        except ValueError as e:
            return f"Error: {e}"
```

### Validation Parameters

The `save()` method accepts these validation parameters:

```python
photo.save(
    destination="uploads/",
    validate=True,  # Enable MIME validation (default: True)
    allowed_types=['image/jpeg', 'image/png'],  # Whitelist of MIME types
    secure_filename=True  # Rename with UUID (default: True)
)
```

**Parameters**:
- `validate` (bool): Enable/disable validation. Default: `True`
- `allowed_types` (list): Whitelist of allowed MIME types. If `None`, accepts all validated types (⚠️ warning logged)
- `secure_filename` (bool): Rename file with UUID for security. Default: `True`

### Supported File Types (50+ formats)

Asok validates files using **magic bytes** (file signatures) for accuracy:

#### 🖼️ Images (11 formats)
```python
allowed_types = [
    'image/jpeg',      # .jpg, .jpeg
    'image/png',       # .png
    'image/gif',       # .gif
    'image/webp',      # .webp (modern format)
    'image/bmp',       # .bmp
    'image/tiff',      # .tif, .tiff
    'image/x-icon',    # .ico
    'image/svg+xml',   # .svg (vector)
]
```

#### 🎵 Audio (8 formats)
```python
allowed_types = [
    'audio/mpeg',      # .mp3
    'audio/wav',       # .wav
    'audio/flac',      # .flac (lossless)
    'audio/ogg',       # .ogg, .oga
    'audio/aac',       # .aac
    'audio/mp4',       # .m4a
]
```

#### 🎬 Video (6 formats)
```python
allowed_types = [
    'video/mp4',       # .mp4 (H.264)
    'video/webm',      # .webm (VP8/VP9)
    'video/x-matroska',# .mkv
    'video/avi',       # .avi
    'video/quicktime', # .mov
    'video/3gpp',      # .3gp (mobile)
]
```

#### 📄 Documents & Archives
```python
allowed_types = [
    'application/pdf',              # .pdf
    'application/zip',              # .zip, .docx, .xlsx, .pptx
    'application/msword',           # .doc, .xls, .ppt (legacy)
    'text/rtf',                     # .rtf
    'application/gzip',             # .gz
    'application/x-bzip2',          # .bz2
    'application/x-rar-compressed', # .rar
    'application/x-7z-compressed',  # .7z
]
```

### Advanced Validation

#### Standalone Validation

You can validate files without saving:

```python
photo = request.files.get("photo")
try:
    photo.validate_mime_type(allowed_types=['image/jpeg', 'image/png'])
    print("✅ File is valid")
except ValueError as e:
    print(f"❌ Invalid file: {e}")
```

#### Multiple File Types

```python
# Accept images and PDFs
allowed = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf']
document.save("docs/", allowed_types=allowed)
```

#### Media Gallery

```python
# Accept all images, audio, and video
allowed = [
    'image/jpeg', 'image/png', 'image/gif', 'image/webp',
    'audio/mpeg', 'audio/wav',
    'video/mp4', 'video/webm'
]
media.save("gallery/", allowed_types=allowed)
```

### Security Features

1. **Magic Bytes Detection**: Files are validated by their actual content, not extension
   ```python
   # A .jpg renamed to .txt will still be detected as image/jpeg
   ```

2. **Extension Matching**: File extension must match the detected MIME type
   ```python
   # A PNG file with .jpg extension will be rejected
   ```

3. **Secure Filenames**: Files are renamed with UUID by default
   ```python
   photo.save("uploads/")  # → uploads/a3f2b9c1-4567-89ab-cdef.jpg
   ```

4. **Restrictive Permissions**: Saved files get `0o644` (rw-r--r--) permissions

5. **Security Warnings**: Logs warning if `allowed_types` not specified
   ```python
   # ⚠️ Generates security warning
   photo.save("uploads/")  # No allowed_types!

   # ✅ Recommended
   photo.save("uploads/", allowed_types=['image/jpeg'])
   ```

### Error Handling

```python
from asok import Request

def render(request: Request):
    photo = request.files.get("photo")
    if not photo:
        return "No file uploaded"

    try:
        path = photo.save(
            "avatars/",
            allowed_types=['image/jpeg', 'image/png', 'image/webp']
        )
        return f"✅ File saved: {path}"

    except ValueError as e:
        # Handle validation errors
        if "not allowed" in str(e):
            return "Only JPEG, PNG, and WebP images are allowed"
        elif "does not match" in str(e):
            return "File extension doesn't match file type"
        else:
            return f"Validation error: {e}"
```

### Best Practices

✅ **DO**:
- Always specify `allowed_types` for security
- Use the most restrictive whitelist possible
- Keep `validate=True` (default)
- Use `secure_filename=True` for public uploads

```python
# ✅ Secure upload
avatar.save("avatars/", allowed_types=['image/jpeg', 'image/png'])
```

❌ **DON'T**:
- Don't disable validation (`validate=False`)
- Don't allow all types without restriction
- Don't trust file extensions alone

```python
# ❌ Insecure - accepts any file!
file.save("uploads/", validate=False)

# ⚠️ Less secure - accepts any valid type
file.save("uploads/")  # allowed_types=None
```

### Performance Notes

- Validation reads only the first **few bytes** of each file (magic bytes)
- Minimal performance impact even for large files
- Files are validated **before** writing to disk

### Accessing files

`request.files` is a dictionary of `UploadedFile` objects. You can access them using bracket notation or `.get()` (safest):

```python
# Safest: returns None if missing
photo = request.files.get("photo")

# Alternative: raises KeyError if missing
photo = request.files["photo"]

# Accessing properties (preferred)
print(photo.filename)

# Dict-style access (backward compatibility)
print(request.files["photo"]["filename"])
```

## Serving Files

Use `request.send_file()` to return a file to the browser. Relative paths are automatically resolved relative to **`src/partials/uploads/`**.

```python
from asok import Request

def render(request: Request):
    # Resolves to src/partials/uploads/report.pdf
    return request.send_file("report.pdf")

    # Resolves to src/partials/uploads/pdf/cv.pdf
    return request.send_file("pdf/cv.pdf")

    # Force download with custom name
    return request.send_file("data.csv", filename="export.csv")

    # Display image in browser (inline)
    return request.send_file("header.png", as_attachment=False)
```

### Path Resolution
- **Absolute paths**: Used as-is.
- **Relative paths**: Resolved relative to `src/partials/uploads`.

> For security, `request.send_file()` only allows serving files from within the `src/partials/uploads` directory. Attempts to access files outside this directory will return a `403 Forbidden` error.

## Configuration

You can limit the maximum upload size globally in your `Asok` app configuration:

```python
# wsgi.py
app = Asok()
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB limit
```

Default is **10 MB**. If a request exceeds this limit, Asok returns a `413 Payload Too Large` error.

---
[← Previous: Serialization (Schema)](15-serialization.md) | [Documentation](README.md) | [Next: Authentication →](17-authentication.md)
