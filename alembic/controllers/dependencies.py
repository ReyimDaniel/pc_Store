from typing import Annotated

from fastapi import HTTPException, status, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from alembic.repositories import alembic_repository
from core import db_helper
from models.user import User


async def get_user_by_id(user_id: Annotated[int, Path],
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)) -> User:
    user = await alembic_repository.get_user_by_id(session=session, user_id=user_id)
    if user is not None:
        return user.id
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")
