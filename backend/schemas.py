
from pydantic import BaseModel, ConfigDict


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
