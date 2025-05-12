# 说明
通过 FastAPI 部署模型并暴露 http 接口  
最低 Python 环境版本为 3.9

# 使用方法
1. 在根目录创建虚拟环境
```bash
python -m venv fastApi
```
2. 激活虚拟环境  
- Windows（cmd）
```cmd
venv_name\Scripts\activate
```
- Windows（PowerShell）
```PowerShell
venv_name\Scripts\Activate.ps1
```
- macOS / Linux（bash/zsh）
```bash
source venv_name/bin/activate
```
- 退出虚拟环境（所有平台通用）
```bash
deactivate
```
3. 安装依赖工具
```bash
pip install FastAPI transformers python-dotenv uvicorn sse-starlette
```
- Windows  根据CUDA版本进行选择
```bash
# CUDA 12.8
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
# CUDA 12.6
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
# CUDA 11.8
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
- linux  根据CUDA版本进行选择
```bash
# CUDA 12.8
ppip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
# CUDA 12.6
pip3 install torch torchvision torchaudio
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