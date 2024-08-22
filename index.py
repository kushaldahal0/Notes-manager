from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from routes.route import notes


app = FastAPI()
app.mount("/static", StaticFiles(directory = "static"), name='static')
app.include_router(notes)