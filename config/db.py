import pymongo
from pymongo import MongoClient, TEXT
from dotenv import load_dotenv
import os

load_dotenv()

MongoConnection = os.getenv('DatabaseConnection')

db = os.getenv('DB_NAME')

Client = MongoClient(MongoConnection)

DbRed = Client[db]

CollectionRedSocial = DbRed["usuarios"] 

collectionportal = DbRed["portal"]
colletionvideo = DbRed["video"]
collentionlistim = DbRed["diario_libre"]
collentioninsta = DbRed["instagram_violence"]
# pruba = DbRed["prueba"]