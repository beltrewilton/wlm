import time

from fastapi import APIRouter, HTTPException, status, WebSocket

from aiocache import Cache
import asyncio

from server.core.whisperhelper import audio_to_text
from server.core.llamahelper import call_llama
from server.core.mimichelper import text_to_audio, say_hello
from server.core.schema import SoundMessage
from server.core.ws.connectionmanager import ConnectionManager, send_periodically


router = APIRouter(prefix='/core', tags=['core'])
S_UNIT: int = 1000000000
myvar = Cache(Cache.MEMORY)


@router.on_event("startup")
async def startup_event():
    print('Router: Init startup_event....')
    await myvar.set('sharable', {'char': None})
    await myvar.set('client_uuid_list', list())
    await myvar.set('sharable_per_client', list())


@router.post("/transcribe_audio/{client_uuid}",)
async def transcribe_audio(msg: SoundMessage, client_uuid: str):
    try:
        start = time.time_ns()
        trs: str = audio_to_text(msg.wavBuffer)
        end = time.time_ns()
        xtime = end - start
        print(f'Whisper time: {xtime / S_UNIT}s\n')
        return trs
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))


@router.post("/hit_llama/{client_uuid}",)
async def hit_llama(msg: SoundMessage, client_uuid: str):
    try:
        start = time.time_ns()
        res: str = call_llama(msg.transcript)
        end = time.time_ns()
        xtime = end - start
        print(f'Llama time: {xtime / S_UNIT}s\n')

        client_uuid_list = await myvar.get('client_uuid_list')
        out: list = []
        for idx, r in enumerate(res):   # generator -> token by token ?
            chr: str = ''.join([c['text'] for c in r['choices']])
            chr = chr.replace('\n', '').replace('\r', '')
            out.append(chr)
            # print(o)
            sharable = {'chr': chr, 'id': r['id']}
            await myvar.set('sharable', sharable)
            sharable_per_client = await myvar.get('sharable_per_client')
            for id in client_uuid_list:
                if id == client_uuid:
                    sharable_per_client.append({'client_uuid': id, 'sharable': sharable})
                    await myvar.set('sharable_per_client', sharable_per_client)

        start = time.time_ns()
        tta: str = text_to_audio(''.join(out), voice_base=msg.voice_base)
        end = time.time_ns()
        xtime = end - start
        print(f'Mimic3 time: {xtime / S_UNIT}s\n')

        return {
            'text': ''.join(out),
            'base64_audio': tta
        }
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))


@router.post('/say_hello')
async def _say_hello(msg: SoundMessage):
    return say_hello(voice_base=msg.voice_base)


@router.websocket("/ws/{client_uuid}")
async def websocket_endpoint(websocket: WebSocket, client_uuid: str):
    manager = ConnectionManager()
    await manager.connect(websocket, client_uuid, myvar=myvar)
    await websocket.send_json({'Welcome nigga':  client_uuid})
    print('Wating for new events [send_periodically] ....')
    await asyncio.create_task(send_periodically(websocket, manager, client_uuid, 0, myvar=myvar))
