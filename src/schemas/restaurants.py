from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RestaurantCreateSchema(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class RestaurantResponseSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class MenuCreateSchema(BaseModel):
    restaurant_id: int
    dishes: str


class MenuResponseSchema(BaseModel):
    id: int
    dishes: str
    date: datetime
    restaurant_id: int
    likes_count: int

    model_config = ConfigDict(from_attributes=True)


class LikeCreateSchema(BaseModel):
    menu_id: int


class LikeResponseSchema(BaseModel):
    id: int
    user_id: int
    menu_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
