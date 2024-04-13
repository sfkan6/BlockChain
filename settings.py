from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from blockchain import BlockManager, Blockchain 
import sqlite3


connect = sqlite3.connect('DataChain.db')
block_manager = BlockManager(connect)
blockchain = Blockchain(block_manager)


templates = Jinja2Templates(directory="templates/")


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


