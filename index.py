from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from routes.route import notes
from routes.user import user


app = FastAPI()
app.mount("/static", StaticFiles(directory = "static"), name='static')
app.include_router(notes)
app.include_router(user)