"""
CREATE
READ
UPDATE
DELETE
"""
from schemas.users import User


def create_user(user_in: User) -> dict:
    user = user_in.model_dump()
    return {
        "status": True,
        "user": user
    }
