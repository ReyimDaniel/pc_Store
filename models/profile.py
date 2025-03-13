from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import UserRelationMixIn


class Profile(UserRelationMixIn, Base):
    _user_id_unique = True
    _user_back_populates = "profile"

    first_name: Mapped[Optional[str]] = mapped_column(String(40))
    last_name: Mapped[Optional[str]] = mapped_column(String(40))
    description: Mapped[Optional[str]]

    # user_id: Mapped[Optional[int]] = mapped_column(ForeignKey('user.id'), unique=True)
    # posts: Mapped[list["Post"]] = relationship(back_populates="user")
