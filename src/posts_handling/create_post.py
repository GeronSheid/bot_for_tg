import os
from aiogram import Bot
from aiogram.types import Message, InputMediaPhoto, FSInputFile

from database.models import delete_image

async def create_post_from_db(post, bot: Bot, chat_id: str):
    media = []
    if post['author'] == 'Unknown':
        author ='Неизвестен'
    else: 
        author = post['author']
    tags = ''
    if post['tags']:
        for tag in post.tags:
            tags = tags + f'#{tag} '
    text = f'Автор: {author}\n Тэги: {tags}\n'
    media.append(InputMediaPhoto(media=FSInputFile(path=post.url), caption=text))
    await bot.send_media_group(chat_id=chat_id, media=media)
    await delete_image(post.url)
    os.remove(post.url)

    # async def post_to_multiple_chanels(chanels, bot: Bot):
    #     for chanel in chanels:
            
        