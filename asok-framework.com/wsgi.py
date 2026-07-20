from asok.admin import Admin
from datetime import datetime, timezone
from asok import Asok, WebSocketServer


app = Asok()
Admin(app)

from src.models.announcement import Announcement

app.share(
    version=app.version,
    year=datetime.now(timezone.utc).year,
    announcements=lambda request: Announcement.query().filter_by(is_visible=True).order_by("-created_at").get()
)


ws = WebSocketServer(app=app, port=8001)
ws.start()