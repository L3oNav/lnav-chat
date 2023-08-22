from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

import os

app = FastAPI()

origins = [
    "http://api.localhost",
]

@app.get("/")
async def main(request: Request):
    urls = [{"path": route.path, "name": route.name} for route in request.app.routes]
    return {
        "message": "Hello World",
        "env": os.getenv("ENVIROMENT", "development"),
        "urls": urls
    }
