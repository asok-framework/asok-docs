from asok import Field, Model, ModelAdmin


class AdminSession(Model):
    __tablename__ = "asok_sessions"
    sid = Field.String(unique=True, nullable=False)
    user_id = Field.Integer(nullable=True)
    ip = Field.String()
    user_agent = Field.String()
    device_type = Field.String()
    browser = Field.String()
    os_name = Field.String()
    location = Field.String()
    is_active = Field.Boolean(default=True)
    last_seen = Field.Integer()
    created_at = Field.CreatedAt()
    revoked_at = Field.Integer(nullable=True)

    class Admin(ModelAdmin):
        label = "Sessions"
        slug = "sessions"
        group = "System & Audit"
        list_display = ["id", "created_at", "user_id", "ip", "device_type", "browser", "is_active", "last_seen"]
        list_filter = ["is_active", "device_type", "browser"]
        search_fields = ["sid", "ip", "user_agent", "browser", "os_name"]
        show_in_overview = False
        per_page = 50
        can_add = False
        can_edit = False
        can_delete = False
