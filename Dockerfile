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

# ---------- Stage 1: Build stage ----------
FROM python:3.11-slim AS build

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    g++ \
    libgomp1 \
    python3-dev \
    libffi-dev \
    libssl-dev \
    wget \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, wheel
RUN pip install --upgrade pip setuptools wheel

# Copy requirements
COPY requirements.txt .

# Install Python packages to /install
RUN pip install --prefix=/install --upgrade --no-cache-dir --prefer-binary -r requirements.txt

# Copy project files
COPY . .

# ---------- Stage 2: Runtime stage ----------
FROM python:3.11-slim AS runtime

WORKDIR /app

# Copy installed Python packages from build stage
COPY --from=build /install /usr/local

# Copy project files
COPY --from=build /app /app

# Expose port (adjust if needed)
EXPOSE 8000

# Default command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
