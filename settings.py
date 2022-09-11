from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from bd import DataB


app = FastAPI()
datab = DataB()
templates = Jinja2Templates(directory="templates/")
app.mount("/static", StaticFiles(directory="static"), name="static")


BLOCK_PERIOD = 8
MAX_BLOCKS = 100



