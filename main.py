from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app_blockchain.block import verification

import uvicorn, psycopg2, asyncio
import starlette.status as status

app = FastAPI()
for_data_block = ""
templates = Jinja2Templates(directory="templates/")
app.mount("/static", StaticFiles(directory="static"), name="static")

try:
    connect = psycopg2.connect("dbname=<dbname> user=<user>")
    connect.autocommit = True
    cur = connect.cursor()
    cur.execute("DROP TABLE chain")
    cur.execute("""CREATE TABLE chain (
                index serial PRIMARY KEY,
                timestamp timestamp,
                prev_hash text,
                hash text,
                data text,
                nonce integer
            )""")
    from app_blockchain import mine
except:
    print("DataBase is not connected")


def self_save(block):
    cur.execute(
        "INSERT INTO chain (index, timestamp, prev_hash, hash, data, nonce) VALUES (%s, %s, %s, %s, %s, %s)",
        (block.index, block.timestamp, block.prev_hash, block.hash, block.data, block.nonce))


def all_chain():
    cur.execute("SELECT * FROM chain")
    chain = verification(list(cur))
    return chain


def block_from(id):
    cur.execute("SELECT * FROM chain WHERE index=%s" % id)
    return cur.fetchone()


def data_from(id):
    cur.execute("SELECT data FROM chain WHERE index=%s" % id)
    return cur.fetchone()[0]


def len_blocks():
    cur.execute("SELECT MAX(index) as max FROM chain")
    length = 0 + cur.fetchone()[0] + 1
    return length


BLOCK_PERIOD = 8
MAX_BLOCKS = 100
@app.get("/generate")
async def generate_chain():

    i = 1
    global for_data_block
    while i < MAX_BLOCKS:
        data = for_data_block
        for_data_block = ""
        mine._mine_block(data)
        await asyncio.sleep(BLOCK_PERIOD)
        i += 1



@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request,
                                                             'len_blocks': len_blocks(),
                                                             'chains': all_chain()})


@app.get("/mine")
async def mine_data(request: Request):
    return templates.TemplateResponse('mine_block.html', context={'request': request, 'len_blocks': len_blocks()})


@app.get("/{index_block}")
async def view_block(request: Request, index_block: int):
    return templates.TemplateResponse('view_block.html', context={'request': request,
                                                                  'index_block': index_block,
                                                                  'len_blocks': len_blocks(),
                                                                  'this_block': block_from(index_block)})


@app.post("/mine/mining")
async def mining_data(data_from_block=Form(...), name_node=Form(...)):
    global for_data_block
    for_data_block += "[ %s ]: %s\n" % (name_node, data_from_block)
    return RedirectResponse(url="/mine", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/{index_block}/data")
async def data_block(request: Request, index_block):
    return templates.TemplateResponse('data_block.html', context={'request': request,
                                                                  'index_block': index_block,
                                                                  'data_this_block': data_from(index_block)})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000, workers=2)
