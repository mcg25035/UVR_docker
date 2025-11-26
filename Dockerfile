# 1. Base Image: NVIDIA CUDA 11.8 + Ubuntu 22.04
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

# 2. 安裝系統基礎工具 & 添加 Python 3.11 PPA
# [修正] 新增 libglu1-mesa (解決 pyglet 報錯)
RUN apt-get update && apt-get install -y \
    software-properties-common \
    wget \
    git \
    ffmpeg \
    libsndfile1 \
    rubberband-cli \
    libgl1 \
    libglib2.0-0 \
    pulseaudio \
    alsa-utils \
    libxrandr2 \
    libxinerama1 \
    libxcursor1 \
    libxi6 \
    x11-xserver-utils \
    libglu1-mesa \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update

# 3. 安裝 Python 3.11, Dev tools, 和最重要的 TKinter
RUN apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3.11-venv \
    python3.11-tk \
    python3.11-distutils \
    && rm -rf /var/lib/apt/lists/*

# 4. 安裝 Pip
RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python3.11 get-pip.py && \
    rm get-pip.py

# 5. 設定系統預設 Python 為 3.11
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# 6. 準備安裝依賴
COPY src/requirements.txt /tmp/requirements.txt

# 修正依賴
RUN sed -i 's/\r$//' /tmp/requirements.txt && \
    sed -i '/Dora==0.0.3/d' /tmp/requirements.txt && \
    sed -i '/sklearn/d' /tmp/requirements.txt && \
    sed -i 's/.*playsound.*/playsound==1.2.2/' /tmp/requirements.txt

# 7. 安裝 Python 套件
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip install --no-cache-dir --prefer-binary -r /tmp/requirements.txt
RUN pip install --no-cache-dir scikit-learn tqdm

# 8. 設定工作目錄
WORKDIR /app/src

CMD ["python", "UVR.py"]