# Security Audit

> **Keywords:** security report, vulnerability audit, security hardening, audit log, security features

Asok includes built-in security measures. This document summarizes the protections integrated into the framework to help protect applications from common web vulnerabilities.

## Executive Summary

Asok includes modern security protections by default. In most cases, you do not need to write security-specific code to get baseline protection against SQL injection, XSS, CSRF, and related issues.

---

## 1. Protection Against Injections

### SQL Injection
The Asok ORM uses **parameterized queries** for all data interactions. User input is never concatenated directly into SQL strings.
- All `Query` methods (`where`, `where_in`, etc.) use `?` placeholders.
- Column names are strictly validated against model metadata.

### Cross-Site Scripting (XSS)
The Asok template engine implements **automatic HTML escaping** by default.
- Any variable rendered via `{{ user_input }}` is escaped (e.g., `<` becomes `&lt;`).
- To render raw HTML, you must explicitly use the `|safe` filter or the `SafeString` class.

---

## 2. Broken Access Control

### CSRF Protection
Asok uses the **Double Submit Cookie** pattern to prevent Cross-Site Request Forgery.
- All state-changing requests (POST, PUT, DELETE) must include a `csrf_token`.
- The token is verified against an `HttpOnly` cookie.
- Use `{{ request.csrf_input() }}` in your forms to automatically include the token.

### Mass Assignment
The ORM protects sensitive fields from being updated in bulk from user input.
- Fields marked as `protected` in your Model are ignored by `Model.create()` and `Model.update()` unless the `_trust=True` flag is passed.

---

## 3. Authentication & Sessions

### Password Storage
Asok uses **PBKDF2-SHA256** with 600,000 iterations for password hashing. This is handled automatically by `Field.Password()`.

### Session Security
- **Secure IDs**: Session identifiers are 32-byte cryptographically strong hex strings (`secrets.token_urlsafe(32)`).
- **Cookie Security**:
  - Session cookies are `HttpOnly` and `SameSite=Strict` by default
  - `Secure` flag added automatically on HTTPS
  - CSRF cookies also use `HttpOnly` and `SameSite=Strict` for maximum protection
- **HMAC Signing**: Session IDs are signed with HMAC to prevent tampering
- **Rotation**: IDs can be rotated using `session.regenerate()` to prevent session fixation
- **CSRF Token Rotation**: CSRF tokens are automatically rotated after successful validation to prevent token reuse attacks

---

## 4. File and URL Safety

### File Upload Validation ⭐ NEW in v0.1.6

Asok provides **automatic MIME type validation** using magic bytes detection to prevent malicious file uploads:

- **Magic Bytes Detection**: Files are validated by their actual content (first bytes), not just extension
- **50+ Formats Supported**: Images (JPEG, PNG, GIF, WebP, BMP, TIFF, SVG), Audio (MP3, WAV, FLAC, OGG, AAC), Video (MP4, WebM, MKV, AVI, MOV), Documents (PDF, ZIP, Office files)
- **Extension Matching**: File extension must match the detected MIME type
- **Whitelist Enforcement**: `allowed_types` parameter enforces strict MIME type whitelist
- **Secure Filenames**: Files are renamed with UUID by default (`secure_filename=True`)
- **Restrictive Permissions**: Saved files get `0o644` (rw-r--r--) permissions
- **Security Warnings**: Logs warning if validation is disabled or no whitelist specified

```python
# Secure file upload with validation
photo.save("uploads/", allowed_types=['image/jpeg', 'image/png'])
```

