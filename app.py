import uvicorn, asyncio
import starlette.status as status

from fastapi import Request, Form
from fastapi.responses import RedirectResponse

from settings import app, datab,templates, MAX_BLOCKS, BLOCK_PERIOD
from blockchain import verification, mine, create_first_block


collect_data_block = ''


@app.get("/generate")
async def generate_chain():
    global collect_data_block
    create_first_block()

    for _ in range(MAX_BLOCKS):
        await asyncio.sleep(BLOCK_PERIOD)
        data = collect_data_block
        mine(data)
        collect_data_block = "" 


@app.get("/")
async def view_chain(request: Request):
    chain = verification(datab.get_all())
    return templates.TemplateResponse('index.html', context={'request': request,
                                                             'len_blocks': datab.len_chain(),
                                                             'chains': chain})


@app.get("/mine")
async def mine_data(request: Request):
    return templates.TemplateResponse('mine_block.html', context={'request': request, 'len_blocks': datab.len_chain()})


@app.get("/{index_block}")
async def view_block(request: Request, index_block: int):
    return templates.TemplateResponse('view_block.html', context={'request': request,
                                                                  'index_block': index_block,
                                                                  'len_blocks': datab.len_chain(),
                                                                  'this_block': datab.get_block(index_block)})


@app.post("/mine/mining")
async def mining_data(data_from_block=Form(...), name_node=Form(...)):
    global collect_data_block
    collect_data_block += "[ %s ]: %s\n" % (name_node, data_from_block)
    return RedirectResponse(url="/mine", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/{index_block}/data")
async def data_block(request: Request, index_block):
    return templates.TemplateResponse('data_block.html', context={'request': request,
                                                                  'index_block': index_block,
                                                                  'data_this_block': datab.get_data_block(index_block)})


if __name__ == "__main__":
    config = uvicorn.Config("app:app", host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    server.run()
