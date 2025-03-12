"""
CREATE
READ
UPDATE
DELETE
"""
from models import Product


def create_product(product_in: Product) -> dict:
    product = product_in.model_dump()
    return {
        "status": True,
        "product": product
    }
