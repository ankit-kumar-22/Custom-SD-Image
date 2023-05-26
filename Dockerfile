FROM runpod/stable-diffusion:web-automatic-base-6.0.0

SHELL ["/bin/bash", "-c"]

ENV PATH="${PATH}:/workspace/stable-diffusion-webui/venv/bin"

WORKDIR /
COPY config_v1.json /workspace/stable-diffusion-webui/

RUN wget -O /workspace/stable-diffusion-webui/models/Stable-diffusion/Realistic_Vision_V2.0-inpainting.safetensors "https://huggingface.co/SG161222/Realistic_Vision_V2.0/resolve/main/Realistic_Vision_V2.0-inpainting.safetensors"

RUN mkdir -p /workspace/stable-diffusion-webui/models/ControlNet
RUN wget -O /workspace/stable-diffusion-webui/models/ControlNet/control_v11p_sd15_canny.pth "https://huggingface.co/Ryukz/Custom-SD-File-Requirements/resolve/main/control_v11p_sd15_canny.pth"


WORKDIR /workspace/stable-diffusion-webui/extensions
RUN git clone https://github.com/Mikubill/sd-webui-controlnet.git 

#VAE
RUN wget -O /workspace/stable-diffusion-webui/models/VAE/vae-ft-mse-840000-ema-pruned.safetensors "https://huggingface.co/Ryukz/Custom-SD-File-Requirements/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors"

#Embeddings
RUN wget -O /workspace/stable-diffusion-webui/embeddings/bad_prompt_version2.pt "https://huggingface.co/Ryukz/Custom-SD-File-Requirements/resolve/main/bad_prompt_version2.pt"
RUN wget -O /workspace/stable-diffusion-webui/embeddings/bad-hands-5.pt "https://huggingface.co/Ryukz/Custom-SD-File-Requirements/resolve/main/bad-hands-5.pt"
RUN wget -O /workspace/stable-diffusion-webui/embeddings/ng_deepnegative_v1_64t.pt "https://huggingface.co/Ryukz/Custom-SD-File-Requirements/resolve/main/ng_deepnegative_v1_64t.pt"
RUN wget -O /workspace/stable-diffusion-webui/embeddings/realisticvision-negative-embedding.pt "https://huggingface.co/Ryukz/Custom-SD-File-Requirements/resolve/main/realisticvision-negative-embedding.pt"

WORKDIR /
RUN pip install -U xformers
RUN pip install runpod
RUN pip install azure-storage-blob
RUN pip install azure-core


ADD handler.py .
ADD start.sh /start.sh
RUN chmod +x /start.sh

CMD [ "/start.sh" ]
