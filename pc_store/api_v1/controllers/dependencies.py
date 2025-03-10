from typing import Annotated

from fastapi import HTTPException, status, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from pc_store.api_v1.repositories import product_repository
from pc_store.core import db_helper
from pc_store.models.product import Product


async def get_product_by_id(product_id: Annotated[int, Path],
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)) -> Product:
    product = await product_repository.get_product_by_id(session=session, product_id=product_id)
    if product is not None:
        return product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {product_id} not found")
