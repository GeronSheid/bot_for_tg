import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

from beanie import Document, init_beanie

load_dotenv()

MONGO_USERNAME = os.getenv('USER')
MONGO_PASS = os.getenv('PASSWORD')
MONGO_DB_NAME = os.getenv('DB_NAME')


class User(Document):
    name: str
    surname: str



async def init_db():
    client = AsyncIOMotorClient(f'mongodb+srv://{MONGO_USERNAME}:{MONGO_PASS}@cluster0.3o6dn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
    try:
        await init_beanie(database=client[MONGO_DB_NAME], document_models=[User])
        print("Beanie инициализирован успешно")
    except Exception as e:
        print(f'Ошибка при инициализации db: {e}')