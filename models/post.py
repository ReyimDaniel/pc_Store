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

    # user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    # user: Mapped["User"] = relationship(back_populates="posts")
    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, user={self.user_id}, title={self.title!r}"

    def __repr__(self):
        return str(self)
