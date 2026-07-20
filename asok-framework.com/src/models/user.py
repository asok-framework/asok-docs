from asok import Field, Model

class User(Model):
    email = Field.String(unique=True, nullable=False)
    password = Field.Password()
    name = Field.String()
    is_admin = Field.Boolean(default=False)
    totp_secret = Field.String(nullable=True, hidden=True)
    totp_enabled = Field.Boolean(default=False)
    backup_codes = Field.String(nullable=True, hidden=True)
    created_at = Field.CreatedAt()
