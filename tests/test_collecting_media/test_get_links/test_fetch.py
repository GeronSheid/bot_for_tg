import pytest
import aiohttp
from aioresponses import aioresponses
from collecting_media.get_links import fetch 

@pytest.mark.asyncio
async def test_fetch_success():
    url = 'http://example.com'
    expected_text = 'Hello, world!'

    with aioresponses() as m:
        m.get(url, body=expected_text)  
        async with aiohttp.ClientSession() as session:
            result = await fetch(session, url)
            assert result == expected_text

@pytest.mark.asyncio
async def test_fetch_failure():
    url = 'http://example.com'
    
    with aioresponses() as m:
        m.get(url, status=404)  # Мокируем GET-запрос, который вернёт ошибку 404
        async with aiohttp.ClientSession() as session:
            result = await fetch(session, url)
            assert result is None