from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .accounts import RefreshTokenModel as RefreshTokenModel
from .accounts import UserModel as UserModel
from .restauratns import RestaurantModel as RestaurantModel
