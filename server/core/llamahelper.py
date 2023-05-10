from llama_cpp import Llama

LLAMA_PATH_MODEL: str = '/Users/beltre.wilton/apps/llama.cpp/models/7B/ggml-model-q4_0.bin'
llm = Llama(model_path=LLAMA_PATH_MODEL)


def call_llama(prompt: str):
    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]
    # result = llm.create_chat_completion(messages=messages)
    result = llm.create_completion(prompt=prompt)
    return result

