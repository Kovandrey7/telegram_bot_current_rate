from datetime import datetime

import aiocron
from sqlalchemy import select

from cb_rate import get_current_usd
from db.db_helper import db_helper
from db.models import User
from db.models.current_rate import update_usd_current_rate
from db.models.history import add_data_in_history


async def update_usd_info_cron():
    @aiocron.crontab("0 */2 * * *")
    async def update_usd_info():
        current_usd = await get_current_usd()
        await update_usd_current_rate(value=current_usd)


async def send_message_cron(bot):
    @aiocron.crontab("0 10 * * *")
    async def send_message_at_10_00():
        async with db_helper.session_factory() as session:
            stmt = select(User.user_id).where(User.subscribe, User.is_active)
            result = await session.scalars(stmt)
            id_list = result.all()
        if id_list:
            current_usd = await get_current_usd()
            date = datetime.now()
            for id_user in id_list:
                await add_data_in_history(current_usd, id_user, date)
                await bot.send_message(
                    id_user, f"По данным ЦБ РФ курc доллара: {current_usd} руб."
                )
