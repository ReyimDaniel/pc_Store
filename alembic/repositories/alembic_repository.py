import asyncio
from typing import Optional

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from core import db_helper
from models import User, Post, Profile, Order, Product, OrderProductAssociation


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


async def user_profile_posts_relations(session: AsyncSession):
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
    # await create_user_profile(session=session, user_id=user_dan.id, first_name="Jane", last_name="Doe",
    #                           description="This is my second account")
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

async def create_order(session: AsyncSession, promocode: Optional[str] = None) -> Order:
    order = Order(promocode=promocode)
    session.add(order)
    await session.commit()
    return order


async def create_product(session: AsyncSession, name: str, price: int, description: str) -> Product:
    product = Product(name=name, price=price, description=description)
    session.add(product)
    await session.commit()
    return product


async def create_orders_with_products(session: AsyncSession):
    order_promo = await create_order(session=session, promocode="M2M")
    order1 = await create_order(session=session)
    mouse1 = await create_product(session=session, name="Mouse Game 1", price=1500, description="New gaming Mouse")
    gamepad1 = await create_product(session=session, name="Gamepad", price=2200, description="New gaming Gamepad")
    display1 = await create_product(session=session, name="Game Display", price=2200,
                                    description="New OLED gaming Display")

    order_promo = await session.scalar(
        select(Order).where(Order.id == order_promo.id).options(selectinload(Order.products)))
    order1 = await session.scalar(select(Order).where(Order.id == order1.id).options(selectinload(Order.products)))
    order_promo.products.append(mouse1)
    order_promo.products.append(gamepad1)
    order_promo.products.append(display1)
    order1.products.append(gamepad1)
    order1.products.append(display1)
    await session.commit()


async def get_orders_with_products(session: AsyncSession) -> list[Order]:
    stmt = select(Order).options(selectinload(Order.products)).order_by(Order.id)
    orders = await session.scalars(stmt)
    return list(orders)


async def get_orders_with_products_through_secondary(session: AsyncSession):
    orders = await get_orders_with_products(session=session)
    for orders in orders:
        print(f"Order ID is {orders.id}, promocode is {orders.promocode}, created at {orders.created_at}")
        for products in orders.products:
            print("-", products.id, products.name, products.price, products.description)


async def get_orders_with_products_association(session: AsyncSession) -> list[Order]:
    stmt = select(Order).options(
        selectinload(Order.products).joinedload(OrderProductAssociation.product)).order_by(Order.id)
    orders = await session.scalars(stmt)
    return list(orders)


async def get_print_orders_with_products_with_association(session: AsyncSession):
    orders = await get_orders_with_products_association(session=session)
    for order in orders:
        print(f"Order ID is {order.id}, promocode is {order.promocode}")
        for product_detail in order.products:  # type: OrderProductAssociation
            print("-", product_detail.product.id, product_detail.product.name, product_detail.product.price,
                  product_detail.product.description, "count: ", product_detail.count)


async def create_new_product_for_existing_order(session: AsyncSession):
    orders = await get_orders_with_products_association(session=session)
    gift_product = await create_product(session, "Gift Product", 0, "Your Gift Product")
    for order in orders:
        order.products.append(
            OrderProductAssociation(
                count=1,
                unit_price=0,
                product=gift_product,
            )
        )
    await session.commit()


async def main_m2m(session: AsyncSession):
    # await create_orders_with_products(session=session)
    # await get_orders_with_products_through_secondary(session=session)
    # await create_new_product_for_existing_order(session=session)
    await get_print_orders_with_products_with_association(session=session)


async def main():
    async with db_helper.session_factory() as session:
        # await user_profile_posts_relations(session)
        await main_m2m(session)


if __name__ == '__main__':
    asyncio.run(main())
