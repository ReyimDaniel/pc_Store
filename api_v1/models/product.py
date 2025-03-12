from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    price: int
    description: str


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductUpdatePartial(ProductBase):
    name: Optional[str] = None
    price: Optional[int] = None
    description: Optional[str] = None


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ProductPriceRange(BaseModel):
    min_price: int
    max_price: int
