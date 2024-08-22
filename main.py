import os

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
# from pymongo.server_api import ServerApi

from fastapi import FastAPI
from typing import Union
from dotenv import load_dotenv


load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI") #+ "&tlsInsecure=true"
client = AsyncIOMotorClient(MONGODB_URI)#, server_api=ServerApi('1'))
database = client.First
collection = database.get_collection("First")

app = FastAPI()




# Convert MongoDB document to Pydantic model
# def document_to_model(document) -> MyModel:
#     return MyModel(**document)


    # return {"Hello": "World"}

