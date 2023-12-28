from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func, ForeignKey, BigInteger, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models import Base
from ..db_helper import db_helper

if TYPE_CHECKING:
    from .user import User


class History(Base):
    history_id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(server_default=func.now(), default=datetime.now)
    values: Mapped[float]
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("user.user_id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="histories")


async def add_data_in_history(values: float, user_id: int, date: datetime) -> None:
    async with db_helper.session_factory() as session:
        history = History(date=date, values=values, user_id=user_id)
        session.add(history)
        await session.commit()


async def get_history(user_id) -> list:
    async with db_helper.session_factory() as session:
        stmt = select(History.date, History.values).where(History.user_id == user_id)
        result = await session.execute(stmt)
        histories = result.all()
        return list(histories)
