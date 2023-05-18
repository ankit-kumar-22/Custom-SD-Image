FROM runpod/stable-diffusion:web-automatic-base-6.0.0

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


WORKDIR /workspace/stable-diffusion-webui
RUN git reset --hard a9eab236d7e8afa4d6205127904a385b2c43bb24



WORKDIR /
RUN pip install gradio==3.23
RUN pip install -U xformers
RUN pip install runpod
RUN pip install azure-storage-blob
RUN pip install azure-core
RUN pip install playwright
RUN pip install pytest-playwright
RUN playwright install chromium
RUN apt-get update && apt-get install -y libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libatspi2.0-0 libxcomposite1 libxdamage1 libgbm1 && rm -rf /var/lib/apt/lists/*

EXPOSE 3000

ADD handler.py .
ADD fn_index.py .
ADD start.sh /start.sh
RUN chmod +x /start.sh

CMD [ "/start.sh" ]
