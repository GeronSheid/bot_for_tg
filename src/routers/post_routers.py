import os
from aiogram import Router, Bot
from aiogram.types import Message, InputMediaPhoto

from lib.create_post import create_post

dir = '/content/normal'
post_router = Router()

@post_router.message()
async def send_post(message: Message, bot: Bot):
    media = []
    for post in create_post(dir):
        with open(post.image, 'rb') as photo:
            media.append(InputMediaPhoto(photo, caption=post.caption))
    await bot.send_media_group(chat_id='', media=media)
    media = []
    for post in create_post(dir):
        os.remove(post.image)
        os.remove(post.text)


