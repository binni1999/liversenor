# Use a modern, supported base image
FROM python:3.8-slim-bookworm

# 1. Install system dependencies
# We combine update and install, and clean up to keep the image small
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# 2. Install AWS CLI via pip (more reliable than apt in slim images)
RUN pip install --no-cache-dir awscli

# 3. Set up workspace
WORKDIR /app

# 4. Copy requirements first (better for build caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the code
COPY . .

CMD ["python3", "main.py"]