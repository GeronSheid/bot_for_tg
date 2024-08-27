import aiohttp
import os
import asyncio
from typing import Dict
from aiofiles import open as aioopen

async def download_image(session: aiohttp.ClientSession, url: str, folder: str, image_num: int) -> None:
    """Асинхронная функция для загрузки изображения по ссылке."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        async with session.get(url, headers=headers, timeout=20) as response:
            response.raise_for_status()

            # Создаем уникальное имя файла для изображения
            image_filename = f"image_{image_num}.jpg"
            image_filepath = os.path.join(folder, image_filename)

            # Асинхронно сохраняем изображение в файл
            async with aioopen(image_filepath, 'wb') as f:
                content = await response.read()
                await f.write(content)

    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        print(f"Не удалось загрузить изображение по ссылке {url}: {e}")

async def save_artist_name(folder: str, image_num: int, artist_name: str) -> None:
    """Асинхронная функция для сохранения имени артиста в текстовый файл."""
    try:
        # Создаем уникальное имя файла для имени артиста
        artist_filename = f"image_{image_num}.txt"
        artist_filepath = os.path.join(folder, artist_filename)

        # Асинхронно сохраняем имя артиста в файл
        async with aioopen(artist_filepath, 'w') as f:
            await f.write(artist_name)

    except OSError as e:
        print(f"Не удалось сохранить имя артиста {artist_name}: {e}")

async def download_images(url_artist_map: Dict[str, str], folder: str) -> None:
    """Асинхронная функция для загрузки изображений и сохранения имен артистов."""
    # Проверяем и создаем папку, если она не существует
    os.makedirs(folder, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, (url, artist_name) in enumerate(url_artist_map.items(), 1):
            tasks.append(download_image(session, url, folder, i))
            tasks.append(save_artist_name(folder, i, artist_name))
        
        # Ожидаем завершения всех задач
        await asyncio.gather(*tasks)