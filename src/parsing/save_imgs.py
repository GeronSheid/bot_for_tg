import os
import aiohttp
import asyncio
import aiofiles
from PIL import Image
from io import BytesIO
from typing import List, Dict

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
                break  # Если удалось скачать изображение, выходим из цикла

        except (aiohttp.ClientError, asyncio.TimeoutError, Image.UnidentifiedImageError) as e:
            print(f"Не удалось загрузить изображение по ссылке {url}: {e}. Попытка {attempt} из {retries}")
            if attempt == retries:
                print(f"Превышено максимальное количество попыток для изображения {image_num}.")
                return
            await asyncio.sleep(2)  # Небольшая задержка перед следующей попыткой

async def download_video(session: aiohttp.ClientSession, video_info: Dict[str, any], folder: str, video_num: int, retries: int = 3) -> None:
    """Асинхронная функция для загрузки видео по ссылке и сохранения с повторами."""
    url = video_info["url"]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    for attempt in range(1, retries + 1):
        try:
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=1000)) as response:
                response.raise_for_status()

                # Всегда сохраняем как webm
                video_filename = f"video_{video_num}.webm"
                video_filepath = os.path.join(folder, video_filename)

                async with aiofiles.open(video_filepath, 'wb') as f:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        await f.write(chunk)
                print(f"Видео {video_num} успешно загружено.")
                break  # Если удалось скачать видео, выходим из цикла

        except aiohttp.ClientResponseError as e:
            print(f"Ошибка ответа от сервера при загрузке видео {video_num}: {e}. Попытка {attempt} из {retries}")
        except aiohttp.ClientError as e:
            print(f"Ошибка клиента при загрузке видео {video_num}: {e}. Попытка {attempt} из {retries}")
        except asyncio.TimeoutError as e:
            print(f"Время ожидания истекло при загрузке видео {video_num}: {e}. Попытка {attempt} из {retries}")
        except Exception as e:
            print(f"Неизвестная ошибка при загрузке видео {video_num}: {e}. Попытка {attempt} из {retries}")

        if attempt == retries:
            print(f"Превышено максимальное количество попыток для видео {video_num}.")
            return

        await asyncio.sleep(2)  # Небольшая задержка перед следующей попыткой

async def download_media(url_artist_map: List[Dict[str, any]], folder: str) -> None:
    """Асинхронная функция для загрузки изображений и видео из списка словарей."""
    # Создаем папку 'content', если она не существует
    content_folder = 'content'
    os.makedirs(content_folder, exist_ok=True)

    # Создаем папку внутри 'content', если она не существует
    full_folder_path = os.path.join(content_folder, folder)
    os.makedirs(full_folder_path, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, media_info in enumerate(url_artist_map, 1):
            if media_info["type"] == "image":
                tasks.append(download_image(session, media_info, full_folder_path, i))
            elif media_info["type"] == "video":
                tasks.append(download_video(session, media_info, full_folder_path, i))
            else:
                print(f"Неизвестный тип медиа: {media_info['type']}. Пропуск.")

        # Ожидаем завершения всех задач
        await asyncio.gather(*tasks)
