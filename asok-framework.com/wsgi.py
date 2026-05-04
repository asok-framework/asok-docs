"""
import os
from datetime import datetime, timezone
from asok import Asok, WebSocketServer
from asok.session import SessionStore

# 1. Application Initialization
app = Asok()

# 2. RUNTIME CONFIGURATION (Special for SystemD / AlmaLinux)
# This directory is created by SystemD via the RuntimeDirectory=asok option
SESSION_DIR = "/run/asok/sessions"

# Ensure the sub-directory exists
if not os.path.exists(SESSION_DIR):
    try:
        os.makedirs(SESSION_DIR, exist_ok=True)
    except:
        pass

app.config["SESSION_BACKEND"] = "file"
app.config["SESSION_PATH"] = SESSION_DIR
app._session_store = SessionStore(backend="file", path=SESSION_DIR)

# 3. Content-Security-Policy Security Patch
# IMPORTANT: In Asok v0.1.3, the signature changed to include 'request'
_original_security_headers = app._security_headers

def _patched_security_headers(request=None, nonce=None):
    # Pass the 'request' argument to the original method for v0.1.3+ compatibility
    headers = _original_security_headers(request=request, nonce=nonce)
    for i, (name, value) in enumerate(headers):
        if name == "Content-Security-Policy":
            new_value = value.replace(
                "connect-src 'self'", 
                "connect-src 'self' wss://asok-framework.com https://asok-framework.com wss://www.asok-framework.com"
            ).replace(";;", ";")
            headers[i] = (name, new_value)
    return headers

app._security_headers = _patched_security_headers

# 4. Global Variables Sharing
app.share(
    version=app.version, 
    year=datetime.now(timezone.utc).year
)

# 5. WebSocket Configuration
# Change the ws port ex: 8001 in production (as configured in SystemD/Nginx)
ws_port = int(os.environ.get("WS_PORT", 8001))
allowed = ["https://asok-framework.com", "https://www.asok-framework.com"]

ws = WebSocketServer(app=app, port=ws_port, allowed_origins=allowed)
ws.start()
"""

from asok import Asok, WebSocketServer


app = Asok()

ws = WebSocketServer(app=app, port=8001)
ws.start()
