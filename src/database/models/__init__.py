from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .accounts import UserModel, RefreshTokenModel
from .restauratns import RestaurantModel
