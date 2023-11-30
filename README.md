# Sync-NeRF integration for nerfstudio

## Start development

### Clone repository
```
git clone https://github.com/kazuwjn/syncnerf-nerfstudio.git
cd syncnerf-nerfstudio
```

### Create docker container
```
cd environments/wajin  # rename folder name
docker compose up -d
docker compose exec syncnerfstudio bash
```

## Installation

### Create environment
```
conda create --name syncnerf -y python=3.10
conda activate syncnerf
python -m pip install --upgrade pip
```

### Dependencies
Torch 2.0.1 with CUDA 11.8
```
pip install torch==2.0.1+cu118 torchvision==0.15.2+cu118 --extra-index-url https://download.pytorch.org/whl/cu118
conda install -c "nvidia/label/cuda-11.8.0" cuda-toolkit
```

tiny-cuda-nn
```
pip install ninja git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch
```

### Installing syncnerf-nerfstudio
```
cd syncnerf-nerfstudio
pip install --upgrade pip setuptools
pip install -e .
ns-install-cli
```

## Run

```
ns-train syncnerf-kplanes --data <data_folder>
```