from sqlalchemy import String, select, update
from sqlalchemy.orm import Mapped, mapped_column

from db.db_helper import db_helper
from db.models.base import Base


class CurrentRate(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    currency_name: Mapped[str] = mapped_column(String(40), nullable=False)
    value: Mapped[float]


async def add_usd_in_current_rate(value, currency_name: str = "USD") -> None:
    async with db_helper.session_factory() as session:
        stmt = select(CurrentRate.currency_name).where(
            CurrentRate.currency_name == currency_name
        )
        if await session.scalar(stmt):
            stmt_2 = (
                update(CurrentRate)
                .where(CurrentRate.currency_name == currency_name)
                .values(value=value)
            )
            await session.execute(stmt_2)
            await session.commit()
        else:
            current_usd = CurrentRate(currency_name=currency_name, value=value)
            session.add(current_usd)
            await session.commit()


async def update_usd_current_rate(value, currency_name: str = "USD") -> None:
    async with db_helper.session_factory() as session:
        stmt = (
            update(CurrentRate)
            .where(CurrentRate.currency_name == currency_name)
            .values(value=value)
        )
        await session.execute(stmt)
        await session.commit()


async def get_current_rate_usd(currency_name: str = "USD") -> float:
    async with db_helper.session_factory() as session:
        stmt = select(CurrentRate.value).where(
            CurrentRate.currency_name == currency_name
        )
        current_rate_usd = await session.scalar(stmt)
        return current_rate_usd
