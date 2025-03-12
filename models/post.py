from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Post(Base):
    title: Mapped[str] = mapped_column(String(100))
    body: Mapped[str]
    user_id: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
