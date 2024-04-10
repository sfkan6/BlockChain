import uvicorn
import starlette.status as status
from fastapi import Request, Form
from fastapi.responses import RedirectResponse

from settings import app, templates, block_manager, blockchain


@app.get("/start")
async def start_generating_blocks():
    if not blockchain.is_running:
        await blockchain.start()


@app.post("/transaction/create")
async def add_transaction(sender=Form(...), recipient=Form(...), amount=Form(...), message=Form(...), private_key=Form(...)):
    # blockchain.add_transaction(sender, recipient, amount, message, transaction_hash)
    blockchain.create_and_add_transaction(sender, recipient, amount, message, private_key)
    return RedirectResponse(url="/transaction", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/transaction")
async def creating_transaction(request: Request):
    chain_length = block_manager.get_chain_length()
    context = {
        'request': request, 
        'chain_length': chain_length
    }
    return templates.TemplateResponse('creating_transaction.html', context=context)


@app.get("/")
async def viewing_blocks(request: Request):
    blocks = block_manager.get_all()
    chain_length = block_manager.get_chain_length()
    context = {
        'request': request,
        'chain_length': chain_length,
        'blocks': blocks,
    }
    return templates.TemplateResponse('viewing_blocks.html', context=context)


@app.get("/{block_index}")
async def viewing_block(request: Request, block_index: int):
    chain_length = block_manager.get_chain_length()
    block = block_manager.get_by_index(block_index)
    context = {
        'request': request,
        'block_index': block_index,
        'chain_length': chain_length,
        'block': block,
    }
    return templates.TemplateResponse('viewing_block.html', context=context)


@app.get("/wallet/create")
async def creating_wallet(request: Request):
    private_key, public_key = blockchain.create_wallet()
    context = {
        'request': request, 
        'private_key': private_key,
        'public_key': public_key,
    }
    return templates.TemplateResponse('creating_wallet.html', context=context)


if __name__ == "__main__":
    config = uvicorn.Config("app:app", host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    server.run()

