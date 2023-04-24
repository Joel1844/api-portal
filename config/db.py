import pymongo
from pymongo import MongoClient, TEXT
from http import client
from dotenv import load_dotenv
import os

load_dotenv()

MongoConnection = os.getenv('DatabaseConnection')

Client = MongoClient(MongoConnection)

DbRed = Client["foodfit"]

CollectionRedSocial = DbRed["usuarios"] 

collectionportal = DbRed["portal"]
colletionvideo = DbRed["video"]