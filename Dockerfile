# FROM python:3.11-slim

# WORKDIR /app

# # Install system dependencies for packages like psycopg2
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libpq-dev \
#     gcc \
#  && rm -rf /var/lib/apt/lists/*

# # Copy requirements first
# COPY requirements.txt .

# # Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy all app code
# COPY . .

# EXPOSE 8000

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# # ===== Stage 1: Build stage =====
# FROM python:3.11 as builder

# # Set working directory
# WORKDIR /app

# # Install build dependencies
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     gfortran \
#     libgomp1 \
#     python3-dev \
#     libffi-dev \
#     libssl-dev \
#     && rm -rf /var/lib/apt/lists/*

# # Upgrade pip, setuptools, wheel
# RUN pip install --upgrade pip setuptools wheel

# # Copy requirements to leverage Docker cache
# COPY requirements.txt .

# # Install Python dependencies into /install
# RUN pip install --prefix=/install --no-cache-dir --prefer-binary -r requirements.txt

# # Copy the application code
# COPY . .

# # ===== Stage 2: Final minimal image =====
# FROM python:3.11-slim

# # Set working directory
# WORKDIR /app

# # Copy installed packages from builder stage
# COPY --from=builder /install /usr/local

# # Copy application code
# COPY --from=builder /app /app

# # Expose FastAPI port
# EXPOSE 8000

# # Run the FastAPI app
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]




# Use official micromamba image
FROM mambaorg/micromamba:1.4.3

# Set working directory
WORKDIR /app

# Copy only environment file first to leverage caching
COPY environment.yml /tmp/environment.yml

# Create environment (without prophet) and pack it to speed up future builds
RUN micromamba create -y -f /tmp/environment.yml -n optilogic \
    --no-default-packages \
    --strict-channel-priority \
    && micromamba clean --all --yes \
    && micromamba pack -n optilogic -o /tmp/optilogic.tar.gz

# Unpack the prebuilt environment (fast)
RUN micromamba unpack -n base -f /tmp/optilogic.tar.gz

# Switch to new environment shell
SHELL ["micromamba", "run", "-n", "optilogic", "/bin/bash", "-c"]

# Install prophet separately via pip (fastest way)
RUN pip install --no-cache-dir prophet==1.1.7

# Copy your application code
COPY . /app

# Set default command
CMD ["micromamba", "run", "-n", "optilogic", "python", "main.py"]

