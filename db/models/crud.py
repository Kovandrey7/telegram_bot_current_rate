import asyncio
from datetime import datetime

from sqlalchemy import select, update

from db.db_helper import db_helper
from db.models import User, History, CurrentRate


async def add_user(user_name: str, user_id: int, subscribe: bool = False, is_active: bool = True):
    async with db_helper.session_factory() as session:
        user = User(user_id=user_id, user_name=user_name, subscribe=subscribe, is_active=is_active)
        session.add(user)
        await session.commit()


async def check_user_in_user_table(user_id: int) -> True | False:
    async with db_helper.session_factory() as session:
        stmt = select(User).where(User.user_id == user_id)
        res = await session.scalar(stmt)
        return True if res else False


async def add_data_in_history(values: float, user_id: int, date: datetime):
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


async def check_subscribe(user_id: int) -> True | False:
    async with db_helper.session_factory() as session:
        stmt = select(User).where(User.user_id == user_id, User.subscribe)
        result = await session.scalar(stmt)
        return True if result else False


async def check_user_status(user_id: int) -> True | False:
    async with db_helper.session_factory() as session:
        stmt = select(User).where(User.user_id == user_id, User.is_active)
        result = await session.scalar(stmt)
        return True if result else False


async def change_user_status(user_id: int):
    async with db_helper.session_factory() as session:
        if await check_user_status(user_id=user_id):
            stmt = update(User).where(User.user_id == user_id).values(is_active=False)
        else:
            stmt = update(User).where(User.user_id == user_id).values(is_active=True)
        await session.execute(stmt)
        await session.commit()


async def subscribe_on(user_id: int):
    async with db_helper.session_factory() as session:
        stmt = update(User).where(User.user_id == user_id).values(subscribe=True)
        await session.execute(stmt)
        await session.commit()


async def subscribe_off(user_id: int):
    async with db_helper.session_factory() as session:
        stmt = update(User).where(User.user_id == user_id).values(subscribe=False)
        await session.execute(stmt)
        await session.commit()


async def add_usd_in_current_rate(value, currency_name: str = "USD"):
    async with db_helper.session_factory() as session:
        stmt = select(CurrentRate.currency_name).where(CurrentRate.currency_name == currency_name)
        if await session.scalar(stmt):
            stmt_2 = update(CurrentRate).where(CurrentRate.currency_name == currency_name).values(value=value)
            await session.execute(stmt_2)
            await session.commit()
        else:
            current_usd = CurrentRate(currency_name=currency_name, value=value)
            session.add(current_usd)
            await session.commit()


async def update_usd_current_rate(value, currency_name: str = "USD"):
    async with db_helper.session_factory() as session:
        stmt = update(CurrentRate).where(CurrentRate.currency_name == currency_name).values(value=value)
        await session.execute(stmt)
        await session.commit()


async def get_current_rate_usd(currency_name: str = "USD"):
    async with db_helper.session_factory() as session:
        stmt = select(CurrentRate.value).where(CurrentRate.currency_name == currency_name)
        current_rate_usd = await session.scalar(stmt)
        return current_rate_usd


async def main():
    pass

if __name__ == '__main__':
    asyncio.run(main())
    # pass
