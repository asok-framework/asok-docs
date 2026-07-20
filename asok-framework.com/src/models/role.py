from asok import Field, Model


class Role(Model):
    name = Field.String(unique=True, nullable=False)
    label = Field.String()
    permissions = Field.String(default="")
    created_at = Field.CreatedAt()

    def __str__(self):
        return self.label or self.name
