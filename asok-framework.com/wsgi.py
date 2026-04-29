"""
import os
from datetime import datetime, timezone

from asok import Asok, WebSocketServer
from asok.session import SessionStore

# 1. Initialisation de l'application
app = Asok()

# 2. CONFIGURATION RUNTIME (Spécial SystemD / AlmaLinux)
# Ce dossier est créé par SystemD via l'option RuntimeDirectory=asok
SESSION_DIR = "/run/asok/sessions"

# On s'assure que le sous-dossier existe
if not os.path.exists(SESSION_DIR):
    try:
        os.makedirs(SESSION_DIR, exist_ok=True)
    except:
        pass

app.config["SESSION_BACKEND"] = "file"
app.config["SESSION_PATH"] = SESSION_DIR
app._session_store = SessionStore(backend="file", path=SESSION_DIR)

# Log de contrôle
print(f"--- ASOK RUNTIME CONFIG ---")
print(f"Session Path: {app._session_store.path}")

# 3. Patch de sécurité Content-Security-Policy
_original_security_headers = app._security_headers

def _patched_security_headers(nonce=None):
    headers = _original_security_headers(nonce=nonce)
    for i, (name, value) in enumerate(headers):
        if name == "Content-Security-Policy":
            new_value = value.replace(
                "connect-src 'self'", 
                "connect-src 'self' wss://asok-framework.com https://asok-framework.com wss://www.asok-framework.com"
            ).replace(";;", ";")
            headers[i] = (name, new_value)
    return headers

app._security_headers = _patched_security_headers

# 4. Partage de variables globales
app.share(
    version=app.version, 
    year=datetime.now(timezone.utc).year
)

# 5. Configuration WebSocket
ws_port = int(os.environ.get("WS_PORT", 8001))
allowed = ["https://asok-framework.com", "https://www.asok-framework.com"]

ws = WebSocketServer(app=app, port=ws_port, allowed_origins=allowed)
ws.start()
"""

from datetime import datetime, timezone

from asok import Asok, WebSocketServer

app = Asok()

app.share(
    version=app.version, 
    year=datetime.now(timezone.utc).year
)

ws = WebSocketServer(app=app, allowed_origins="*", port=8001)

ws.start()