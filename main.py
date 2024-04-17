import uvicorn
import starlette.status as status
from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse

from settings import app, templates, block_manager, blockchain
from blockchain import Transaction



@app.post("/start")
def start_generating_blocks():
    blockchain.run()


@app.get("/chainlength")
async def get_chain_length():
    return {'chain_length': block_manager.get_chain_length()}


@app.get("/transaction")
async def creating_transaction(request: Request):
    context = {
        'request': request, 
        'chain_length': block_manager.get_chain_length(),
    }
    return templates.TemplateResponse('creating_transaction.html', context=context)


@app.post("/transaction/create")
async def add_transaction(request: Request):
    transaction_data = await request.json()
    transaction = Transaction.create_by_data(**transaction_data)
    if not transaction.is_valid:
        raise HTTPException(status_code=401, detail="Invalid signature!")
    try:
        blockchain.create_transaction(transaction)
    except:
        raise HTTPException(status_code=405, detail="A block with such an index has already been created!")
    return RedirectResponse(url="/transaction", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/wallet/create")
async def creating_wallet(request: Request):
    private_key, public_key = blockchain.create_and_get_wallet()
    context = {
        'request': request, 
        'private_key': private_key,
        'public_key': public_key,
    }
    return templates.TemplateResponse('creating_wallet.html', context=context)


@app.get("/{block_index}/{transaction_index}")
async def viewing_transaction(request: Request, block_index, transaction_index):
    transaction_index = int(transaction_index)
    transactions = block_manager.get_transactions_by_block_index(block_index)
    if transactions.length <= transaction_index or transaction_index < 0:
        raise HTTPException(status_code=404, detail="There is no transaction with such an index")
    context = {
        'request': request, 
        'transaction_index': transaction_index,
        'transaction': transactions.get_by_id(transaction_index),
    }
    return templates.TemplateResponse('viewing_transaction.html', context=context)



@app.get("/{block_index}")
async def viewing_block(request: Request, block_index: int):
    chain_length = block_manager.get_chain_length()
    if block_index >= chain_length:
        raise HTTPException(status_code=404, detail="A block with such an index has not yet been created!")
    context = {
        'request': request,
        'chain_length': block_manager.get_chain_length(),
        'block': block_manager.get_by_index(block_index),
    }
    return templates.TemplateResponse('viewing_block.html', context=context)


@app.get("/")
async def viewing_blocks(request: Request):
    context = {
        'request': request,
        'blocks': block_manager.get_all(),
        'chain_length': block_manager.get_chain_length(),
    }
    return templates.TemplateResponse('viewing_blocks.html', context=context)



if __name__ == "__main__":
    config = uvicorn.Config("app:app", host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    server.run()

