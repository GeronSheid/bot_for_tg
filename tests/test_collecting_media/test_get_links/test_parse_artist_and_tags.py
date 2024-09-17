import pytest
from bs4 import BeautifulSoup
from collecting_media.get_links import parse_artist_and_tags

def test_parse_artist_and_tags_with_artist_and_tags():
    # Мокируем HTML-структуру с тегами художника и автора
    html = """
    <ul>
        <li class="tag-type-artist"><a href="#">Artist:</a> <a href="#">JohnDoe</a></li>
        <li class="tag-type-copyright"><a href="#">Copyright:</a> <a href="#">BrandX</a></li>
    </ul>
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # Ожидаемый результат
    expected = {
        'artist_name': 'JohnDoe',
        'tags': ['BrandX']
    }
    
    # Выполняем функцию
    result = parse_artist_and_tags(soup)
    
    # Сравниваем результат с ожидаемым
    assert result == expected

def test_parse_artist_and_tags_without_artist():
    # Мокируем HTML без тега художника
    html = """
    <ul>
        <li class="tag-type-copyright"><a href="#">Copyright:</a> <a href="#">BrandX</a></li>
    </ul>
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # Ожидаемый результат
    expected = {
        'artist_name': 'Unknown',
        'tags': ['BrandX']
    }
    
    result = parse_artist_and_tags(soup)
    
    assert result == expected

def test_parse_artist_and_tags_without_tags():
    # Мокируем HTML без тега художника и автора
    html = """
    <ul>
        <li class="other-tag"><a href="#">Other:</a> <a href="#">NoArtistNoTags</a></li>
    </ul>
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    expected = {
        'artist_name': 'Unknown',
        'tags': ['Unknown']
    }
    
    result = parse_artist_and_tags(soup)
    
    assert result == expected

