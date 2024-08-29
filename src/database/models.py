from typing import List
from beanie import Document

class User(Document):
    tg_nickname: str
    tg_id: int

class Image(Document):
    url: str
    author: str
    tags: List[str]

async def add_image(data: Image):
    image = Image(**data)
    await image.insert()

async def get_image(url: str):
    return await Image.find_one(Image.url == url)
    