# Base image for Node.js and Python environment
FROM node:18-bullseye AS node-base

# Install Python 3.9 for WhisperX
RUN apt-get update && apt-get install -y python3 python3-pip

# Copy Node.js dependencies
WORKDIR /app
COPY package*.json ./
RUN npm install

# Copy Python dependencies
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# Copy all source code
COPY . .

# Expose necessary ports (e.g., 3000 for Node server, adjust for WebRTC)
EXPOSE 3000

# Start the Node.js server
CMD ["node", "server.js"]
