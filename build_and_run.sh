# Example build and run commands

# Build the Docker image for AMD64 platform
docker build --platform linux/amd64 -t outline-extractor:latest .

# Run the container with volume mounts
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  outline-extractor:latest

# For local development (without Docker)
pip install -r requirements.txt
python extract_outline.py
