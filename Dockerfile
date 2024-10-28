# Base image for Python
FROM python:3.9-slim

# Install any necessary libraries for audio capture and WebRTC
RUN xargs apt-get update && apt-get install -y < setup/packages.txt

# Set the working directory and copy code
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install -r setup/pip_requirements.txt

# Run the audio streaming script
CMD ["python", "streamer/edge_streamer.py"]
