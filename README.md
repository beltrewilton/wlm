# WML

> ✨ WhisperCpp + LlaMAcpp + Mimic3 = Voice Prompted Assistant *Experiment

https://github.com/beltrewilton/wlm/assets/8779994/af513a62-09df-484d-92a3-ed4a9827a9cb

## Quick preview
- [Test this Notebook](https://colab.research.google.com/drive/13mYSZzmv5Oxyh7yg95EghL7JWfqLgfZ0#scrollTo=wF7udCmWyR5u)

## Are you ready to play on your local machine??
- Python 3.10 / Conda / [Conda Miniforge](https://github.com/conda-forge/miniforge) 
- Create conda environment and activate
  ```shell
    conda create -n wlm-env python=3.10 -y
    conda activate wlm-env
  ```
- Install dependencies
  ```shell
  pip install numpy
  pip install uvicorn
  pip install python-multipart
  pip install fastapi
  pip install pydantic
  pip install cffi
  pip install pydub
  pip install pyngrok
  pip install nest-asyncio
  pip install aiocache
  ```
- Clone this repo 
  ```shell
    git clone https://github.com/beltrewilton/wlm.git
  ```
- Getting the models
  - Whisper Model 
    ```shell
      cd wlm/models
      ./download-ggml-model.sh base.en
    ```
  - LlaMA Model (already quantized to 4-bits q4_0 method) [Details about](https://github.com/ggerganov/llama.cpp)
    ```shell
      ./download-llama-ggml-model.sh
    ```
  - Mimic3 Voices 
   ```shell
     git clone https://github.com/MycroftAI/mimic3-voices.git
   ```
  - Install Mimic3 (Text to Speech Engine) [Detail about](https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mimic-tts/mimic-3)
      ```shell
        # -> go to wlm directory
        git clone https://github.com/mycroftAI/mimic3.git
        cp install-mimic3.sh mimic3/
        cd mimic3
        ./install-mimic3.sh 
      ```
    - Install mimic3 plugin (Python bridge)
      ```shell
         pip install mycroft_plugin_tts_mimic3
      ```
- Installing WhisperCpp Python bridge.
  ```shell
      pip install git+https://github.com/aarnphm/whispercpp.git -vv
   ```
- Installing (also) LlaMACpp Python bridge
  ```shell
     pip install --no-cache-dir llama-cpp-python
   ```
- Building web-client (React)
  ```shell
     cd wlm/client 
     npm install
     
     cp wlm/client/node_modules/@ricky0123/vad-web/dist/vad.worklet.bundle.min.js  wlm/client/
     cp wlm/client/node_modules/@ricky0123/vad-web/dist/*.onnx  wlm/client/
     cp wlm/client/node_modules/onnxruntime-web/dist/*.wasm  wlm/client/

     cd wlm/client; npm run build
  ```

- Doing some SSL configuration
  - First, Configure/install mkcert [See how to install on your local machine](https://github.com/FiloSottile/mkcert)
  - Next, generate keys:
  ```shell
   cd wlm/server
   ./generate_keys.sh
  ```
  

- Running the services!
```shell
   ./run-server.sh
```


