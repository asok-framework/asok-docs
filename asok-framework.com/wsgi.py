from datetime import datetime, timezone
from asok import Asok, WebSocketServer


app = Asok()
app.share(
    version=app.version,
    year=datetime.now(timezone.utc).year
)

ws = WebSocketServer(app=app, port=8001)
ws.start()