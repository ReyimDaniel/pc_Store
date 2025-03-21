from typing import Optional

from pydantic import ConfigDict
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

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, first_name={self.first_name!r}, last_name={self.last_name!r}, "
            f"description={self.description!r})")

    def __repr__(self):
        return str(self)
