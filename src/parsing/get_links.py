import re
import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs
from typing import Optional, List, Dict


async def fetch(session: aiohttp.ClientSession, url: str) -> Optional[str]:
    """Асинхронная функция для выполнения GET-запроса."""
    try:
        async with session.get(url, timeout=10) as response:
            response.raise_for_status()
            return await response.text()
    except (asyncio.TimeoutError, aiohttp.ClientError) as e:
        print(f"Ошибка при запросе на URL {url}: {e}")
        return None


def parse_artist_and_tags(soup: bs) -> Dict[str, str]:
    """Парсинг имени художника и тегов."""
    # Парсим имя художника
    artist_tag = soup.find('li', class_='tag-type-artist')
    if artist_tag:
        artist_name = re.sub(r'[^a-zA-Z0-9]', '', artist_tag.find_all('a', href=True)[1].text)
    else:
        artist_name = "Unknown"

    # Парсим теги авторского права
    copyright_tags = soup.find_all('li', class_='tag-type-copyright')
    if copyright_tags:
        tags = [re.sub(r'[^a-zA-Z0-9]', '', tag.find_all('a', href=True)[1].text) for tag in copyright_tags]
    else:
        tags = ["Unknown"]

    return {'artist_name': artist_name, 'tags': tags}


def extract_content_link(soup: bs) -> Optional[Dict[str, str]]:
    """Извлечение ссылки на контент (видео или изображение) и определение типа контента."""
    picture = soup.find('picture')
    video = soup.find('video')

    if picture:
        img = picture.find('img')
        if img:
            return {'content_link': img['src'], 'type': 'image'}
    elif video:
        source = video.find_all('source')[1]
        if source:
            return {'content_link': source['src'], 'type': 'video'}
    
    return None


async def fetch_content_data(session: aiohttp.ClientSession, link: str) -> Optional[Dict[str, List[str]]]:
    """Получение данных о контенте с указанной ссылки."""
    html = await fetch(session, link)
    if not html:
        return None

    soup = bs(html, "html.parser")
    artist_and_tags = parse_artist_and_tags(soup)
    if not artist_and_tags:
        return None

    content_data = extract_content_link(soup)
    if content_data:
        content_link = content_data['content_link']
        if content_link.endswith(('png', 'jpg', 'jpeg', 'webm')):
            return {
                'url': content_link,
                'author': artist_and_tags['artist_name'],
                'tags': artist_and_tags['tags'],
                'type': content_data['type']
            }

    return None


async def search_links(url: str, content_type: str, posts_amount: int) -> List[Dict[str, str]]:
    """Поиск ссылок на изображения или видео по указанному URL."""
    data_links_artists: List[Dict[str, str]] = []
    pagination: int = 0

    async with aiohttp.ClientSession() as session:
        for _ in range(posts_amount):
            paginated_url = f"{url}&pid={pagination}"
            html = await fetch(session, paginated_url)
            if not html:
                print(f"Ошибка при запросе на URL: {paginated_url}")
                break

            soup = bs(html, "html.parser")
            container = soup.find('div', class_='thumbnail-container')
            if not container:
                print("Не найден контейнер с изображениями!")
                break

            img_containers = container.find_all('article', class_='thumbnail-preview')
            for img_c in img_containers:
                link = img_c.find('a', href=True)
                if link:
                    content_data = await fetch_content_data(session, link['href'])
                    if content_data:
                        data_links_artists.append(content_data)
                else:
                    print("Не найдена ссылка на изображение!")

            pagination += 42

    return [item for item in data_links_artists if item['type'] == content_type]
