# Deployment

Asok is designed to be straightforward to deploy. The framework focuses on a documented production stack using **Gunicorn**, **Nginx**, and **SystemD**.

## 1. Automated Deployment

The `asok deploy` command automates the generation of a production stack.

### Workflow

Run the command in your project root:
```bash
asok deploy
```

Asok will generate a `deployment/` directory containing:
- `gunicorn_conf.py`: Optimized worker settings based on your server's CPU.
- `nginx.conf`: Nginx reverse-proxy with **Gzip compression** and **Security headers**.
- `myapp.service`: SystemD unit file configured with your current `SECRET_KEY`.
- `setup.sh`: A comprehensive installation script for Ubuntu/Debian.

## 2. Build Pipeline (Recommended)

Before deploying, it is recommended to generate an optimized distribution of your project using the Asok build engine. This will minify your assets, compile your Python source to bytecode, and optimize images when the relevant features are enabled.

```bash
asok build
```

This command generates a `dist/` folder. You should deploy the **contents** of this folder to your production server instead of your raw source code. 

> **Migrations in Build**: By default, `asok build` preserves your `src/migrations/` directory as source code (`.py`) even if you don't use `--keep-source`. This allows you to run `asok migrate` on your production server to keep your database in sync.

## 3. Server Setup (Ubuntu/Debian)

1. **Upload**: Copy your project (including the `deployment/` folder) to your server (e.g., via `scp` or `git clone`).
2. **Execute**: Run the setup script as root:
   ```bash
   sudo ./deployment/setup.sh
   ```

### What the script does:
- Installs `nginx`, `python3-pip`, and `python3-venv`.
- Creates a virtual environment and installs `gunicorn`.
## 4. Directory Permissions

For the `file` backend to work correctly, the directories used for sessions and caching must be writable by the user running the web server (Gunicorn).

### Recommended Permissions Table

| Directory / File | Default Path | Purpose | Rec. Permissions | Rec. Owner |
|---|---|---|---|---|
| **Sessions** | `.asok/sessions/` | User session storage | `775` | `www-data` |
| **Cache** | `.asok/cache/` | Fragment/ORM caching | `775` | `www-data` |
| **Database** | `db.sqlite3` | SQLite database file | `664` | `www-data` |
| **Database Dir** | `./` (Project root) | SQLite WAL/SHM files | `775` | `www-data` |
| **Uploads** | `src/partials/uploads/` | User-uploaded files | `775` | `www-data` |

### Setup Commands (Ubuntu/Debian)

If you are running Gunicorn as the `www-data` user (the default on Ubuntu), you must grant it ownership of the state directories:

```bash
# Ensure directories exist
mkdir -p .asok/sessions .asok/cache src/partials/uploads

# Give ownership to the web server user
sudo chown -R www-data:www-data .asok/sessions .asok/cache src/partials/uploads

# Important: SQLite needs write access to the DIRECTORY containing the DB
# to create temporary WAL (Write-Ahead Log) files.
sudo chown www-data:www-data .
sudo chmod 775 .

# Set permissions (Owner: Read/Write/Exec, Group: Read/Exec)
sudo chmod -R 775 .asok/sessions .asok/cache src/partials/uploads

# Secure the database file
if [ -f "db.sqlite3" ]; then
    sudo chown www-data:www-data db.sqlite3
    sudo chmod 664 db.sqlite3
fi
```

### Security Note
Asok's `file` backend automatically sets `0600` permissions (read/write for owner only) on the individual session and cache files it creates. This ensures that even if another user on the system has access to the directory, they cannot read the sensitive contents of your sessions.

## 5. RHEL / AlmaLinux (SELinux)

Deploying on RHEL-based systems like **AlmaLinux** or **Rocky Linux** requires handling **SELinux** (Security-Enhanced Linux). If your app fails to write sessions or cache, you will likely see `PermissionError: [Errno 13] Permission denied` in your logs.

### The Problem: init_t vs httpd_sys_rw_content_t
By default, Gunicorn runs in the `init_t` domain. Even if you set your folder to `httpd_sys_rw_content_t`, the system may block the write operations.

### RuntimeDirectory Solution
Instead of using manual SELinux labels, use the SystemD `RuntimeDirectory` setting to handle ephemeral state. This grants the required permissions and SELinux contexts.

1. **Update your `.service` file**:
```ini
[Service]
RuntimeDirectory=asok
RuntimeDirectoryMode=0775
```

2. **Update your `wsgi.py`**:
```python
# Use the auto-generated systemd path
SESSION_DIR = "/run/asok/sessions"
app._session_store = SessionStore(backend="file", path=SESSION_DIR)
```

### Alternative: Custom SELinux Policy
If you must use a directory inside `/var/www`, you can generate a custom policy from the audit logs:
```bash
sudo ausearch -m avc -ts recent | audit2allow -M asok_fix
sudo semodule -i asok_fix.pp
```

---
[← Previous: CLI Reference](38-cli-reference.md) | [Documentation](README.md) | [Next: Testing →](40-testing.md)
