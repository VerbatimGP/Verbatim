import asyncio
import sounddevice as sd
import numpy as np
import websockets
import json
from aiortc import RTCPeerConnection, RTCSessionDescription, MediaStreamTrack

# Configuration
SIGNALING_SERVER_URI = 'ws://multi-asr-server:3010'  # Replace with actual server address

# Audio configuration
SAMPLE_RATE = 44100
CHANNELS = 1
CHUNK_DURATION = 0.1  # seconds

class AudioStreamTrack(MediaStreamTrack):
    kind = "audio"

    def __init__(self):
        super().__init__()
        self.sample_rate = SAMPLE_RATE
        self.channels = CHANNELS
        self.audio_chunk = np.zeros((int(SAMPLE_RATE * CHUNK_DURATION), CHANNELS), dtype=np.float32)

    async def recv(self):
        # Record audio
        self.audio_chunk = sd.rec(int(SAMPLE_RATE * CHUNK_DURATION), samplerate=SAMPLE_RATE, channels=CHANNELS, blocking=True)
        audio_data = (self.audio_chunk * 32767).astype(np.int16).tobytes()
        
        # Create a new frame for WebRTC
        return audio_data

async def start_stream():
    # Create a WebRTC peer connection
    pc = RTCPeerConnection()

    # Connect to the WebSocket signaling server
    async with websockets.connect(SIGNALING_SERVER_URI) as websocket:
        print("Connected to signaling server")

        # Set up an audio track and add to peer connection
        audio_track = AudioStreamTrack()
        pc.addTrack(audio_track)

        # Create an SDP offer and send to the signaling server
        offer = await pc.createOffer()
        await pc.setLocalDescription(offer)
        await websocket.send(json.dumps({
            "type": "offer",
            "sdp": pc.localDescription.sdp
        }))

        # Wait for the SDP answer from the server
        async for message in websocket:
            data = json.loads(message)

            if data['type'] == 'answer':
                answer = RTCSessionDescription(sdp=data['sdp'], type=data['type'])
                await pc.setRemoteDescription(answer)
                print("Connection established, streaming audio...")

            elif data['type'] == 'candidate':
                candidate = data['candidate']
                await pc.addIceCandidate(candidate)

async def main():
    await start_stream()

if __name__ == "__main__":
    asyncio.run(main())
