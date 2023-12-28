from typing import TYPE_CHECKING

from sqlalchemy import String, BigInteger, select, update
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base
from ..db_helper import db_helper

if TYPE_CHECKING:
    from .history import History


class User(Base):
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_name: Mapped[str] = mapped_column(String(40), nullable=False)
    subscribe: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    histories: Mapped[list["History"]] = relationship(back_populates="user")


async def add_user(
    user_name: str, user_id: int, subscribe: bool = False, is_active: bool = True
) -> None:
    async with db_helper.session_factory() as session:
        user = User(
            user_id=user_id,
            user_name=user_name,
            subscribe=subscribe,
            is_active=is_active,
        )
        session.add(user)
        await session.commit()


async def check_user_in_user_table(user_id: int) -> bool:
    async with db_helper.session_factory() as session:
        stmt = select(User).where(User.user_id == user_id)
        res = await session.scalar(stmt)
        return True if res else False


async def check_subscribe(user_id: int) -> bool:
    async with db_helper.session_factory() as session:
        stmt = select(User).where(User.user_id == user_id, User.subscribe)
        result = await session.scalar(stmt)
        return True if result else False


async def check_user_status(user_id: int) -> bool:
    async with db_helper.session_factory() as session:
        stmt = select(User).where(User.user_id == user_id, User.is_active)
        result = await session.scalar(stmt)
        return True if result else False


async def change_user_status(user_id: int) -> None:
    async with db_helper.session_factory() as session:
        if await check_user_status(user_id=user_id):
            stmt = update(User).where(User.user_id == user_id).values(is_active=False)
        else:
            stmt = update(User).where(User.user_id == user_id).values(is_active=True)
        await session.execute(stmt)
        await session.commit()


async def subscribe_on(user_id: int) -> None:
    async with db_helper.session_factory() as session:
        stmt = update(User).where(User.user_id == user_id).values(subscribe=True)
        await session.execute(stmt)
        await session.commit()


async def subscribe_off(user_id: int) -> None:
    async with db_helper.session_factory() as session:
        stmt = update(User).where(User.user_id == user_id).values(subscribe=False)
        await session.execute(stmt)
        await session.commit()
