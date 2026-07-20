# Deployment

> **Keywords:** gunicorn config, nginx config, systemd service, deploy production, reverse proxy, ssl tls deployment

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
- `myapp.service`: SystemD unit file for the main Gunicorn web server, configured with your current `SECRET_KEY`.
- `myapp-worker.service`: SystemD unit file for the background task worker (`asok worker`) in Redis queue mode.
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
- Installs `nginx`, `python3-pip`, `python3-venv`, and `redis-server`.
- Configures, starts, and enables the local Redis service.
- Creates a Python virtual environment and installs `gunicorn`, `asok`, and `redis`.
- Installs project dependencies from `requirements.txt`.
- Sets correct permissions for the `www-data` user on the database and uploads directory.
- Copies both SystemD service files (`.service` and `-worker.service`) to the system directory, reloads SystemD, enables both services to start on boot, and starts them automatically.
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

## 6. Docker Deployment

Deploying with Docker simplifies environment configuration and ensures consistency across development, staging, and production environments. The recommended structure uses **Docker Compose** to manage both the ASGI application container (Gunicorn/Uvicorn) and an Nginx reverse-proxy container.

### Dockerfile

Create a `Dockerfile` at the root of your project:

```dockerfile
# Use a lightweight official Python image
FROM python:3.12-slim

# Environment variables to optimize Python inside Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn uvicorn

# Copy the rest of the project source code
COPY . .

# Security: Run the application as a non-root user
RUN useradd -u 1000 appuser \
    && mkdir -p .asok/sessions .asok/cache src/partials/uploads \
    && chown -R appuser:appuser /app \
    && chmod -R 775 /app

USER appuser

# Expose the internal application port
EXPOSE 8000

# Start server using Gunicorn supervising Uvicorn workers
CMD ["gunicorn", "wsgi:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
```

### .dockerignore

Create a `.dockerignore` file to exclude local folders from the build context:

```text
.git
.github
.venv
venv
__pycache__
*.pyc
*.pyo
*.pyd
db.sqlite3
db.sqlite3-shm
db.sqlite3-wal
.asok
.env
.DS_Store
.ruff_cache
```

### Docker Compose Configuration (`docker-compose.yml`)

The compose setup coordinates the ASGI app and the Nginx web server. To ensure that static assets (CSS, JS, images) are kept in sync across image updates (since Docker named volumes do not automatically overwrite files once initialized), we use a shared volume to copy assets to Nginx during startup. SQLite and user uploads are persisted in separate dedicated volumes.

```yaml
version: '3.8'

services:
  app:
    build: .
    container_name: asok_app
    restart: always
    environment:
      - DEBUG=False
      - SECRET_KEY=your_production_secret_key_here
      - DATABASE_URL=sqlite:///app/db_data/db.sqlite3
    volumes:
      # Shared volume to transfer static assets to Nginx
      - static_volume:/app/static_volume_shared
      # Persistent volume for user uploads
      - uploads_volume:/app/src/partials/uploads
      # Persistent volume for SQLite database
      - db_volume:/app/db_data
    # Sync assets, run migrations, and start server on startup
    entrypoint: >
      sh -c "
      mkdir -p /app/static_volume_shared &&
      cp -rf /app/src/partials/css /app/src/partials/js /app/src/partials/images /app/static_volume_shared/ &&
      asok migrate &&
      gunicorn wsgi:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
      "

  nginx:
    image: nginx:alpine
    container_name: asok_nginx
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - static_volume:/usr/share/nginx/html/static:ro
      - uploads_volume:/usr/share/nginx/html/uploads:ro
    depends_on:
      - app

volumes:
  static_volume:
  uploads_volume:
  db_volume:
```

### Nginx Configuration (`nginx.conf`)

Add a `nginx.conf` at your project root. Notice that Asok serves static folders directly at the root (`/css/`, `/js/`, `/images/`, `/uploads/`), which Nginx maps to the shared volumes:

```nginx
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    sendfile on;
    keepalive_timeout 65;

    # Gzip Compression
    gzip on;
    gzip_disable "msie6";
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml application/json application/javascript application/xml+rss image/svg+xml;

    server {
        listen 80;
        server_name localhost; # Replace with your domain name

        # Static CSS files served directly by Nginx
        location /css/ {
            alias /usr/share/nginx/html/static/css/;
            expires 30d;
            add_header Cache-Control "public, no-transform";
            access_log off;
        }

        # Static JavaScript files served directly by Nginx
        location /js/ {
            alias /usr/share/nginx/html/static/js/;
            expires 30d;
            add_header Cache-Control "public, no-transform";
            access_log off;
        }

        # Static image assets served directly by Nginx
        location /images/ {
            alias /usr/share/nginx/html/static/images/;
            expires 30d;
            add_header Cache-Control "public, no-transform";
            access_log off;
        }

        # User uploaded media assets served directly by Nginx
        location /uploads/ {
            alias /usr/share/nginx/html/uploads/;
            expires 30d;
            add_header Cache-Control "public, no-transform";
        }

        # Forward all other requests to the ASGI Python application
        location / {
            proxy_pass http://app:8000;
            
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # WebSocket support (required for Asok sockets & SSE)
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";

            # Disable buffering for SSE (real-time stream) compatibility
            proxy_buffering off;

            client_max_body_size 10M;
        }
    }
}
```

### Launching the Stack

To build and start your application container stack in the background, run:

```bash
docker compose up -d --build
```
