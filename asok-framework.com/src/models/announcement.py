import enum
from asok import Model, Field


class AnnouncementType(enum.Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"


class Announcement(Model):
    message = Field.Text(nullable=False)
    type = Field.Enum(AnnouncementType, default=AnnouncementType.INFO)
    dismissible = Field.Boolean(default=True)
    is_visible = Field.Boolean(default=False)
    created_at = Field.CreatedAt()