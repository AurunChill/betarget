from datetime import datetime
import uuid
from typing import List
import enum

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyBaseOAuthAccountTableUUID
from sqlalchemy import String, Boolean, text, Integer, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from base import Base


class SubscriptionType(enum.Enum):
    free = "free"
    premium = "premium"


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    __tablename__ = "oauth_account"
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    oauth_name: Mapped[str] = mapped_column(String(100), nullable=False)
    access_token: Mapped[str] = mapped_column(String(1024), nullable=False)
    expires_at: Mapped[int] = mapped_column(Integer, nullable=True)
    refresh_token: Mapped[str] = mapped_column(String(1024), nullable=True)
    account_id: Mapped[str] = mapped_column(String(320), nullable=False)
    account_email: Mapped[str] = mapped_column(String(320), nullable=False)
    
    user = relationship("User", back_populates="oauth_accounts")


class User(SQLAlchemyBaseUserTable[uuid.UUID], Base):
    __tablename__ = "user"
    oauth_accounts: Mapped[List[OAuthAccount]] = relationship("OAuthAccount", lazy="joined", cascade="all, delete")

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), unique=True, index=True, nullable=False, primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(1023), nullable=False)
    registered_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    telegram: Mapped[str | None]
    whatsapp: Mapped[str | None]
    linkedin: Mapped[str | None]
    email: Mapped[str | None]
    phone_number: Mapped[str | None]
    verification_token: Mapped[str | None]
    reset_password_token: Mapped[str | None]
    subscription_type: Mapped[SubscriptionType | None] = mapped_column(Enum(SubscriptionType), default=SubscriptionType.free)
    profile_picture_url: Mapped[str | None]

    vacancies = relationship("Vacancy", back_populates="user", cascade="all, delete", passive_deletes=True)

    def __doc__(self):
        return f"User({self.id}){self.username}"

    def __str__(self):
        return f"({self.id}) {self.username}"
