import os
import aiohttp
import asyncio
from PIL import Image
from io import BytesIO
from typing import List, Dict

from database.models import add_image

async def download_image(session: aiohttp.ClientSession, image_info: Dict[str, any], folder: str, image_num: int, retries: int = 3) -> None:
    """Асинхронная функция для загрузки изображения по ссылке и сохранения в формате WebP с повторами."""
    url = image_info["url"]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    for attempt in range(1, retries + 1):
        try:
            async with session.get(url, headers=headers, timeout=20) as response:
                response.raise_for_status()

                # Считываем содержимое изображения
                content = await response.read()

                # Открываем изображение с использованием PIL
                image = Image.open(BytesIO(content))

                # Создаем уникальное имя файла для изображения в формате WebP
                image_filename = f"image_{image_num}.webp"
                image_filepath = os.path.join(folder, image_filename)
                
                # Сохраняем изображение в формате WebP
                image.save(image_filepath, format="WEBP")

                table = {
                    'url': image_filepath,
                    'author': image_info['author'],
                    'tags': image_info['tags']
                }
                await add_image(table)
                break  # Если удалось скачать изображение, выходим из цикла

        except (aiohttp.ClientError, asyncio.TimeoutError, Image.UnidentifiedImageError) as e:
            print(f"Не удалось загрузить изображение по ссылке {url}: {e}. Попытка {attempt} из {retries}")
            if attempt == retries:
                print(f"Превышено максимальное количество попыток для изображения {image_num}.")
                return
            await asyncio.sleep(2)  # Небольшая задержка перед следующей попыткой

async def download_images(url_artist_map: List[Dict[str, any]], folder: str) -> None:
    """Асинхронная функция для загрузки изображений из списка словарей."""
    # Проверяем и создаем папку, если она не существует
    os.makedirs(folder, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, image_info in enumerate(url_artist_map, 1):
            tasks.append(download_image(session, image_info, folder, i))
        
        # Ожидаем завершения всех задач
        await asyncio.gather(*tasks)