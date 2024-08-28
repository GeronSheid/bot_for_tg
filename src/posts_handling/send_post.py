import os
from aiogram import Bot
from aiogram.types import Message, InputMediaPhoto, FSInputFile

from posts_handling.create_post import create_post

print(os.path.abspath(__file__))

async def send_post(bot: Bot, chat_id: str, dir: str):
    media = []
    async for posts in create_post(dir):
        for post in posts:
            photo_path = post['img']
            caption = post['text']
            photo = FSInputFile(path=photo_path)
            media.append(InputMediaPhoto(media=photo, caption=caption))
    await bot.send_media_group(chat_id=chat_id, media=media)
    media = []
    async for posts in create_post(dir):
        for post in posts: 
            os.remove(post['img'])
            os.remove(post['text_path'])


