import sqlalchemy as sa
from sqlalchemy.orm import relationship

from src.db import Base


class BaseABC(Base):
    __abstract__ = True

    created_at = sa.Column(sa.DateTime, default=sa.func.now())
    updated_at = sa.Column(sa.DateTime, default=sa.func.now(),
                           onupdate=sa.func.now())

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.__dict__}>"


class Account(BaseABC):
    __tablename__ = "account"

    account_id = sa.Column(sa.Integer, primary_key=True, index=True)
    username = sa.Column(sa.String, unique=True, index=True)
    is_active = sa.Column(sa.Boolean, default=True)

    reviews = relationship(
        "Review",
        back_populates="account"
    )

    listening = relationship(
        "Listening",
        back_populates="account"
    )

    def __str__(self):
        return self.username


class UserSettings(BaseABC):
    __tablename__ = "user_settings"
    account_id = sa.Column(
        sa.Integer, sa.ForeignKey("account.account_id"), primary_key=True
    )
    account = relationship(
        "Account",
        backref="settings",
        cascade="all, delete-orphan",
        single_parent=True,
    )

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

    reviews = relationship(
        "Review",
        back_populates="audiobook"
    )

    listening = relationship(
        "Listening",
        back_populates="audiobook"
    )

    def __str__(self):
        return f"{self.title} by {self.author}"


class Chapter(BaseABC):
    __tablename__ = "chapter"

    chapter_id = sa.Column(sa.Integer, primary_key=True, index=True)
    chapter_ordered_id = sa.Column(sa.String(100), nullable=False, index=True)

    audiobook_id = sa.Column(sa.Integer,
                             sa.ForeignKey("audiobook.audiobook_id"))
    parent_id = sa.Column(sa.Integer,
                          sa.ForeignKey("chapter.chapter_id"),
                          default=None)

    sub_title = sa.Column(sa.String(120), nullable=False, index=True)
    full_text = sa.Column(sa.Text, nullable=True)
    duration = sa.Column(sa.Integer, nullable=False)
    audio_file_url = sa.Column(sa.String(2048), nullable=False)

    audiobook = relationship(
        "Audiobook",
        backref="chapters",
        cascade="all, delete",
        single_parent=True,
    )
    children = relationship(
        "Chapter",
        back_populates="parent",
        lazy="joined",
        join_depth=1,
    )
    parent = relationship(
        "Chapter", back_populates="children", remote_side=[chapter_id]
    )
    listening = relationship(
        "Listening",
        back_populates="current_chapter"
    )

    def __str__(self):
        return f"{self.chapter_id} {self.sub_title}"


class UserChapter(BaseABC):
    __tablename__ = "user_chapter"

    user_chapter_id = sa.Column(sa.Integer, primary_key=True, index=True)

    account_id = sa.Column(sa.Integer, sa.ForeignKey("account.account_id"))
    account = relationship(
        "Account",
        cascade="all, delete-orphan",
        single_parent=True,
    )

    chapter_id = sa.Column(sa.Integer, sa.ForeignKey("chapter.chapter_id"))
    chapter = relationship(
        "Chapter",
        cascade="all, delete-orphan",
        single_parent=True,
    )

    listened_times = sa.Column(sa.Integer, default=1)

    def __str__(self):
        return f"{self.account_id} - {self.chapter_id}"


class UserAudiobook(BaseABC):
    __tablename__ = "user_audiobook"

    user_audiobook_id = sa.Column(sa.Integer, primary_key=True, index=True)

    account_id = sa.Column(sa.Integer,
                           sa.ForeignKey("account.account_id"))

    account = relationship(
        "Account",
        cascade="all, delete-orphan",
        single_parent=True,
    )

    audiobook_id = sa.Column(sa.Integer,
                             sa.ForeignKey("audiobook.audiobook_id"))

    audiobook = relationship(
        "Audiobook",
        cascade="all, delete-orphan",
        single_parent=True,
    )

    last_listened_chapter_id = sa.Column(
        sa.Integer, sa.ForeignKey("chapter.chapter_id")
    )
    last_listened_chapter = relationship(
        "Chapter",
        cascade="all, delete-orphan",
        single_parent=True,
    )

    def __str__(self):
        return f"{self.account_id}" \
               f" - {self.audiobook_id}" \
               f" - {self.last_listened_chapter}"


class Category(BaseABC):
    __tablename__ = "category"

    category_id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String, nullable=False, index=True)

    def __str__(self):
        return self.name


class Review(BaseABC):
    __tablename__ = "review"

    account_id = sa.Column(sa.Integer,
                           sa.ForeignKey("account.account_id"),
                           primary_key=True)

    account = relationship(
        "Account",
        back_populates="reviews"
    )

    audiobook_id = sa.Column(sa.Integer,
                             sa.ForeignKey("audiobook.audiobook_id"),
                             primary_key=True)

    audiobook = relationship(
        "Audiobook",
        cascade="all, delete",
        back_populates="reviews"
    )

    rating_value = sa.Column(sa.Integer, nullable=False)
    rating_date = sa.Column(sa.TIMESTAMP, nullable=False)
    review_content = sa.Column(sa.String)

    def __str__(self):
        return f"{self.account_id} {self.audiobook_id} {self.rating_value}"


class Listening(BaseABC):
    __tablename__ = "listening"

    account_id = sa.Column(sa.Integer,
                           sa.ForeignKey("account.account_id"),
                           primary_key=True)

    account = relationship(
        "Account",
        back_populates="listening",
        cascade="all, delete"
    )

    audiobook_id = sa.Column(sa.Integer,
                             sa.ForeignKey("audiobook.audiobook_id"),
                             primary_key=True)

    audiobook = relationship(
        "Audiobook",
        back_populates="listening",
        cascade="all, delete"
    )

    current_chapter_id = sa.Column(sa.Integer,
                                   sa.ForeignKey("chapter.chapter_id"))

    current_chapter = relationship(
        "Chapter",
        back_populates="listening",
        cascade="all, delete"
    )

    start_time = sa.Column(sa.TIMESTAMP, nullable=False)
    last_access_time = sa.Column(sa.TIMESTAMP, nullable=False)
    finish_time = sa.Column(sa.TIMESTAMP, default=sa.Null)
    is_favorite = sa.Column(sa.Boolean, nullable=False, default=False)
