from fastapi import FastAPI

app = FastAPI(debug=True)

@app.post("/api/index/one")
async def index_one():
    pass

@app.post("/api/index/everything")
async def index_all():
    pass

@app.delete('/api/index')
async def index_clear():
    pass

@app.post("/api/chat")
async def chat():
    pass
