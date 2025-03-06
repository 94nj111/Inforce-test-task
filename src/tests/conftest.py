import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.dependencies import get_settings
from src.database.models.restaurants import Base
from src.database.session_sqlite import get_sqlite_db, reset_sqlite_database

@pytest.fixture(scope="function")
async def db_session():
    await reset_sqlite_database()
    async with get_sqlite_db() as session:
        yield session
        await session.rollback()

@pytest.fixture(scope="function")
async def async_client(db_session: AsyncSession):
    from httpx import AsyncClient
    from src.main import app
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client