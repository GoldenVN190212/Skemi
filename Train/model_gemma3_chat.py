# model_qwen3.py
from ollama import chat

# Chatbot xịn Qwen3-VL:4B
def call_qwen3_block(messages):
    """
    messages: list of dict {"role": "user"/"system", "content": "..."}
    Trả về text chatbot
    """
    resp = chat(model="qwen3-vl:4b", messages=messages)
    return resp.message.content  # chỉ lấy text
