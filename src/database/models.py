from typing import List
from beanie import Document

class User(Document):
    tg_nickname: str
    tg_id: int

async def add_user(data: User):
    user = User(**data)
    await user.insert()

class Image(Document):
    url: str
    author: str
    type: str
    tags: List[str]

async def add_image(data: Image):
    image = Image(**data)
    await image.insert()

async def get_image(url: str):
    return await Image.find_one(Image.url == url)

async def delete_image(url: str):
    return await Image.delete(Image.url == url)