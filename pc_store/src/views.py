from fastapi import APIRouter

from pc_store.src import crud
from pc_store.src.schemas.users import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.post('/')
def create_user(user: User):
    return crud.create_user(user_in=user)
