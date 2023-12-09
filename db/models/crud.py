import asyncio
from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_helper import db_helper
from db.models import User, History


async def add_user(session: AsyncSession, user_name: str, user_id: int, subscribe: bool = False):
    user = User(user_id=user_id, user_name=user_name, subscribe=subscribe)
    session.add(user)
    await session.commit()


async def check_user_in_user_table(session: AsyncSession, user_id: int) -> True | False:
    stmt = select(User).where(User.user_id == user_id)
    res = await session.scalar(stmt)
    return True if res else False


async def add_data_in_history(
        session: AsyncSession,
        values: str,
        user_id: int,
        date: datetime
):
    history = History(date=date, values=values, user_id=user_id)
    session.add(history)
    await session.commit()


async def get_history(session: AsyncSession, user_id) -> list:
    stmt = select(History.date, History.values).where(History.user_id == user_id)
    result = await session.execute(stmt)
    histories = result.all()
    return list(histories)


async def check_subscribe(session: AsyncSession, user_id: int):
    stmt = select(User).where(User.user_id == user_id, User.subscribe)
    result = await session.scalar(stmt)
    return True if result else False


async def subscribe_on(session: AsyncSession, user_id: int):
    stmt = update(User).where(User.user_id == user_id).values(subscribe=True)
    await session.execute(stmt)
    await session.commit()


async def subscribe_off(session: AsyncSession, user_id: int):
    stmt = update(User).where(User.user_id == user_id).values(subscribe=False)
    await session.execute(stmt)
    await session.commit()


async def main():
    async with db_helper.session_factory() as session:
        pass
        # await add_user(session, "Andrey", 1)
        # await check_user_in_user_table(session, 1)
        # await add_data_in_history(session, "123", 1, date=datetime.utcnow())
        # await add_data_in_history(session, "456", 1, date=datetime.utcnow())
        # print(await get_history(session, 1))
        # print(await check_subscribe(session, 1))
        # await subscribe_on(session, 1)
        # await subscribe_off(session, 1)


if __name__ == '__main__':
    asyncio.run(main())
