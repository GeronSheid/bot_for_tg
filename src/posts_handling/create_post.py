import os
from aiogram import Bot
from aiogram.types import Message, InputMediaPhoto, FSInputFile

from database.models import delete_image

async def create_post(bot: Bot, chat_id: str, dir: str):
    media = []
    filename = os.listdir(dir)[0]
    image_path = os.path.join(dir, filename)
    text_path = os.path.splitext(image_path)[0] + '.txt'
    text = ''
    if os.path.exists(text_path):
        with open(text_path, 'r', encoding='utf-8') as text_file:
            plain_text = text_file.read().strip()
            
            for tag in plain_text.split(' '):
                text = text + f'#{tag} '
    media_image = FSInputFile(path=image_path)
    media.append(InputMediaPhoto(media=media_image, caption=text))
    await bot.send_media_group(chat_id=chat_id, media=media)
    media = []
    os.remove(image_path)
    os.remove(text_path)

async def create_post_from_db(post, bot: Bot, chat_id: str):
    media = []
    author = post['author']
    tags = ''
    for tag in post.tags:
        tags = tags + f'#{tag} '
    text = f'Автор: {author}\n Тэги: {tags}\n'
    media.append(InputMediaPhoto(media=FSInputFile(path=post.url), caption=text))
    await bot.send_media_group(chat_id=chat_id, media=media)
    await delete_image(post.url)
    os.remove(post.url)