from typing import Optional

from pydantic import BaseModel


class ProfileResponse(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    description: Optional[str]

    class Config:
        from_attributes = True
