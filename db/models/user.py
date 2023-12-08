from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base


class User(Base):
    user_id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(40), nullable=False)
    subscribe: Mapped[bool] = mapped_column(Boolean, default=False)
