from fastapi import APIRouter

from models import Product
from repositories import product_repository

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.post("/")
def create_product(product: Product):
    return product_repository.create_product(product_in=product)
