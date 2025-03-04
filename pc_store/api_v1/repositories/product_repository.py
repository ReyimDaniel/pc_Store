from __future__ import annotations

from sqlalchemy import select, func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from pc_store.api_v1.models.product import ProductCreate, ProductUpdate, ProductUpdatePartial, ProductPriceRange
from pc_store.models.product import Product


async def get_products(session: AsyncSession) -> list[Product]:
    stmt = select(Product).order_by(Product.id)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def get_product_by_id(session: AsyncSession, product_id: int) -> Product | None:
    return await session.get(Product, product_id)


async def create_product(session: AsyncSession, product_in: ProductCreate) -> Product:
    product = Product(**product_in.model_dump())
    session.add(product)  # Отслеживание этого объекта
    await session.commit()
    # await session.refresh(product)
    return product


# Put + Patch
async def update_product(session: AsyncSession, product: Product,
                         product_update: ProductUpdate | ProductUpdatePartial, partial: bool = False, ) -> Product:
    for key, value in product_update.model_dump(exclude_unset=partial).items():
        setattr(product, key, value)
    await session.commit()
    return product


async def delete_product(session: AsyncSession, product: Product) -> None:
    await session.delete(product)
    await session.commit()


async def get_product_range_price(
        session: AsyncSession,
        price_range: ProductPriceRange) -> list[Product]:
    stmt = select(Product).where(Product.price.between(price_range.min_price, price_range.max_price))
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def get_product_by_name(session: AsyncSession, name: str) -> list[Product] | None:
    stmt = select(Product).where(Product.name.ilike(f"%{name}%"))
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def get_products_count(session: AsyncSession):
    stmt = select(func.count()).select_from(Product)
    result: Result = await session.execute(stmt)
    return {"total_result": result.scalar()}
