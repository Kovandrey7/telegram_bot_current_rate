import asyncio
import logging

from aiogram import Bot, Dispatcher

from cb_rate import get_current_usd
from config import settings
from db.models.current_rate import add_usd_in_current_rate
from filters import blocked_bot
from handlers import user_handlers, callback_query
from scheduler.scheduler import update_usd_info_cron, send_message_cron

logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.BOT_TOKEN)

dp = Dispatcher()
dp.include_router(user_handlers.router)
dp.include_router(callback_query.router)
dp.include_router(blocked_bot.router)


async def main():
    current_usd = await get_current_usd()
    await add_usd_in_current_rate(current_usd)
    task = asyncio.create_task(update_usd_info_cron())
    task_2 = asyncio.create_task(send_message_cron(bot))
    await task
    await task_2
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
