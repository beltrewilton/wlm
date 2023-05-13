import os
import base64
from tempfile import NamedTemporaryFile
from pydub import AudioSegment
from mycroft_plugin_tts_mimic3 import Mimic3TTSPlugin
from server.core.path_config import MIMIC_VOICE_PATH


def base64_to_audio(sb64_wav: str):
    try:
        wavdec: bytes = base64.b64decode(sb64_wav)
        sound_file = NamedTemporaryFile(mode="wb")
        sound_file.write(wavdec)
        audio_file = AudioSegment.from_file(sound_file.name)
        audio_file.export(sound_file.name, format="wav")
        return sound_file
    except Exception as ex:
        raise ex


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
    base: str = voice_base.split('#')[0]
    speaker: str = ''
    if '#' in voice_base:
        speaker = voice_base.split('#')[1]

    print('speaker', speaker)
    print('base', base)

    dirs = f'{MIMIC_VOICE_PATH}/{base}'.split('#')[0]
    print(dirs)
    try:
        config = {
            'voice': f'en_US/{base}',
            'language': 'en_US',
            'voices_directories': [dirs],
            'voices_url_format': '',
            'speaker': speaker,
            'noise_scale': 0.667,
            'noise_w': 1.0,
            'length_scale': 1.0,   # how fast speech < 1, how slow > 1
        }
        m = Mimic3TTSPlugin(lang='en_US', config=config)
        sound_file = NamedTemporaryFile()
        # text: str = ' '.join([t['text'] for t in llm_response['choices']])
        # text: str =' '.join([t['message']['content'] for t in llm_response['choices']])
        m.get_tts(llm_response, sound_file.name)
        return audio_to_base64(sound_file.name)
    except Exception as ex:
        print('###### ERROR HERE text_to_audio ', ex)
    finally:
        try:
            sound_file.close()
        except Exception as ex:
            print(ex)


def say_hello(voice_base: str):
    # llm_response = {
    #     'choices': [{
    #        'message': { 'content': '<speak><s><prosody rate="10%">Ummmm</prosody></s><break time="1s" /> <s>let me check, please wait a couple of seconds</s></speak>' }
    #     }]
    # }
    text: str = '<speak><s><prosody rate="10%">Ummmm</prosody></s><break time="1s" /> <s>let me check, please wait a couple of seconds</s></speak>'
    return text_to_audio(text, voice_base)


if __name__ == "__main__":
    llm_response = {
        'choices': [{
            'text': 'In natural language processing, a hallucination is often defined as "generated content that is nonsensical or unfaithful to the provided source content". Depending on whether the output contradicts the prompt or not they could be divided to closed-domain and open-domain respectively'
        }]
    }
    try:
        b64_wav = text_to_audio(
            llm_response,
            voice_base='vctk_low')
        sound_file = base64_to_audio(b64_wav)
        os.system(f'ffplay {sound_file.name} -autoexit')
    except Exception as ex:
        print(ex)
    finally:
        sound_file.close()
