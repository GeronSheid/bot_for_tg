from beanie import Document

class User(Document):
    tg_nickname: str
    tg_id: int