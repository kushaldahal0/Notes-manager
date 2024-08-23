import os
from dotenv import load_dotenv
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI") #+ "&tlsInsecure=true"
client = AsyncIOMotorClient(MONGODB_URI)#, server_api=ServerApi('1'))
database = client.First
collection = database.get_collection("First")

user_collection = database.get_collection("User")
