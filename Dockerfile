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

# ============================
# Stage 1: Builder (full tools)
# ============================
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VIRTUALENVS_CREATE=false

# Install essential build tools for heavy packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libffi-dev \
    libssl-dev \
    libgomp1 \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and wheel to ensure wheel installation
RUN python -m pip install --upgrade pip setuptools wheel

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies using wheels wherever possible
RUN pip install --upgrade --no-cache-dir --prefer-binary -r requirements.txt

# ============================
# Stage 2: Final lightweight image
# ============================
FROM python:3.11-slim

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Set working directory
WORKDIR /app

# Copy your application code
COPY . .

# Expose port if needed (for web apps)
# EXPOSE 8000

# Default command
CMD ["python", "main.py"]

