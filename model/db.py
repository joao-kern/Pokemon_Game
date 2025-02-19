from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

class DB:
    def __init__(self):
        MONGO_URI = os.getenv("MONGO_URI")
        print("MONGO_URI carregado:", os.getenv("MONGO_URI"))
        if not MONGO_URI:
            raise ValueError("A variável de ambiente 'MONGO_URI' não está definida")
        
        self.client = MongoClient(MONGO_URI)
        self.db = self.client["DB_Pokemon_Trainers"]
        self.trainers = self.db["Trainers"]
