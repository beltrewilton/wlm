import time

from fastapi import APIRouter, HTTPException, status

from server.core.whisperhelper import audio_to_text
from server.core.llamahelper import call_llama
from server.core.mimichelper import text_to_audio, say_hello
from server.core.schema import SoundMessage
from server.core.in_util import DUMMY_BASE64


router = APIRouter(prefix='/core', tags=['core'])
S_UNIT: int = 1000000000


@router.on_event("startup")
async def startup_event():
    print('Router: Init startup_event....')


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

        start = time.time_ns()
        tta: str = text_to_audio(res, voice_base=msg.voice_base)
        end = time.time_ns()
        xtime = end - start
        print(f'Mimic3 time: {xtime / S_UNIT}s\n')

        return {
            'text': res,
            'base64_audio': tta
        }
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))


@router.post('/say_hello')
async def _say_hello(msg: SoundMessage):
    return say_hello(voice_base=msg.voice_base)
