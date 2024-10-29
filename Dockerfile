# Base image for Python
FROM python:3.10-slim

# Install any necessary libraries for audio capture and WebRTC
RUN apt-get update 

# Set the working directory and copy code
WORKDIR /app
COPY . .

# Install Package dependencies
RUN xargs -a setup/packages.txt -r apt-get install -y

# Install Python dependencies
RUN pip install -r setup/pip_requirements.txt

# Run the audio streaming script
CMD ["python", "streamer/edge_streamer.py"]
