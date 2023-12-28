from aiogram import Router
from aiogram.filters import ChatMemberUpdatedFilter, KICKED, MEMBER
from aiogram.types import ChatMemberUpdated

from db.models.user import change_user_status

router = Router()


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def process_user_blocked_bot(event: ChatMemberUpdated):
    await change_user_status(user_id=event.from_user.id)
    print(f"Пользователь {event.from_user.id} заблокировал бота")


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def process_user_unblocked_bot(event: ChatMemberUpdated, bot):
    await change_user_status(user_id=event.from_user.id)
    print(f"Пользователь {event.from_user.id} разблокировал бота")
    await bot.send_message(chat_id=event.from_user.id, text=f'{event.from_user.first_name}, Добро пожаловать обратно!')
