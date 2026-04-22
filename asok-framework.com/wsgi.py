import os
from datetime import datetime, timezone
from asok import Asok, WebSocketServer

# Get current year for template sharing
year = datetime.now(timezone.utc).year

# Initialize Asok application
app = Asok()

# Share common variables across all templates
app.share(
    version=app.version, 
    year=year
)

# Initialize WebSocket server using environment variable or default 8001
ws_port = int(os.environ.get("WS_PORT", 8001))
ws = WebSocketServer(app=app, port=ws_port)

# Start WebSocket server in background
ws.start()