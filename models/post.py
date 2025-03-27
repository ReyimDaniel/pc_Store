from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import UserRelationMixIn


class Post(UserRelationMixIn, Base):
    _user_back_populates = "posts"

    title: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default=""
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, user={self.user_id}, title={self.title!r}"

    def __repr__(self):
        return str(self)
