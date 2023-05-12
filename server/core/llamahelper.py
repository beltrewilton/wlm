from llama_cpp import Llama
from server.core.path_config import LLAMA_PATH_MODEL

llm = Llama(model_path=LLAMA_PATH_MODEL)


def call_llama(prompt: str):
    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]
    result = llm.create_chat_completion(messages=messages)
    # result = llm.create_completion(prompt=prompt)
    return result
