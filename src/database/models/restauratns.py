from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from database.models import Base


class RestaurantModel(Base):
    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    menus: Mapped[List["MenuModel"]] = relationship(
        "MenuModel", back_populates="restaurant", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<RestaurantModel(id={self.id}, name={self.name})>"


class MenuModel(Base):
    __tablename__ = "menus"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dishes: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    restaurant_id: Mapped[int] = mapped_column(Integer, ForeignKey("restaurants.id"), nullable=False)
    restaurant: Mapped["RestaurantModel"] = relationship("RestaurantModel", back_populates="menus")
    likes: Mapped[List["LikeModel"]] = relationship("LikeModel", back_populates="menu", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<MenuModel(id={self.id}, dishes={self.dishes})>"


class LikeModel(Base):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    menu_id: Mapped[int] = mapped_column(Integer, ForeignKey("menus.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="likes")
    menu: Mapped["MenuModel"] = relationship("MenuModel", back_populates="likes")

    __table_args__ = (UniqueConstraint("user_id", "menu_id", name="unique_user_menu_like"),)

    def __repr__(self):
        return f"<LikeModel(id={self.id}, user_id={self.user_id}, menu_id={self.menu_id})>"
