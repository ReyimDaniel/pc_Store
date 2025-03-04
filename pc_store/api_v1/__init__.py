from fastapi import APIRouter

from .controllers.product_controller import router as product_router

router = APIRouter()
router.include_router(router=product_router, prefix="/products", tags=["products"])
