from datetime import date, timedelta
from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from config.dependencies import get_current_user
from database import get_db
from database.models.accounts import (
    UserModel,
)
from database.models.restauratns import LikeModel, MenuModel, RestaurantModel
from schemas.restaurants import (
    LikeCreateSchema,
    LikeResponseSchema,
    MenuCreateSchema,
    MenuResponseSchema,
    RestaurantCreateSchema,
    RestaurantResponseSchema,
)

router = APIRouter()


@router.post(
    "/restaurants/",
    response_model=RestaurantResponseSchema,
    summary="Creating Restaurant",
    status_code=status.HTTP_201_CREATED,
    tags=["restaurants"],
    responses={
        409: {
            "description": "Conflict - Restaurant with this name already exists.",
            "content": {"application/json": {"example": {"detail": "A restaurant with this name already exists."}}},
        }
    },
)
async def create_restaurant(
    restaurant: RestaurantCreateSchema,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> RestaurantResponseSchema:
    """
    Create a new restaurant.
    """
    try:
        result = await db.execute(select(RestaurantModel).filter(RestaurantModel.name == restaurant.name))
        existing_restaurant = result.scalars().first()
        if existing_restaurant is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A restaurant with this name {restaurant.name} already exists.",
            )

        new_restaurant = RestaurantModel(name=restaurant.name)
        db.add(new_restaurant)
        await db.commit()
        await db.refresh(new_restaurant)
        return new_restaurant
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during restaurant creation: {str(e)}",
        )


@router.get(
    "/restaurants/",
    response_model=List[RestaurantResponseSchema],
    summary="Get All Restaurants",
    status_code=status.HTTP_200_OK,
    tags=["restaurants"],
)
async def get_restaurants(
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[RestaurantResponseSchema]:
    """
    Get all restaurants.
    """
    result = await db.execute(select(RestaurantModel))
    restaurants = result.scalars().all()
    return restaurants


@router.post(
    "/menus/",
    response_model=MenuResponseSchema,
    summary="Creating Restaurant",
    status_code=status.HTTP_201_CREATED,
    tags=["menus"],
    responses={
        404: {
            "description": "Not Found - Restaurant with this id not found.",
            "content": {"application/json": {"example": {"detail": "A restaurant with this id not found."}}},
        }
    },
)
async def create_menu(
    menu: MenuCreateSchema,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> MenuResponseSchema:
    """
    Create a new restaurant.
    """
    try:
        result = await db.execute(select(RestaurantModel).filter(RestaurantModel.id == menu.restaurant_id))
        existing_restaurant = result.scalars().first()
        if existing_restaurant is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"A restaurant with this id {menu.restaurant_id} not found.",
            )

        new_menu = MenuModel(restaurant_id=menu.restaurant_id, dishes=menu.dishes)
        db.add(new_menu)
        await db.commit()
        await db.refresh(new_menu)
        return new_menu
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during restaurant creation: {str(e)}",
        )


@router.get(
    "/menus/",
    response_model=List[MenuResponseSchema],
    summary="Get Today's Menus",
    status_code=status.HTTP_200_OK,
    tags=["menus"],
    responses={
        404: {
            "description": "Not Found - No menus found for today.",
            "content": {"application/json": {"example": {"detail": "No menus found for today."}}},
        }
    },
)
async def get_today_menus_ordered_by_likes(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> List[MenuResponseSchema]:
    today = date.today()

    query = (
        select(MenuModel, func.count(LikeModel.id).label("likes_count"))
        .outerjoin(LikeModel, MenuModel.id == LikeModel.menu_id)  # Join with likes
        .where(MenuModel.date >= today)  # Filter by today
        .where(MenuModel.date < today + timedelta(days=1))
        .group_by(MenuModel)  # Group by menu
        .order_by(func.count(LikeModel.id).desc())  # Sort by likes count
    )

    result = await db.execute(query)
    menus = result.all()

    response = [
        MenuResponseSchema(
            id=menu.id, dishes=menu.dishes, date=menu.date, restaurant_id=menu.restaurant_id, likes_count=likes_count
        )
        for menu, likes_count in menus
    ]

    return response


@router.post(
    "/likes/",
    response_model=LikeResponseSchema,
    summary="Create Like",
    status_code=status.HTTP_201_CREATED,
    tags=["likes"],
    responses={
        404: {
            "description": "Not Found - Menu with this id not found.",
            "content": {"application/json": {"example": {"detail": "A menu with this id not found."}}},
        }
    },
)
async def create_like(
    like_data: LikeCreateSchema,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> LikeResponseSchema:
    new_like = LikeModel(user_id=current_user.id, menu_id=like_data.menu_id)
    db.add(new_like)

    try:
        await db.commit()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during restaurant creation: {str(e)}",
        )

    await db.refresh(new_like)

    return new_like
