from aiogram import types, Router
from aiogram.filters import BaseFilter

from db.models.crud import check_user_in_user_table

router = Router()


class UserInDatabase(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return await check_user_in_user_table(message.chat.id)
