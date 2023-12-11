import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pycbrf import ExchangeRates

from button import setting_button_subscribe, keyboard_start
from config import BOT_TOKEN
from db.models.crud import (
    add_data_in_history,
    check_user_in_user_table,
    add_user,
    check_subscribe,
    subscribe_on,
    subscribe_off,
    get_history)
from start_message_text import start_text

logging.basicConfig(level=logging.INFO)
main_bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()


async def get_current_rate():
    today = str(datetime.now().date())
    rates = ExchangeRates(today)
    result = rates["USD"]
    current_rate = result.value
    return current_rate


async def start_or_not_register_command(message: types.Message):
    if await check_user_in_user_table(message.chat.id):
        await message.answer(start_text, reply_markup=keyboard_start())
    else:
        await add_user(message.chat.first_name, message.chat.id)
        await message.answer(start_text, reply_markup=keyboard_start())


async def send_message_cron(bot: main_bot, chat_id: int):
    current_rate = await get_current_rate()
    date = datetime.utcnow()
    await add_data_in_history(values=current_rate, user_id=chat_id, date=date)
    await bot.send_message(chat_id, f"По данным ЦБ РФ курc доллара: {current_rate} руб.")


@dp.message(Command("start"))
async def start(message: types.Message):
    await start_or_not_register_command(message)


@dp.message(F.text.lower() == "узнать текущий курс доллара")
async def current_rate_message(message: types.Message):
    value = await get_current_rate()
    date = datetime.utcnow()
    await add_data_in_history(values=value,
                              user_id=message.chat.id,
                              date=date)
    await message.answer(f"По данным ЦБ РФ текущий курc доллара: {value} руб.")


@dp.message(F.text.lower() == "настройка подписки")
async def setting_subscribe_message(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=setting_button_subscribe())


@dp.callback_query(F.data == "subscribe_on")
async def subscribe_on_callback(callback: types.CallbackQuery):
    if await check_subscribe(callback.message.chat.id):
        await callback.message.answer(f"Вы уже подписаны на рассылку!")
        await callback.message.delete()
    else:
        await subscribe_on(callback.message.chat.id)
        scheduler.add_job(send_message_cron,
                          trigger="cron",
                          hour=12,
                          minute=10,
                          start_date=datetime.utcnow(),
                          kwargs={"bot": main_bot, "chat_id": callback.message.chat.id},
                          id=str(callback.message.chat.id))
        await callback.message.answer(f"Вы подписаны на рассылку сообщений раз в день.")
        await callback.message.delete()


@dp.callback_query(F.data == "subscribe_off")
async def subscribe_off_callback(callback: types.CallbackQuery):
    if await check_subscribe(callback.message.chat.id):
        await subscribe_off(callback.message.chat.id)
        scheduler.remove_job(f"{callback.message.chat.id}")
        await callback.message.answer(f"Вы успешно отписались от рассылки.")
        await callback.message.delete()

    else:
        await callback.message.answer(f"Вы не подписаны на рассылку.")
        await callback.message.delete()


@dp.message(F.text.lower() == "посмотреть историю запросов")
async def history_message(message: types.Message):
    history_list = await get_history(message.chat.id)
    await message.answer("История ваших запросов:")
    histories = []
    for index, history in enumerate(history_list, 1):
        date = datetime.strftime(history[0], "%Y-%m-%d %H:%M:%S")
        value = history[1]
        histories.append(f"{index}. Дата и время: {date}, курс доллара: {value}")

    await message.answer("\n".join(histories))


@dp.message()
async def not_register_command(message: types.Message):
    await start_or_not_register_command(message)


async def main():
    scheduler.start()
    await main_bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(main_bot)


if __name__ == "__main__":
    asyncio.run(main())
