import os
from aiogram import Bot
from aiogram.types import Message, InputMediaPhoto

from posts_handling import create_post

dir = '/content/normal'

async def send_post(bot: Bot, chat_id: str):
    media = []
    for post in create_post(dir):
        with open(post.image, 'rb') as photo:
            media.append(InputMediaPhoto(photo, caption=post.caption))
    await bot.send_media_group(chat_id=chat_id, media=media)
    media = []
    for post in create_post(dir):
        os.remove(post.image)
        os.remove(post.text)


