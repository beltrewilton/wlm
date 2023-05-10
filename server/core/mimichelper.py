import sys
import os
from tempfile import NamedTemporaryFile
import base64
from pydub import AudioSegment
from mycroft_plugin_tts_mimic3 import Mimic3TTSPlugin

MIMIC_VOICE_PATH: str = '/Users/beltre.wilton/.local/share/mycroft/mimic3/voices/en_US'


def audio_to_base64(file_path):
    # audio_file = AudioSegment.from_file(file_path)
    base64_audio: str = base64.b64encode(open(file_path, "rb").read())
    return base64_audio


def text_to_audio(llm_response, voice_base: str):
    base: str = voice_base
    try:
        config = {
            'voice': f'en_US/{base}',
            'language': 'en_US',
            'voices_directories': [f'{MIMIC_VOICE_PATH}/{base}'],
            'voices_url_format': '',
            'speaker': 'male',
            'noise_scale': 0.667,
            'noise_w': 1.0,
        }
        m = Mimic3TTSPlugin(lang='en_US', config=config)
        sound_file = NamedTemporaryFile()
        text: str = ' '.join([t['text'] for t in llm_response['choices']])
        # text: str = '<speak><s><prosody rate="10%">Ummmm</prosody></s><break time="1s" /> <s>let me check, please wait a couple of seconds</s></speak>'
        m.get_tts(text, sound_file.name)
        return audio_to_base64(sound_file.name)
    except Exception as ex:
        print(ex)
    finally:
        sound_file.close()
