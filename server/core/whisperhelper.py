import base64
from tempfile import NamedTemporaryFile
from whispercpp import Whisper
from pydub import AudioSegment
from server.core.path_config import WHISPER_PATH

w = Whisper.from_pretrained(WHISPER_PATH)


def audio_to_text(raw):
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
