#!/bin/bash
echo "Container Started"
export PYTHONUNBUFFERED=1
source /workspace/stable-diffusion-webui/venv/bin/activate
cd /workspace/stable-diffusion-webui
echo "starting stable diffusion"
python webui.py --port 3000 --api --xformers --ckpt /models/Stable-diffusion/Realistic_Vision_V2.0-inpainting.safetensors --vae-path /models/VAE/vae-ft-mse-840000-ema-pruned.safetensors &
cd /

echo "starting worker"
python -u handler.py