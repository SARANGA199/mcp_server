# ---------------------------------
# Base Image
# ---------------------------------
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Avoid bytecode & buffer issues
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install basic dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy dependency list
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose FastMCP HTTP port
EXPOSE 8000

# ---------------------------------
# Start FastMCP HTTP server
# ---------------------------------
CMD ["fastmcp", "run", "main.py:mcp", "--transport", "http", "--host", "0.0.0.0", "--port", "8000"]