import re
import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs
from typing import Optional, List

async def fetch(session: aiohttp.ClientSession, url: str) -> Optional[str]:
    """Асинхронная функция для выполнения GET-запроса"""
    try:
        async with session.get(url, timeout=10) as response:
            response.raise_for_status()
            return await response.text()
    except asyncio.TimeoutError:
        print(f"Ошибка при запросе на URL: {url}")
        return None
    except aiohttp.ClientError as e:
        print(f"Ошибка при запросе: {e} на URL: {url}")
        return None

async def search_links(url: str, posts_amount: int) -> dict[str: str]:
    pagination: int = 0
    data_links_artists: dict[str: str] = {}

    while pagination < posts_amount:
        url = f"{url}&pid={pagination}"
        
        # Создаем асинхронную сессию
        async with aiohttp.ClientSession() as session:
            html = await fetch(session, url)

            if html:
                # Создаем объект BeautifulSoup для парсинга HTML
                soup = bs(html, "html.parser")
            
                container = soup.find('div', class_='thumbnail-container')

                if container:
                    img_containers = container.find_all('article', class_='thumbnail-preview')

                    for img_c in img_containers:
                        link = img_c.find('a', href=True)
                        
                        if link:
                            # Отправляем запрос по найденной ссылке
                            html_2 = await fetch(session, link['href'])

                            if html_2:
                                # Парсим HTML страницы с картинкой
                                soup_2 = bs(html_2, "html.parser")
                                
                                picture = soup_2.find('picture')
                                artist = soup_2.find('li', class_='tag-type-artist')
                                copyright = soup_2.find_all('li', class_='tag-type-copyright')

                                tags = []

                                if picture and artist:
                                    artist_name = artist.find_all('a', href=True)[1]
                                    img = picture.find('img')

                                    if img and artist_name :
                                        img_link = img['src']
                                        tags.append(re.sub(r'[^a-zA-Z0-9]', '', artist_name.text))

                                        for tag in copyright:
                                            tag = tag.find_all('a', href=True)[1]
                                            tags.append(re.sub(r'[^a-zA-Z0-9]', '', tag.text))
                                        
                                        if img_link.endswith(('png', 'jpg', 'jpeg')):
                                            data_links_artists[img['src']] = ' '.join(tags)
                            else:
                                print(f"Ошибка при запросе на URL: {link['href']}")
                        else:
                            print("Не найдена ссылка на изображение!")
                else:
                    print("Не найден контейнер с изображениями!")
            else:
                print(f"Ошибка при запросе на URL: {url}")
        
        # переходим на следующую страницу
        pagination += 42

    return data_links_artists

