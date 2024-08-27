import asyncio
from .save_imgs import *
from .get_links import *
from typing import List

# urls для обхода и название для папки, на выходе будет дописано "img_*your text*"
urls: List[List[str]] = [
    ['https://gelbooru.com/index.php?page=post&s=list&tags=1girl+highres+anal', 'anal'],
    ['https://gelbooru.com/index.php?page=post&s=list&tags=1girl+highres+vaginal', 'classic'],
    ['https://gelbooru.com/index.php?page=post&s=list&tags=1girl+highres+oral', 'oral'],
]

async def main(url: str, dir: str) -> None:
    print("Загружаю ссылки...")
    links = await search_links(url, 50)

    if links:
        print("Ссылки загружены!", len(links))
        print("Загружаю изображения...")
        await download_images(links, dir)
        print("Изображения загружены!")
    else:
        print("Ссылки не найдены!")

async def start_parsing():
    for url in urls:
        dir = f"img_{url[1]}"
        await main(url[0], dir)

    return 

