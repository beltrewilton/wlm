import random
from llama_cpp import Llama
from server.core.path_config import LLAMA_PATH_MODEL

llm = Llama(model_path=LLAMA_PATH_MODEL, seed=random.randint(1, 100))


def call_llama(prompt: str):
    messages: list = [
        {
            "role": "user",
            "content": prompt
        }
    ]
    # result = llm.create_chat_completion(messages=messages, max_tokens=256)
    result: str = llm.create_completion(prompt=prompt, max_tokens=32, stream=True)
    # result = llm.create_completion(prompt=prompt)
    return result


if __name__ == "__main__":
    prompt: str = 'Write a code in Python for write text to a file'
    result: str = llm.create_completion(prompt=prompt, max_tokens=256, stream=True)
    for r in result:
        o = ''.join([c['text'] for c in r['choices']])
        print(o)
