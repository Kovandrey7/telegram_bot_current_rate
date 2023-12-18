from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models import Base

if TYPE_CHECKING:
    from .user import User


class History(Base):
    history_id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(server_default=func.now(), default=datetime.now)
    values: Mapped[float]
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("user.user_id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="histories")
