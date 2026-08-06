# Code Ocean capsule environment — Paper 13 (offline, deterministic analysis).
# Base image served from Code Ocean's registry (same family used by our other capsules).
FROM registry.codeocean.com/codeocean/py-r:python3.12.8-R4.4.2-JupyterLab4.3.5-RStudiorstudio-server-2024.12.1-563-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive

# Pinned, minimal analysis stack. No pandas / statsmodels / network libraries are required:
# the capsule reads only frozen CSV/JSON assets and computes with numpy + scipy + matplotlib.
RUN pip install -U --no-cache-dir \
    numpy==2.2.6 \
    scipy==1.14.1 \
    matplotlib==3.9.2 \
    pytest==8.3.3
