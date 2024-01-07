import sqlalchemy as sa
from sqlalchemy.orm import relationship

from src.db import Base


class BaseABC(Base):
    __abstract__ = True

    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
    updated_at = sa.Column(
        sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()
    )

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.__dict__}>"


class Account(BaseABC):
    __tablename__ = "account"

    account_id = sa.Column(sa.Integer, primary_key=True, index=True)
    username = sa.Column(sa.String, unique=True, index=True)
    is_active = sa.Column(sa.Boolean, default=True)

    def __str__(self):
        return self.username


class UserSettings(BaseABC):
    __tablename__ = "user_settings"
    account_id = sa.Column(
        sa.Integer, sa.ForeignKey("account.account_id"), primary_key=True
    )
    account = relationship("Account", backref="settings")

    theme = sa.Column(sa.String(40), server_default="light")
    profile_picture = sa.Column(sa.String(2048), server_default="default.png")
    language = sa.Column(sa.String(40), server_default="English")
    wifi_only = sa.Column(sa.Boolean, default=False)
    auto_play = sa.Column(sa.Boolean, default=False)
    notifications_enabled = sa.Column(sa.Boolean, default=True)
    adult_content_enabled = sa.Column(sa.Boolean, default=False)
    explicit_phrases = sa.Column(sa.Boolean, default=False)

    def __str__(self):
        return self.account.username


class Audiobook(BaseABC):
    __tablename__ = "audiobook"

    audiobook_id = sa.Column(sa.Integer, primary_key=True, index=True)

    category_id = sa.Column(sa.Integer, sa.ForeignKey("category.category_id"))
    category = relationship("Category", backref="audiobooks")

    title = sa.Column(sa.String(120), nullable=False, index=True)
    author = sa.Column(sa.String(100), nullable=False, index=True)
    description = sa.Column(sa.String(1000), nullable=False)
    duration = sa.Column(sa.Integer, nullable=False)
    cover_image = sa.Column(sa.String(2048), nullable=False)
    listened_times = sa.Column(sa.Integer, default=0)
    rating = sa.Column(sa.Float, default=0)

    def __str__(self):
        return f"{self.title} by {self.author}"


class Category(BaseABC):
    __tablename__ = "category"

    category_id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String, nullable=False, index=True)

    def __str__(self):
        return self.name
