from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    name: Annotated[str, MinLen(3), MaxLen(10)]
    email: EmailStr
    phone: Annotated[int, MinLen(11), MaxLen(11)]
