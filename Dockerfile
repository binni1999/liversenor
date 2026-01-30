FROM python:3.8-slim-bookworm

# 1. Install system dependencies + Build Tools
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Install AWS CLI
RUN pip install --no-cache-dir awscli

WORKDIR /app

# 3. Copy and install requirements
COPY requirements.txt .
# Upgrading pip often solves "Exit Code 1" issues with newer packages
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "main.py"]