# Pinned environment for the fully-offline reproduction of
# "The AI Incident Disclosure Shadow." No API keys or network are required.
# This matches the audited Code Ocean capsule environment
# (https://doi.org/10.24433/CO.2340354.v1).
FROM python:3.12-slim

ARG DEBIAN_FRONTEND=noninteractive

# Minimal pinned analysis stack. No pandas, statsmodels, or network libraries
# are needed for the reproduction path.
RUN pip install -U --no-cache-dir \
    numpy==2.2.6 \
    scipy==1.14.1 \
    matplotlib==3.9.2 \
    pytest==8.3.3

WORKDIR /repo
COPY . /repo
ENV MPLBACKEND=Agg PYTHONHASHSEED=0
CMD ["bash", "reproduce.sh"]
