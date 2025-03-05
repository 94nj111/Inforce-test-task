import os
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field
from dotenv import load_dotenv


load_dotenv()


class BaseAppSettings(BaseModel):
    BASE_DIR: Path = Field(default_factory=lambda: Path(__file__).parent.parent)

    PATH_TO_DB: str = Field(
        default_factory=lambda: str(Path(__file__).parent.parent / "database" / "source" / "restaurants.db")
    )

    LOGIN_TIME_DAYS: int = 7


class Settings(BaseAppSettings):
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "test_user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "test_password")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "test_host")
    POSTGRES_DB_PORT: int = int(os.getenv("POSTGRES_DB_PORT", "5432"))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "test_db")

    SECRET_KEY_ACCESS: str = os.getenv("SECRET_KEY_ACCESS", os.urandom(32).hex())
    SECRET_KEY_REFRESH: str = os.getenv("SECRET_KEY_REFRESH", os.urandom(32).hex())
    JWT_SIGNING_ALGORITHM: str = os.getenv("JWT_SIGNING_ALGORITHM", "HS256")


class TestingSettings(BaseAppSettings):
    SECRET_KEY_ACCESS: str = "TEST_SECRET_KEY_ACCESS"
    SECRET_KEY_REFRESH: str = "TEST_SECRET_KEY_REFRESH"
    JWT_SIGNING_ALGORITHM: str = "HS256"

    TEST_DATABASE_URL: str = "sqlite+aiosqlite:///:memory:"

    def model_post_init(self, __context: dict[str, Any] | None = None) -> None:
        object.__setattr__(self, "PATH_TO_DB", self.TEST_DATABASE_URL)


if __name__ == "__main__":
    settings = Settings()
    print("Path to DB:", settings.PATH_TO_DB)
