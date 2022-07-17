from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    try:
        return await query.main(username)
    except Exception as err:
        raise err
