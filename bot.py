import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pycbrf import ExchangeRates

from button import button_else, button_start, del_reply_markup, setting_button_subscribe
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
        await message.answer(start_text, reply_markup=button_else())
    else:
        await add_user(message.chat.first_name, message.chat.id)
        await message.answer(start_text, reply_markup=button_start())


async def send_message_cron(bot: main_bot, chat_id: int):
    current_rate = await get_current_rate()
    date = datetime.utcnow()
    await add_data_in_history(values=current_rate, user_id=chat_id, date=date)
    await bot.send_message(chat_id, f"По данным ЦБ РФ курc доллара: {current_rate} руб.")


@dp.message(Command("start"))
async def start(message: types.Message):
    await start_or_not_register_command(message)


@dp.message()
async def not_register_command(message: types.Message):
    await start_or_not_register_command(message)


@dp.callback_query(F.data == "current_rate")
async def current_rate_callback(callback: types.CallbackQuery):
    value = await get_current_rate()
    date = datetime.utcnow()
    await add_data_in_history(values=value,
                              user_id=callback.message.chat.id,
                              date=date)
    await callback.message.answer(f"По данным ЦБ РФ курc доллара: {value} руб.")
    await callback.message.answer("Выберите действие:", reply_markup=button_else())
    await del_reply_markup(callback)


@dp.callback_query(F.data == "setting_subscribe")
async def setting_subscribe_callback(callback: types.CallbackQuery):
    await callback.message.answer("Выберите действие:", reply_markup=setting_button_subscribe())
    await del_reply_markup(callback)


@dp.callback_query(F.data == "subscribe_on")
async def subscribe_on_callback(callback: types.CallbackQuery):
    if await check_subscribe(callback.message.chat.id):
        await callback.message.answer(f"Вы уже подписаны на рассылку!")
        await callback.message.answer("Выберите действие:", reply_markup=button_else())
        await del_reply_markup(callback)
    else:
        await subscribe_on(callback.message.chat.id)
        await callback.message.answer(f"Вы подписаны на рассылку сообщений раз в день.")
        scheduler.add_job(send_message_cron,
                          trigger="cron",
                          hour=12,
                          minute=10,
                          start_date=datetime.utcnow(),
                          kwargs={"bot": main_bot, "chat_id": callback.message.chat.id},
                          id=str(callback.message.chat.id))
        await callback.message.answer("Выберите действие:", reply_markup=button_else())
        await del_reply_markup(callback)


@dp.callback_query(F.data == "subscribe_off")
async def subscribe_off_callback(callback: types.CallbackQuery):
    if check_subscribe(callback.message.chat.id):
        await subscribe_off(callback.message.chat.id)
        scheduler.remove_job(f"{callback.message.chat.id}")
        await callback.message.answer(f"Вы успешно отписались от рассылки.")
        await callback.message.answer("Выберите действие:", reply_markup=button_else())
        await del_reply_markup(callback)
    else:
        await callback.message.answer(f"Вы не подписаны на рассылку.")
        await callback.message.answer("Выберите действие:", reply_markup=button_else())
        await del_reply_markup(callback)


@dp.callback_query(F.data == "history")
async def history_callback(callback: types.CallbackQuery):
    history_list = await get_history(callback.message.chat.id)
    await callback.message.answer("История ваших запросов:")
    histories = []
    for index, history in enumerate(history_list, 1):
        date = datetime.strftime(history[0], "%Y-%m-%d %H:%M:%S")
        value = history[1]
        histories.append(f"{index}. Дата и время: {date}, курс доллара: {value}")

    await callback.message.answer("\n".join(histories))
    await callback.message.answer("Выберите действие:", reply_markup=button_else())
    await del_reply_markup(callback)


async def main():
    scheduler.start()
    await dp.start_polling(main_bot)


if __name__ == "__main__":
    asyncio.run(main())
