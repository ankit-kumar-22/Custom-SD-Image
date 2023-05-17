#!/bin/bash
echo "Container Started"
export PYTHONUNBUFFERED=1
source /workspace/stable-diffusion-webui/venv/bin/activate
cd /workspace/stable-diffusion-webui
echo "starting stable diffusion"
python webui.py --port 3000 --api --xformers --ckpt /workspace/stable-diffusion-webui/models/Stable-diffusion/Realistic_Vision_V2.0-inpainting-fp16-no-ema.safetensors  --ui-settings-file /workspace/stable-diffusion-webui/config_v1.json  --allow-code True &
cd /

echo "starting worker"
python -u handler.py