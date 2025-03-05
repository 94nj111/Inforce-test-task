from datetime import datetime, timedelta, timezone
from typing import List

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from database.models import Base
from database.validators import accounts as validators
from security.passwords import hash_password, verify_password
from security.utils import generate_secure_token


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    _hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    refresh_tokens: Mapped[List["RefreshTokenModel"]] = relationship(
        "RefreshTokenModel", back_populates="user", cascade="all, delete-orphan"
    )
    likes: Mapped[List["LikeModel"]] = relationship("LikeModel", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<UserModel(id={self.id}, email={self.email})>"

    @classmethod
    def create(cls, email: str, raw_password: str) -> "UserModel":
        """
        Factory method to create a new UserModel instance.
        """
        user = cls(email=email)
        user.password = raw_password
        return user

    @property
    def password(self) -> None:
        raise AttributeError("Password is write-only. Use the setter to set the password.")

    @password.setter
    def password(self, raw_password: str) -> None:
        """
        Set the user's password after validating its strength and hashing it.
        """
        validators.validate_password_strength(raw_password)
        self._hashed_password = hash_password(raw_password)

    def verify_password(self, raw_password: str) -> bool:
        """
        Verify the provided password against the stored hashed password.
        """
        return verify_password(raw_password, self._hashed_password)

    @validates("email")
    def validate_email(self, key, value):
        return validators.validate_email(value.lower())


class TokenBaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, default=generate_secure_token)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc) + timedelta(days=1),
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)


class RefreshTokenModel(TokenBaseModel):
    __tablename__ = "refresh_tokens"

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="refresh_tokens")
    token: Mapped[str] = mapped_column(String(512), unique=True, nullable=False, default=generate_secure_token)

    @classmethod
    def create(cls, user_id: int, days_valid: int, token: str) -> "RefreshTokenModel":
        """
        Factory method to create a new RefreshTokenModel instance.
        """
        expires_at = datetime.now(timezone.utc) + timedelta(days=days_valid)
        return cls(user_id=user_id, expires_at=expires_at, token=token)

    def __repr__(self):
        return f"<RefreshTokenModel(id={self.id}, token={self.token}, expires_at={self.expires_at})>"
