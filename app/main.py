from fastapi import FastAPI

from .routers import items

app = FastAPI()
app.include_router(items.router)


sToken = "hJqcu3uJ9Tn2gXPmxx2w9kkCkCE2EPYo"
sEncodingAESKey = "6qkdMrq68nTKduznJYO1A37W2oEgpkMUvkttRToqhUt"
sCorpID = "ww1436e0e65a779aee"

@app.get("/")
async def root(data):
    print(data)
    return {"message": "Hello FastAPI"}
