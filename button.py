from aiogram import Bot, types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import BOT_TOKEN

bot = Bot(BOT_TOKEN)


def button_start():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Узнать текущий курс доллара",
        callback_data="current_rate"),
        width=1
    )
    builder.row(types.InlineKeyboardButton(
        text="Настройка подписки",
        callback_data="setting_subscribe"),
        width=1
    )
    builder.row(types.InlineKeyboardButton(
        text="Посмотреть историю запросов",
        callback_data="history"),
        width=1
    )
    return builder.as_markup()


def button_else():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Узнать текущий курс доллара",
        callback_data="current_rate"),
        width=1
    )
    builder.row(types.InlineKeyboardButton(
        text="Настройка подписки",
        callback_data="setting_subscribe"),
        width=1
    )
    builder.row(types.InlineKeyboardButton(
        text="Посмотреть историю запросов",
        callback_data="history"),
        width=1
    )
    return builder.as_markup()


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
