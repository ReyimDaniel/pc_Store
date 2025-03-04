from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from pc_store.api_v1.models.product import ProductCreate, Product, ProductUpdate, ProductUpdatePartial, \
    ProductPriceRange
from pc_store.api_v1.repositories import product_repository
from pc_store.core import db_helper
from .dependencies import get_product_by_id

router = APIRouter(tags=['products'])


@router.get("/", response_model=list[Product])
async def get_products(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await product_repository.get_products(session=session)


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product_in: ProductCreate,
                         session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await product_repository.create_product(session=session, product_in=product_in)


@router.get("/{product_id}", response_model=Product)
async def get_product(product: Product = Depends(get_product_by_id)):
    return product


@router.put("/{product_id}", response_model=Product)
async def update_product(product_update: ProductUpdate,
                         product: Product = Depends(get_product_by_id),
                         session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await product_repository.update_product(session=session, product=product, product_update=product_update)


@router.patch("/{product_id}", response_model=Product)
async def update_product_partial(product_update: ProductUpdatePartial,
                                 product: Product = Depends(get_product_by_id),
                                 session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await product_repository.update_product(session=session, product=product, product_update=product_update,
                                                   partial=True)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product: Product = Depends(get_product_by_id),
                         session: AsyncSession = Depends(db_helper.scoped_session_dependency)) -> None:
    return await product_repository.delete_product(session=session, product=product)


@router.get("/products/price", response_model=list[Product])
async def get_products_price_range(price_range: ProductPriceRange = Depends(),
                                   session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await product_repository.get_product_range_price(session=session, price_range=price_range)


@router.get("/products/by_name", response_model=list[Product])
async def get_product_by_name(name: str = Query(..., description="Product name"),
                              session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await product_repository.get_product_by_name(session=session, name=name)


@router.get("/products/count")
async def get_product_count(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await product_repository.get_products_count(session=session)
