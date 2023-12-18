from typing import TYPE_CHECKING

from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base

if TYPE_CHECKING:
    from .history import History


class User(Base):
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_name: Mapped[str] = mapped_column(String(40), nullable=False)
    subscribe: Mapped[bool] = mapped_column(default=False)

    histories: Mapped[list["History"]] = relationship(back_populates="user")
