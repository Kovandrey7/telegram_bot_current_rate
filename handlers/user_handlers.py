from datetime import datetime

from aiogram import types, F, Router
from aiogram.filters import CommandStart

from db.models.crud import check_user_in_user_table, add_user, get_current_rate_usd, add_data_in_history, get_history
from filters.user_in_database import UserInDatabase
from keyboards.keyboard import keyboard_start, setting_button_subscribe
from start_message_text import start_text

router = Router()


async def start_or_not_register_command(message: types.Message):
    if await check_user_in_user_table(message.chat.id):
        await message.answer(start_text, reply_markup=keyboard_start())
    else:
        await add_user(message.chat.first_name, message.chat.id)
        await message.answer(start_text, reply_markup=keyboard_start())


@router.message(CommandStart())
async def start(message: types.Message):
    await start_or_not_register_command(message)


@router.message(F.text.lower() == "узнать текущий курс доллара", UserInDatabase())
async def current_rate_message(message: types.Message):
    value = await get_current_rate_usd()
    date = message.date.now()
    await add_data_in_history(values=value,
                              user_id=message.chat.id,
                              date=date)
    await message.answer(f"По данным ЦБ РФ текущий курc доллара: {value} руб.")


@router.message(F.text.lower() == "настройка подписки", UserInDatabase())
async def setting_subscribe_message(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=setting_button_subscribe())


@router.message(F.text.lower() == "посмотреть историю запросов", UserInDatabase())
async def history_message(message: types.Message):
    history_list = await get_history(message.chat.id)
    if history_list:
        await message.answer("История ваших запросов:")
        histories = []
        for index, history in enumerate(history_list, 1):
            date = datetime.strftime(history[0], "%Y-%m-%d %H:%M:%S")
            value = history[1]
            histories.append(f"{index}. Дата и время: {date}, курс доллара: {value} руб.")

        await message.answer("\n".join(histories))
    else:
        await message.answer("Ой, ваша история запросов пустая!")

@router.message()
async def not_register_command(message: types.Message):
    await start_or_not_register_command(message)
