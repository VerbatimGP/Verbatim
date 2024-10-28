# Base image for Python
FROM python:3.9-slim

# Install any necessary libraries for audio capture and WebRTC
RUN apt-get update && apt-get install -y <necessary-libraries>

# Set the working directory and copy code
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Run the audio streaming script
CMD ["python", "edge_streamer.py"]
