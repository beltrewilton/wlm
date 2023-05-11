from tempfile import NamedTemporaryFile
import base64
from mycroft_plugin_tts_mimic3 import Mimic3TTSPlugin
from server.core.path_config import MIMIC_VOICE_PATH


def audio_to_base64(file_path):
    try:
        with open(file_path, "rb") as fp:
            base64_audio: str = base64.b64encode(fp.read())
        return base64_audio
    except Exception as ex:
        print('###### ERROR HERE audio_to_base64 ', ex)
    finally:
        fp.close()


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
        print('###### ERROR HERE text_to_audio ', ex)
    finally:
        try:
            sound_file.close()
        except Exception as ex:
            print(ex)
