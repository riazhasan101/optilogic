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

# Use official Python image with Debian base
FROM python:3.11

# Set working directory
WORKDIR /app

# Install system dependencies needed for prophet and other packages
RUN apt-get update && apt-get install -y \
    build-essential \
    gfortran \
    libgomp1 \
    python3-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, wheel
RUN pip install --upgrade pip setuptools wheel

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

# Copy project files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Command to run your FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
