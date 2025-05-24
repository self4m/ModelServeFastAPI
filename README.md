# 没有针对性的优化内容，所以模型回答比较慢，只是提供一个示例
# 说明
通过 FastAPI 部署模型并暴露 http 接口  
最低 Python 环境版本为 3.9

# 安装方法
1. 在根目录创建虚拟环境
```bash
python -m venv ModelServeFastAPI
```
2. 激活虚拟环境  
- Windows（cmd）
```cmd
ModelServeFastAPI\Scripts\activate
```
- Windows（PowerShell）
```PowerShell
ModelServeFastAPI\Scripts\Activate.ps1
```
- macOS / Linux（bash/zsh）
```bash
source ModelServeFastAPI/bin/activate
```
- 退出虚拟环境（所有平台通用）
```bash
deactivate
```
3. 安装依赖工具
```bash
pip install FastAPI transformers python-dotenv uvicorn sse-starlette
```
- Windows linux 根据CUDA版本进行选择
```bash
# CUDA 12.8
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
# CUDA 12.6
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
# CUDA 11.8
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

- macOS
```bash
pip3 install torch torchvision torchaudio
```
4. 修改.env文件  
将 .env 文件中的 `MODEL_PATH` 为你设备上符合 `safetensors` 文件格式的模型路径
例如：
>MODEL_PATH=/Users/username/Downloads/DeepSeek-R1-Distill-Qwen-1.5B
5. 启动项目  
项目服务端口为： 127.0.0.1:8888  
默认仅限本机进行访问，如果有需要可以修改启动文件或者使用命令行启动
- 双击启动
```
windows 双击 start.bat
macOS   双击 start.command
```
- 命令行启动  
```bash
uvicorn start:app --reload --host 127.0.0.1 --port 8888
```

# 使用方法
以下是提供的两个接口信息

| 接口信息          | /generate (普通生成)                          | /stream_generate (流式生成)                     |
|-------------------|----------------------------------------------|-----------------------------------------------|
| **请求方法**      | GET                                          | GET                                           |
| **请求参数**      | prompt: str (输入提示词)                     | prompt: str (输入提示词)                      |
| **响应格式**      | JSON (完整生成结果)                          | Server-Sent Events (流式数据块)               |
| **生成方式**      | 一次性完整生成                               | 逐字符流式输出                                |
| **延迟表现**      | 等待全部生成完成后返回                       | 实时逐步返回结果                              |
| **适用场景**      | 短文本快速生成                               | 长文本/需要实时显示的场景                     |
| **技术实现**      | 直接调用model.generate()                     | 使用生成器函数逐字符yield                     |
| **性能特点**      | 整体处理时间较短                             | 总时间较长但首字符响应快                      |
| **客户端处理**    | 一次性接收完整结果                           | 需要处理流式数据                              |
| **参数控制**      | 固定max_length=150                           | 额外支持do_sample=True                        |
| **响应示例**      | `{"generated_text": "完整生成内容..."}`      | 多次返回：`{"data":"字"}...{"data":"[END]"}`  |
| **网络要求**      | 常规HTTP请求                                 | 需要保持持久连接                              |
