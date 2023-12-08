from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, func, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models import Base

if TYPE_CHECKING:
    from .user import User


class History(Base):
    history_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime] = mapped_column(server_default=func.now(), default=datetime.utcnow)
    values: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.user_id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="histories")
