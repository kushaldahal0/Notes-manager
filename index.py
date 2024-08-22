from fastapi import FastAPI

from routes.route import notes

app = FastAPI()

app.include_router(notes)