See [File Storage](16-file-storage.md#mime-type-validation) for complete documentation.

### Path Traversal
The `secure_filename()` utility is used automatically during file uploads to remove directory separators and illegal characters, ensuring files cannot be saved outside the intended directory.

**Enhanced in v0.1.6**:
- Uses `pathlib.Path.resolve(strict=True)` for robust path resolution
- Validates all parent directories for symlinks
- Only accepts filename (basename) to prevent any path traversal
- Returns `403 Forbidden` on escape attempts

### Open Redirects
The `request.redirect()` method uses `is_safe_url()` to block redirects to external domains or malformed URLs that could be used for phishing.

---

## 5. Security Headers

Asok automatically injects a set of "best-practice" security headers into every HTTP response:

| Header | Value | Purpose |
|---|---|---|
| `X-Content-Type-Options` | `nosniff` | Prevents MIME-sniffing |
| `X-Frame-Options` | `DENY` | Prevents Clickjacking |
| `X-XSS-Protection` | `1; mode=block` | Enables browser XSS filters |
| `Strict-Transport-Security` | `max-age=31536000` | Enforces HTTPS |
| `Referrer-Policy` | `strict-origin...` | Protects privacy |

---

## 6. Content Security Policy (CSP)

Asok provides built-in support for **Nonces**. You can access a unique cryptographic nonce for the current request via `request.nonce`.

```html
<script nonce="{{ request.nonce }}">
  // This inline script is authorized by the CSP
</script>
```

---

## 7. Security Audit Results (v0.3.0)

The following notes summarize the main security mechanisms currently implemented in Asok v0.3.0:

### SQL Injection Protection ✅

- **Parameterized Queries**: All ORM queries use `?` placeholders with separate arguments array.
- **Strict Column Validation**: `_valid_column()` strictly validates all column names against model metadata, preventing injection in non-parameterizable clauses.
- **Operator Whitelist**: SQL operators are validated against a strict `_OPERATORS` whitelist.

### XSS Protection ✅

- **Auto-Escaping**: All template variables are automatically escaped via `_escape()`.
- **UI Attribute Escaping**: The centralized `_render_attrs` utility ensures all HTML attributes (including nested ones like `dropdown__class`) are properly escaped.
- **SafeString Class**: Explicit opt-in required for raw HTML via `SafeString` class or `|safe` filter.

### CSRF Protection ✅

- **Cryptographic Tokens**: 32-byte random tokens via `secrets.token_hex(32)`.
- **HMAC Validation**: Token comparison uses `hmac.compare_digest()` to prevent timing attacks.
- **Strict Origin Verification**: For HTTPS requests, both `Origin` and `Referer` headers are validated against the host to prevent cross-origin state changes.
- **SameSite Cookies**: CSRF cookies use `SameSite=Strict` for maximum protection.

### Server-Side Template Injection (SSTI) Protection ✅

- **Restricted Execution**: Templates are executed in a restricted namespace with `__builtins__` blocked.
- **Sandbox Escape Prevention**: Access to dangerous Python attributes (`__class__`, `__globals__`, `__subclasses__`, etc.) is strictly blocked.
- **Safe Attribute Whitelist**: Only a specific set of safe underscore attributes (like `_table` or `_fields` for internal needs) are accessible.

### Path Traversal Protection ✅

- **Absolute Path Validation**: Uses `os.path.abspath()` with `startswith()` checks
- **Symlink Protection**: Uses `os.path.realpath()` and `os.path.islink()` to prevent symlink traversal attacks
- **Safe Resolve Function**: `_safe_resolve()` utility ensures paths stay within allowed directories
- **403 on Escape Attempts**: Returns 403 Forbidden if path traversal is detected
- **Static File Validation**: All static file serving validates paths before reading

### Password Security ✅

- **PBKDF2-SHA256**: Industry-standard password hashing algorithm
- **High Iteration Count**: 600,000 iterations (OWASP 2023 compliant)
- **Random Salt**: Each password gets a unique 16-byte random salt
- **Secure Format**: Stored as `pbkdf2:sha256:600000$salt$hash`

### Session & Cookie Security ✅

- **HttpOnly Flag**: All sensitive cookies (session, CSRF, flash) have HttpOnly
- **Secure Flag**: Automatically added for HTTPS connections
- **SameSite=Strict**: Session and CSRF cookies use Strict for best protection
- **SameSite=Lax**: Non-sensitive cookies (language) use Lax appropriately
- **HMAC Signing**: Session IDs are signed to prevent tampering
- **Secure RNG**: Uses `secrets` module for cryptographically secure random generation.

### Data Encryption (GDPR / PCI-DSS) ✅

Asok provides a native `Field.EncryptedString()` for storing sensitive data (SSNs, credit card numbers, phone numbers, API keys) transparently encrypted in the database.

- **Algorithm**: AES-256 via the `cryptography` package's Fernet engine (authenticated encryption — also protects integrity).
- **Key Derivation**: The encryption key is derived from the application's `SECRET_KEY` using SHA-256, then base64url-encoded to produce a valid 32-byte Fernet key.
- **Transparent**: Values are automatically encrypted on `save()` and decrypted on `__init__()` (when loading from the DB). Application code always sees plaintext.
- **Graceful Degradation**: If decryption fails (e.g., key rotation or mismatch), the method returns the raw ciphertext instead of crashing, and logs an error for investigation.
- **Non-queryable by design**: Fernet tokens are non-deterministic (ciphertext differs each time), so direct database queries or indexes on encrypted columns are not possible — by design.

```python
from asok import Model, Field

class Customer(Model):
    name = Field.String()
    ssn  = Field.EncryptedString()   # Encrypted transparently

c = Customer.create(name="Alice", ssn="123-45-6789")
print(c.ssn)  # "123-45-6789" — plaintext in Python
# In the DB: "gAAAAAB..." — Fernet ciphertext
```

> [!IMPORTANT]
> The `cryptography` library must be installed: `pip install "asok[security]"`

### Zero-Eval Content Security Policy ✅

- **Least Privilege Principle**: Asok implements a Content Security Policy that completely disables `'unsafe-eval'` by default in production.
- **Zero-Eval Reactive Architecture**: Thanks to server-side precompilation of reactive expressions and dynamic registry injection via cryptographically nonced script elements, the browser never uses `eval()` or `new Function()`.
- **Granular Control**: Developers can still force `'unsafe-eval'` if they use third-party libraries requiring it via `CSP_UNSAFE_EVAL`.

### Command Injection Protection ✅

- **No Runtime Execution**: No `os.system()`, `eval()`, or `exec()` in runtime code
- **Subprocess Limited**: `subprocess` only used in CLI tools and secure background optimization, never directly exposed to request routing.
- **Subprocess Confinement**: The image optimizer utility in `asok/utils/image.py` strictly restricts binary execution pathways inside the `.asok/bin` subdirectory using `os.path.commonpath` checks, preventing path traversal or execution of unauthorized binaries.
- **No Dynamic Code**: No dynamic code execution from user input

### Log Injection Protection ✅

- **Newline Sanitization**: `\n` and `\r` characters removed from logged request data
- **Structured Logging**: JSON format option for production with proper escaping
- **Limited Debug Info**: Debug logs never expose sensitive session data or passwords

### Validation & Input Handling ✅

- **Type Validation**: Strong type checking via `Field` types
- **Email Validation**: RFC-compliant email validation
- **URL Validation**: Validates URL format and scheme
- **HTML Sanitization**: Optional bleach integration for HTML whitelisting

### Security Summary

| Vulnerability Class | Protection Status |
|---------------------|-------------------|
| SQL Injection | ✅ Protected |
| XSS | ✅ Protected |
| CSRF | ✅ Protected |
| Path Traversal | ✅ Protected |
| Authentication | ✅ Hardened |
| Session Management | ✅ Hardened |
| Encrypted Fields (GDPR/PCI-DSS) | ✅ `EncryptedString` — AES-256 Fernet, key derived from `SECRET_KEY` |
| Command Injection | ✅ No direct runtime exposure |
| Log Injection | ✅ Protected |
| Input Validation | ✅ Comprehensive |

### Conclusion

Asok provides secure defaults and layered defenses against common web vulnerabilities. As with any framework, applications still need sensible configuration, safe templates, and careful access control.

---
[← Previous: Rate Limit](22-rate-limit.md) | [Documentation](README.md) | [Next: Reactive Components →](24-reactive-components.md)
