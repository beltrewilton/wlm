import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
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
    # uvicorn.run(app, host="0.0.0.0", port=8770, ssl_keyfile=key_pem, ssl_certfile=public_pem)

    # Google Colab version.
    import uvicorn
    from pyngrok import ngrok
    import nest_asyncio

    ngrok_tunnel = ngrok.connect(8770)
    print('Public URL:', ngrok_tunnel.public_url)
    nest_asyncio.apply()
    uvicorn.run(app, port=8770)
