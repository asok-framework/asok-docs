import os
from datetime import datetime, timezone
from asok import Asok, WebSocketServer
from asok.session import SessionStore

# 1. Application Initialization
app = Asok()

# Configure Session backend (after initialization to allow absolute paths for file fallback)
REDIS_URL = os.environ.get("ASOK_REDIS_URL") or os.environ.get("REDIS_URL")
if REDIS_URL:
    app.config["SESSION_BACKEND"] = "redis"
    app._session_store = SessionStore(backend="redis")
    print("[Asok] Session Store: Redis (Active)")
else:
    # Use standard path for ephemeral sessions (e.g., SystemD RuntimeDirectory), fallback to local path in dev/local environment
    SESSION_DIR = "/run/asok/sessions"
    if not os.path.exists(SESSION_DIR):
        try:
            os.makedirs(SESSION_DIR, exist_ok=True)
        except (PermissionError, OSError):
            SESSION_DIR = os.path.join(os.path.dirname(__file__), ".asok", "sessions")
            os.makedirs(SESSION_DIR, exist_ok=True)

    app.config["SESSION_BACKEND"] = "file"
    app.config["SESSION_PATH"] = SESSION_DIR
    app._session_store = SessionStore(backend="file", path=SESSION_DIR)
    print(f"[Asok] Session Store: File fallback ({SESSION_DIR})")

# 2. Production Optimizations & Content-Security-Policy (CSP)
app.config["CSP"] = {
    # Enable WebSocket connections in CSP (connect-src is automatically merged by Asok)
    "connect-src": [
        "wss://asok-framework.com",
        "wss://www.asok-framework.com",
        "https://asok-framework.com",
    ]
}

# 3. Global Variables Sharing
app.share(
    version=app.version,
    year=datetime.now(timezone.utc).year
)

# 4. WebSocket Configuration
ws_port = int(os.environ.get("WS_PORT", 8776))
allowed = ["https://asok-framework.com", "https://www.asok-framework.com"]

# Sync the WS port with app config for accurate automatic CSP generation
app.config["WS_PORT"] = ws_port

ws = WebSocketServer(app=app, port=ws_port, allowed_origins=allowed)

# Determine if the WS server should be started in this process
should_start_ws = (
    __name__ == "__main__"
    or os.environ.get("START_WS") == "true"
    or os.environ.get("ASOK_ENV") == "development"
)

if should_start_ws:
    ws.start()
    print(f"[Asok] WebSocket Server started on port {ws_port}")
    
    # If executed directly as a script (e.g. python wsgi.py), keep the main thread alive so the WS daemon thread doesn't exit
    if __name__ == "__main__":
        import time
        try:
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            ws.stop()
else:
    print(
        "[Asok] WebSocket Server initialized (Multi-worker WSGI instance, WS server bypass)"
    )

