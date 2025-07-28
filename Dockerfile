# Explicit AMD64 base
FROM --platform=linux/amd64 python:3.10-slim

# Install essentials
RUN pip install --no-cache-dir pymupdf

WORKDIR /app
COPY . /app

# Create input and output directories
RUN mkdir -p /app/input /app/output

# Entrypoint will process all PDFs under /app/input
ENTRYPOINT ["python", "extract_outline.py"]
