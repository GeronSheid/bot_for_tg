import asyncio
from .save_imgs import *
from .get_links import *
from typing import List

async def start_pars(parsing_info: List[str], quantity: int) -> None:
    print("Загружаю ссылки...")
    url = parsing_info[0]
    folder_name = parsing_info[1]
    content_type = 'video' if folder_name.endswith('videos') else 'image'    
    content_info = await search_links(url, content_type, quantity)

    if content_info:
        print("Ссылки загружены!", len(content_info))
        print("Загружаю изображения...")
        await download_media(content_info, folder_name)
        print("Изображения загружены!")
    else:
        print("Ссылки не найдены!")


