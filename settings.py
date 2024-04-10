from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sqlite3
from blockchain import BlockManager, Blockchain


connect = sqlite3.connect('DataChain.db')
block_manager = BlockManager(connect)
blockchain = Blockchain(block_manager)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates/")

