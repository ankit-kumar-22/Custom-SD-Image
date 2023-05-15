FROM runpod/stable-diffusion:web-automatic-base-6.0.1

SHELL ["/bin/bash", "-c"]

ENV PATH="${PATH}:/workspace/stable-diffusion-webui/venv/bin"

WORKDIR /
COPY config_v1.json /workspace/stable-diffusion-webui/

# RUN wget -O model.safetensors https://civitai.com/api/download/models/5616
RUN wget -O /workspace/stable-diffusion-webui/models/Stable-diffusion/Realistic_Vision_V2.0-inpainting-fp16-no-ema.safetensors "https://huggingface.co/Ryukz/Custom-SD-Image/resolve/main/Realistic_Vision_V2.0-inpainting-fp16-no-ema.safetensors"

RUN mkdir -p /workspace/stable-diffusion-webui/models/ControlNet
RUN wget -O /workspace/stable-diffusion-webui/models/ControlNet/control_v11p_sd15_canny.pth "https://huggingface.co/Ryukz/Custom-SD-File-Requirements/resolve/main/control_v11p_sd15_canny.pth"


WORKDIR /workspace/stable-diffusion-webui/extensions
RUN git clone https://github.com/Mikubill/sd-webui-controlnet.git 

WORKDIR /

RUN pip install -U xformers
RUN pip install runpod


ADD handler.py .
ADD start.sh /start.sh
RUN chmod +x /start.sh

CMD [ "/start.sh" ]
