from fastapi import APIRouter

from pc_store.src.models import User
from pc_store.src.repositories import user_repository

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/")
def create_user(user: User):
    return user_repository.create_user(user_in=user)
