# WML

> ✨ WhisperCpp + LlaMAcpp + Mimic3 = Voice Prompted Assistant *Experiment



This Python class was designed for scraping comments of users of hotels of **Punta Cana**, but not limited,
may be used for scrap another useful data from others hotels or restaurants. 


<video src='https://github.com/beltrewilton/wlm/raw/main/vid/wlm-demo-vid.MP4' width=180></video>


## Are you ready for this ?
- Python 3.10 / Conda / [Conda Miniforge](https://github.com/conda-forge/miniforge) 
- Create conda environment and activate
  ```shell
    conda create -n wlm-env python=3.10 -y
    conda activate wlm-env
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
  - LlaMA Model (already quantized to 4-bits q4_0 method) [Details](https://github.com/ggerganov/llama.cpp)
    ```shell
      ./download-llama-ggml-model.sh
    ```
  - Mimic3 Voices 
   ```shell
     git clone https://github.com/MycroftAI/mimic3-voices.git
   ```
  - Install Mimic3 (Text to Speech Engine) [Detail](https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mimic-tts/mimic-3)
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

- mkcert [See how to install on your local machine](https://github.com/FiloSottile/mkcert)
- 

## Example
```shell
python scraper.py --numhotel=10 --city=Florianopolis --maxcommentsperpage=10 --lang=Portuguese --outfile=my_dummy_file_data --verbose=1

```