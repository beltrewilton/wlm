LLAMA_PATH_MODEL: str = '/content/wlm/models/ggml-model-q4_0.bin'
WHISPER_PATH: str = '/content/wlm/models/ggml-base.en.bin'
MIMIC_VOICE_PATH: str = '/content/mimic3-voices/voices/en_US'

# import sys
#
# IN_COLAB = bool(os.getenv('IN_COLAB'))
#
#
# if IN_COLAB:
#     LLAMA_PATH_MODEL: str = '/content/wlm/models/ggml-model-q4_0.bin'
#     WHISPER_PATH: str = '/content/wlm/models/ggml-base.en.bin'
#     MIMIC_VOICE_PATH: str = '/content/mimic3-voices/voices/en_US'
# else:
#     LLAMA_PATH_MODEL: str = '/Users/beltre.wilton/apps/llama.cpp/models/7B/ggml-model-q4_0.bin'
#     WHISPER_PATH: str = '/Users/beltre.wilton/apps/whisper.cpp/models/ggml-base.en.bin'
#     MIMIC_VOICE_PATH: str = '/Users/beltre.wilton/.local/share/mycroft/mimic3/voices/en_US'
