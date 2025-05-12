from fastapi import FastAPI
from transformers import AutoModelForCausalLM, AutoTokenizer
from dotenv import load_dotenv
import os
import shlex
import torch
import time
from sse_starlette.sse import EventSourceResponse


# 加载 .env 文件
load_dotenv()

# 获取模型路径
model_path = os.getenv("MODEL_PATH")
if not model_path:
    raise ValueError("环境变量 MODEL_PATH 未设置")

model_path = shlex.split(model_path)[0]

app = FastAPI()

# 加载 tokenizer （分词器）
tokenizer = AutoTokenizer.from_pretrained(model_path)

# 加载模型并移动到可用设备（GPU/CPU）
device = "cuda" if torch.cuda.is_available() else "cpu"
model = AutoModelForCausalLM.from_pretrained(model_path).to(device)


@app.get("/generate")
async def generate_text(prompt: str):
    # 使用 tokenizer 编码输入的 prompt
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    # 使用模型生成文本
    outputs = model.generate(inputs["input_ids"], max_length=150)

    # 解码生成的输出
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return {"generated_text": generated_text}


# 流式生成接口
@app.get("/stream_generate")
async def stream_generate(prompt: str):
    # 使用 tokenizer 编码输入的 prompt
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    # 使用模型生成文本
    output = model.generate(inputs["input_ids"], max_length=150, do_sample=True)

    # 解码生成的输出
    def event_generator():
        text = tokenizer.decode(output[0], skip_special_tokens=True)
        for char in text:
            yield {"data": char}
            time.sleep(0.05)  # 可调整速度
        yield {"data": "[END]"}

    return EventSourceResponse(event_generator())