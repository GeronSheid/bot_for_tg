from aiogram import F, Bot, Router, types

join_spam_router = Router()


@join_spam_router.chat_join_request()
async def spam_to_new_masturbater(request: types.ChatJoinRequest, bot: Bot):

    user = request.from_user
    chat = request.chat
    await bot.approve_chat_join_request(chat_id=chat.id, user_id=user.id, request_timeout=5000)
    await bot.send_message(user.id, "Привет! \n Cпасибо что подписался, приятного фап-фап your piska.")