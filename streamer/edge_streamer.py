import asyncio
import sounddevice as sd
import numpy as np
from aiortc import RTCPeerConnection, RTCSessionDescription, MediaStreamTrack
from aiortc.contrib.signaling import TcpSocketSignaling

# WebRTC Configuration
SIGNALING_HOST = 'localhost'    # Replace with the server IP or hostname
SIGNALING_PORT = 3010           # Replace with the signaling server port

# Audio configuration
SAMPLE_RATE = 44100
CHANNELS = 1
DURATION = 10  # seconds

class AudioStreamTrack(MediaStreamTrack):
    kind = "audio"

    def __init__(self):
        super().__init__()
        self.sample_rate = SAMPLE_RATE
        self.channels = CHANNELS

    async def recv(self):
        # Capture audio for a small chunk duration and send as RTP packets
        audio_chunk = sd.rec(int(SAMPLE_RATE * 0.1), samplerate=SAMPLE_RATE, channels=CHANNELS)
        sd.wait()
        audio_data = (audio_chunk * 32767).astype(np.int16).tobytes()
        
        return audio_data


async def run():
    # Initialize WebRTC connection and signaling
    pc = RTCPeerConnection()
    signaling = TcpSocketSignaling(SIGNALING_HOST, SIGNALING_PORT)

    # Create a track for the audio stream
    audio_track = AudioStreamTrack()
    pc.addTrack(audio_track)

    @pc.on("iceconnectionstatechange")
    async def on_ice_connection_state_change():
        print("ICE connection state:", pc.iceConnectionState)
        if pc.iceConnectionState == "failed":
            await pc.close()

    # Connect to the signaling server
    await signaling.connect()

    # Send an offer and set the local description
    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)

    # Exchange the SDP information
    await signaling.send(pc.localDescription)
    answer = await signaling.receive()
    await pc.setRemoteDescription(answer)

    # Keep the connection alive and audio streaming
    try:
        await signaling.close()
    finally:
        await pc.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run())
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
