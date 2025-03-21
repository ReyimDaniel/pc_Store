import asyncio
from typing import Optional

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from core import db_helper
from models import User, Post, Profile


async def create_user(session: AsyncSession, username: str, email: str, description: str) -> User:
    user = User(username=username, email=email, description=description)
    session.add(user)
    await session.commit()
    return user


async def get_user_by_id(session: AsyncSession, user_id: int) -> Optional[User]:
    return await session.get(User, user_id)


async def get_user_by_username(session: AsyncSession, username: str) -> Optional[User]:
    stmt = select(User).where(User.username == username)
    result: Result = await session.execute(stmt)
    user: User = result.scalar_one_or_none()
    return user


# TODO УНИКАЛЬНЫЙ USER_ID, В create_user_profile НЕЛЬЗЯ СОЗДАТЬ БОЛЕЕ 1 ПРОФИЛЯ НА ОДНОГО USER
async def create_user_profile(session: AsyncSession, user_id: int, first_name: str, last_name: str,
                              description: str) -> Profile:
    profile = Profile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        description=description
    )
    session.add(profile)
    await session.commit()
    return profile


async def get_users_profile(session: AsyncSession):
    stmt = select(User).options(joinedload(User.profile)).where(User.profile.has()).order_by(User.id)
    users = await session.scalars(stmt)
    return [user.profile for user in users]


async def create_post(session: AsyncSession, user_id: int, *titles: str) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in titles]
    session.add_all(posts)
    await session.commit()
    return posts


async def get_users_with_posts(session: AsyncSession):
    stmt = select(User).options(selectinload(User.posts)).where(User.posts.any()).order_by(User.id)
    users = await session.scalars(stmt)
    return [user.posts for user in users]


async def get_post_with_user(session: AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)
    return [post for post in posts]


async def get_users_with_posts_and_profile(session: AsyncSession):
    stmt = select(User).options(selectinload(User.posts), joinedload(User.profile)).order_by(User.id)
    users = await session.scalars(stmt)
    return [user for user in users]


async def get_profiles_with_user_and_posts(session: AsyncSession):
    stmt = select(Profile).options(joinedload(Profile.user).selectinload(User.posts)).order_by(Profile.id)
    profiles = await session.scalars(stmt)
    return [profile for profile in profiles]


async def main():
    async with db_helper.session_factory() as session:
        # await create_user(session=session, username="Daniel", email="danil@mail.ru",
        #                   description="Hi, my name is Daniel")
        # await create_user(session=session, username="Alexey", email="alex@mail.ru",
        #                   description="Hi, my name is Alexey")
        # await create_user(session=session, username="Dimitry", email="dima@mail.ru",
        #                   description="Hi, my name is Dima")
        user_dan = await get_user_by_username(session=session, username="Daniel")
        print(user_dan)
        # user_alex = await get_user_by_username(session=session, username="Alexey")
        # user_dima = await get_user_by_username(session=session, username="Dimitry")
        await create_user_profile(session=session, user_id=user_dan.id, first_name="Jane", last_name="Doe",
                                  description="This is my second account")
        # await create_user_profile(session=session, user_id=user_dima.id, first_name="Shine", last_name="Gen",
        #                           description="Hi, I love computer games")
        # await get_users_profile(session=session)
        # await create_post(session, user_dan.id, "SQL Joins", "SQL Select", "SQL CRUD")
        # await create_post(session, user_alex.id, "FastAPI", "FastAPI Repo", "FastAPI Controller")
        # await get_users_with_posts(session=session)
        # print(await get_post_with_user(session=session))
        # await get_users_with_posts_and_profile(session=session)
        # print(await get_profiles_with_user_and_posts(session=session))
        # await get_user_by_id(session=session, user_id=1)


if __name__ == '__main__':
    asyncio.run(main())
