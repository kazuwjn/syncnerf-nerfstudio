# Temporal Interpolation is All You Need for Dynamic Neural Radiance Fields

## Installation

Torch 2.0.1 with CUDA 11.8
```
conda create --name syncnerf -y python=3.10
conda activate syncnerf
python -m pip install --upgrade pip
pip install torch==2.0.1+cu118 torchvision==0.15.2+cu118 --extra-index-url https://download.pytorch.org/whl/cu118
conda install -c "nvidia/label/cuda-11.8.0" cuda-toolkit
pip install ninja git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch
https://github.com/kazuwjn/syncnerf-nerfstudio.git
cd syncnerf-nerfstudio
pip install --upgrade pip setuptools
pip install -e .
ns-install-cli
```

## Run

```
ns-train syncnerf-kplanes --data <data_folder>
```