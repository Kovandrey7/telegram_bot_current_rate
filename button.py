from aiogram import Bot, types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import BOT_TOKEN

bot = Bot(BOT_TOKEN)


def keyboard_start():
    kb = [
        [
            types.KeyboardButton(text="Узнать текущий курс доллара")
        ],
        [
            types.KeyboardButton(text="Настройка подписки")
        ],
        [
            types.KeyboardButton(text="Посмотреть историю запросов")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Нажмите на нужную кнопку"
    )
    return keyboard


def setting_button_subscribe():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Подписаться",
        callback_data="subscribe_on"),
        width=1
    )
    builder.row(types.InlineKeyboardButton(
        text="Отписаться",
        callback_data="subscribe_off"),
        width=1
    )
    return builder.as_markup()


async def del_reply_markup(call):
    await bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=None
    )
