import os
import sys

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
import time

import server.core.app_main as core


base_path = os.getcwd()
key_pem = os.getcwd() + '/certs/key.pem'
public_pem = os.getcwd() + '/certs/public.crt'

origins = [
    "https://10.0.0.6:8300",
    "https://localhost:8300",
]

app = FastAPI(ssl_keyfile=key_pem, ssl_certfile=public_pem)

app.include_router(core.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def root():
    return {'message': 'Message from root.'}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8770, ssl_keyfile=key_pem, ssl_certfile=public_pem)
