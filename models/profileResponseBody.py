from pydantic import BaseModel


class ProfileResponse(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    description: str | None = None

    class Config:
        from_attributes = True
