import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, date, timedelta
from src.database.models.restaurants import RestaurantModel, MenuModel, LikeModel

@pytest.mark.asyncio
async def test_create_like(async_client: AsyncClient, db_session: AsyncSession):
    # Create a restaurant
    restaurant = RestaurantModel(name="Test Restaurant")
    db_session.add(restaurant)
    await db_session.commit()
    await db_session.refresh(restaurant)

    # Create a menu
    menu = MenuModel(dishes="Pizza", restaurant_id=restaurant.id, date=datetime.now())
    db_session.add(menu)
    await db_session.commit()
    await db_session.refresh(menu)

    # Create a like
    response = await async_client.post("/likes/", json={"menu_id": menu.id}, params={"user_id": 1})
    assert response.status_code == 200
    assert response.json()["user_id"] == 1
    assert response.json()["menu_id"] == menu.id

    # Check that the like is created in the database and new like will rise an error
    response = await async_client.post("/likes/", json={"menu_id": menu.id}, params={"user_id": 1})
    assert response.status_code == 400
    assert response.json()["detail"] == "Цей користувач уже лайкнув це меню"

@pytest.mark.asyncio
async def test_get_today_menus_ordered_by_likes(async_client: AsyncClient, db_session: AsyncSession):
    # Create a restaurant
    restaurant = RestaurantModel(name="Test Restaurant")
    db_session.add(restaurant)
    await db_session.commit()
    await db_session.refresh(restaurant)

    # Create menus (Pizza and Burger)
    menu1 = MenuModel(dishes="Pizza", restaurant_id=restaurant.id, date=datetime.now())
    menu2 = MenuModel(dishes="Burger", restaurant_id=restaurant.id, date=datetime.now())
    db_session.add_all([menu1, menu2])
    await db_session.commit()
    await db_session.refresh(menu1)
    await db_session.refresh(menu2)

    # Create likes
    like1 = LikeModel(user_id=1, menu_id=menu1.id)
    like2 = LikeModel(user_id=2, menu_id=menu1.id)
    like3 = LikeModel(user_id=3, menu_id=menu2.id)
    db_session.add_all([like1, like2, like3])
    await db_session.commit()

    # Get today's menus ordered by likes
    response = await async_client.get("/menus/today/")
    assert response.status_code == 200
    menus = response.json()
    assert len(menus) == 2
    assert menus[0]["dishes"] == "Pizza"
    assert menus[0]["likes_count"] == 2
    assert menus[1]["dishes"] == "Burger"
    assert menus[1]["likes_count"] == 1

@pytest.mark.asyncio
async def test_create_restaurant(async_client: AsyncClient, db_session: AsyncSession):
    # Create a restaurant
    response = await async_client.post("/restaurants/", json={"name": "New Restaurant"})
    assert response.status_code == 201
    assert response.json()["name"] == "New Restaurant"

    # Check that the restaurant is created in the database
    result = await db_session.execute(select(RestaurantModel).where(RestaurantModel.name == "New Restaurant"))
    restaurant = result.scalars().first()
    assert restaurant is not None
    assert restaurant.name == "New Restaurant"