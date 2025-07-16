from pymongo.mongo_client import MongoClient
uri = "mongodb+srv://azharinmdb: azharinmdb07@cluster0.utgahb8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)

import os
import dotenv

dotenv.load_dotenv()

uri = os.getenv("DATABASE_URL", uri)

db = client.item_db

collection = db["item_collection"]

user_collection = db["user_collection"]