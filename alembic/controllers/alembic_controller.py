from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from alembic.repositories import alembic_repository

from core import db_helper
from models.profileResponseBody import ProfileResponse
from .dependencies import get_user_by_id
from models import User

router = APIRouter(tags=["alembic"])


@router.post("/create_new_user")
async def create_user(username: str = Query(..., description="Username"),
                      email: str = Query(..., description="example@mail.com"),
                      description: str = Query(..., description="Your description"),
                      session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await alembic_repository.create_user(session=session, username=username, email=email,
                                                description=description)


@router.get("/get_by_name")
async def get_user_by_username(username: str = Query(..., description="Username"),
                               session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await alembic_repository.get_user_by_username(session=session, username=username)


# TODO УНИКАЛЬНЫЙ USER_ID, В create_user_profile НЕЛЬЗЯ СОЗДАТЬ БОЛЕЕ 1 ПРОФИЛЯ НА ОДНОГО USER
@router.post("/create_new_profile")
async def create_user_profile(user_id: int = Depends(get_user_by_id),
                              first_name: str = Query(..., description="First name of Profile"),
                              last_name: str = Query(..., description="Last name of Profile"),
                              description: str = Query(..., description="Profile description"),
                              session: AsyncSession = Depends(
                                  db_helper.scoped_session_dependency)):
    return await alembic_repository.create_user_profile(session=session, user_id=user_id, first_name=first_name,
                                                        last_name=last_name, description=description)


@router.get("/get_all_profiles")
async def get_users_profile(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await alembic_repository.get_users_profile(session=session)


@router.post("/create_new_post")
async def create_user_post(user_id: int = Depends(get_user_by_id),
                           titles: list[str] = Query(..., description="Your titles"),
                           session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await alembic_repository.create_post(session, user_id, *titles)


@router.get("/get_all_users_with_posts")
async def get_users_with_posts(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await alembic_repository.get_users_with_posts(session=session)


@router.get("/get_all_post_with_user")
async def get_post_with_user(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await alembic_repository.get_post_with_user(session=session)


@router.get("/get_all_users_with_posts_and_profile")
async def get_users_with_posts_and_profile(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await alembic_repository.get_users_with_posts_and_profile(session=session)


@router.get("/get_all_profiles_with_user_and_posts")
async def get_profiles_with_user_and_posts(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await alembic_repository.get_profiles_with_user_and_posts(session=session)
