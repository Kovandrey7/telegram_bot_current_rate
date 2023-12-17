from aiogram import types, F, Router

from db.models.crud import check_subscribe, subscribe_on, subscribe_off

router = Router()


@router.callback_query(F.data == "subscribe_on")
async def subscribe_on_callback(callback: types.CallbackQuery):
    if await check_subscribe(callback.message.chat.id):
        await callback.message.answer(f"Вы уже подписаны на рассылку!")
        await callback.message.delete()
    else:
        await subscribe_on(callback.message.chat.id)
        await callback.message.answer(f"Вы подписаны на рассылку сообщений раз в день.")
        await callback.message.delete()


@router.callback_query(F.data == "subscribe_off")
async def subscribe_off_callback(callback: types.CallbackQuery):
    if await check_subscribe(callback.message.chat.id):
        await subscribe_off(callback.message.chat.id)
        await callback.message.answer(f"Вы успешно отписались от рассылки.")
        await callback.message.delete()

    else:
        await callback.message.answer(f"Вы не подписаны на рассылку.")
        await callback.message.delete()
