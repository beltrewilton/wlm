import os
import base64
from tempfile import NamedTemporaryFile

from whispercpp import Whisper
from pydub import AudioSegment

WHISPER_PATH: str = '/Users/beltre.wilton/apps/whisper.cpp/models/ggml-base.en.bin'
w = Whisper.from_pretrained(WHISPER_PATH)


def transcribe_helper(raw):
    try:
        wavdec: bytes = base64.b64decode(raw)
        sound_file = NamedTemporaryFile(mode="wb")
        sound_file.write(wavdec)
        audio_file = AudioSegment.from_file(sound_file.name)
        audio_file = audio_file.set_sample_width(2)
        audio_file.export(sound_file.name, format="wav")
        text: str = w.transcribe_from_file(sound_file.name)
        return text
    except Exception as ex:
        raise ex
    finally:
        sound_file.close()
