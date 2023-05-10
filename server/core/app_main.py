import os
import sys
import time

from fastapi import APIRouter, Depends, HTTPException, Security, Header, status
from fastapi import UploadFile, Response, WebSocket, WebSocketDisconnect
import asyncio

from server.core.whisperhelper import transcribe_helper
from server.core.llamahelper import call_llama
from server.core.mimichelper import text_to_audio
from server.core.schema import SoundMessage

router = APIRouter(prefix='/core', tags=['core'])

UNIT: int = 1000000000


@router.on_event("startup")
async def startup_event():
    print('Router: Init startup_event....')


@router.post("/transcribe_audio/{client_uuid}",)
async def transcribe_audio(msg: SoundMessage, client_uuid: str):
    try:
        start = time.time_ns()
        trs: str = transcribe_helper(msg.wavBuffer)
        end = time.time_ns()
        xtime = end - start
        print(f'Whisper time: {xtime/UNIT}s\n')
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
        print(f'Llama time: {xtime/UNIT}s\n')

        start = time.time_ns()
        tta: str = text_to_audio(res, voice_base=msg.voice_base)
        end = time.time_ns()
        xtime = end - start
        print(f'Mimic3 time: {xtime/UNIT}s\n')

        return {
            'text': res,
            'base64_audio': tta
        }
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
