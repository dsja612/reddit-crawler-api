from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time

from . import query

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.get("/users/{username}")
async def main(username: str):
    start = time.time()
    print("start")
    try:
        # return await query.main(username)
        item = await query.main(username)
        end = time.time()
        print(end - start)
        return item
    except Exception as err:
        raise err

@app.get('/')
async def index():
    return "Hello!"