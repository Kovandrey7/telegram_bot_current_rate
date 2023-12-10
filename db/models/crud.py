from datetime import datetime
from decimal import Decimal

from sqlalchemy import select, update

from db.db_helper import db_helper
from db.models import User, History


async def add_user(user_name: str, user_id: int, subscribe: bool = False):
    async with db_helper.session_factory() as session:
        user = User(user_id=user_id, user_name=user_name, subscribe=subscribe)
        session.add(user)
        await session.commit()


async def check_user_in_user_table(user_id: int) -> True | False:
    async with db_helper.session_factory() as session:
        stmt = select(User).where(User.user_id == user_id)
        res = await session.scalar(stmt)
        return True if res else False


async def add_data_in_history(values: Decimal, user_id: int, date: datetime):
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


if __name__ == '__main__':
    # asyncio.run()
    pass
