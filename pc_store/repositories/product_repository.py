"""
CREATE
READ
UPDATE
DELETE
"""
from pc_store.models import Product


def create_product(product_in: Product) -> dict:
    product = product_in.model_dump()
    return {
        "status": True,
        "product": product
    }
