
from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from pydantic import Field

class RestaurantCreate(BaseModel):
    name: str
    slug: str
    description: str | None = None


class RestaurantResponse(RestaurantCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CategoryCreate(BaseModel):
    name: str
    restaurant_id: int


class CategoryResponse(CategoryCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)

class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    category_id: int


class ProductResponse(ProductCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CategoryWithProducts(BaseModel):
    id: int
    name: str
    products: list[ProductResponse]

    model_config = ConfigDict(from_attributes=True)


class RestaurantMenuResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: str | None
    categories: list[CategoryWithProducts]

    model_config = ConfigDict(from_attributes=True)


class ProductUpdate(BaseModel):
    name: str | None = None
    category_id: int | None = Field(default=None, gt=0)
    description: str | None = None
    price: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=10,
        decimal_places=2
    )
