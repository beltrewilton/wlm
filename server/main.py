import os
import sys
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import server.core.app_main as core

IN_COLAB = os.getenv('IN_COLAB')
APP_PORT: int = 8770

base_path = os.getcwd()
key_pem = os.getcwd() + '/certs/key.pem'
public_pem = os.getcwd() + '/certs/public.crt'


app = FastAPI(ssl_keyfile=key_pem, ssl_certfile=public_pem)
app.include_router(core.router)


# @app.get('/')
# async def root():
#     return {'message': 'Message from root.'}


@app.get('/whereiam')
async def whereiam():
    s: str = 'Google Colab' if IN_COLAB else 'your poor machine'
    return {'you': f'Are in {s} baby'}


origins = [
    f"https://10.0.0.6:{APP_PORT}",
    f"https://localhost:{APP_PORT}",
]

if IN_COLAB == "True":
    # Google Colab version.
    import uvicorn
    from pyngrok import ngrok
    import nest_asyncio

    ngrok_tunnel = ngrok.connect(APP_PORT)
    print('Public URL:', ngrok_tunnel.public_url)
    nest_asyncio.apply()
    # uvicorn.run(app, port=APP_PORT)

    origins = [
        ngrok_tunnel.public_url,
    ]
else:
    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=APP_PORT, ssl_keyfile=key_pem, ssl_certfile=public_pem)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/", StaticFiles(directory="./client/build", html=True), name="build")
