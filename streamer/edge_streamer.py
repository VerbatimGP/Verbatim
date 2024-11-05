import asyncio
import sounddevice as sd
import numpy as np
import websockets
import json
import av  # PyAV for managing audio streams
from aiortc import RTCPeerConnection, MediaStreamTrack, RTCSessionDescription, RTCIceCandidate
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("edge_streamer")

SIGNALING_SERVER_URI = "ws://multi-asr-server:3010"  # Docker Compose service name
SAMPLE_RATE = 44100
CHANNELS = 1
CHUNK_DURATION = 0.1  # seconds

# Define audio track class
class AudioStreamTrack(MediaStreamTrack):
    kind = "audio"

    def __init__(self):
        super().__init__()
        self.sample_rate = SAMPLE_RATE
        self.channels = CHANNELS
        self.timestamp = 0  # Initialize the timestamp
        self.audio_lock = asyncio.Lock()  # Lock for synchronizing audio access

    async def recv(self):
        async with self.audio_lock:  # Ensure exclusive access to audio recording
            # Record audio chunk from the microphone
            audio_chunk = sd.rec(int(SAMPLE_RATE * CHUNK_DURATION), samplerate=SAMPLE_RATE, channels=CHANNELS)
            sd.wait()
            
            # Log audio recording
            logger.info("Audio recorded from microphone")
            
            # Convert from float32 to int16
            audio_data = (audio_chunk * 32767).astype(np.int16).reshape(1, -1)
            
            # Create a new PyAV audio frame
            audio_frame = av.AudioFrame.from_ndarray(audio_data, format="s16", layout="mono")
            audio_frame.sample_rate = self.sample_rate
            
            # Set the timestamp for the audio frame
            audio_frame.pts = self.timestamp  # Set presentation timestamp
            self.timestamp += audio_frame.samples  # Increment timestamp by the number of samples in this frame
            
            # Log audio frame creation
            logger.info("Audio frame created with pts=%d", audio_frame.pts)

            await asyncio.sleep(CHUNK_DURATION)  # Match the duration of the chunk
            return audio_frame

async def connect_to_signaling_server():
    async with websockets.connect(SIGNALING_SERVER_URI) as ws:
        logger.info("Connected to signaling server")
        await initiate_webrtc_connection(ws)

        # Start a heartbeat to keep the WebSocket alive
        asyncio.create_task(send_heartbeat(ws))

        # Listen for messages from the server
        async for message in ws:
            logger.info("Listening for messages from server...")
            try:
                data = json.loads(message)
                logger.info("Received message from server: %s", data)  # Log received message

                if data["type"] == "answer":
                    await handle_sdp_answer(data)
                elif data["type"] == "candidate":
                    await handle_ice_candidate(data)
            except json.JSONDecodeError:
                logger.error("Error decoding message from server: %s", message)
            except Exception as e:
                logger.error("Error handling message: %s", e)

async def initiate_webrtc_connection(ws):
    global pc
    pc = RTCPeerConnection()

    # Logging state changes
    pc.on_connectionstatechange = lambda: logger.info("Connection state: %s", pc.connectionState)
    pc.on_signalingstatechange = lambda: logger.info("Signaling state: %s", pc.signalingState)

    # Add audio track
    audio_track = AudioStreamTrack()
    logger.info("Audio track initialized")
    pc.addTrack(audio_track)
    logger.info("Audio track added to peer connection")

    # Create SDP offer and send to signaling server
    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)
    await ws.send(json.dumps({"type": "offer", "sdp": pc.localDescription.sdp}))
    logger.info("Sent SDP offer to signaling server")

async def handle_sdp_answer(data):
    sdp = data["sdp"]
    await pc.setRemoteDescription(RTCSessionDescription(sdp, "answer"))
    logger.info("Received SDP answer from server")

async def handle_ice_candidate(data):
    candidate = data.get("candidate")
    if candidate:
        try:
            # Verify that all required fields are present
            required_fields = ["foundation", "address", "port", "priority", "protocol", "type", "sdpMid", "sdpMLineIndex"]
            if all(field in candidate for field in required_fields):
                ice_candidate = RTCIceCandidate(
                    component="rtp",
                    foundation=candidate["foundation"],
                    ip=candidate["address"],
                    port=candidate["port"],
                    priority=candidate["priority"],
                    protocol=candidate["protocol"],
                    type=candidate["type"],
                    sdpMid=candidate["sdpMid"],
                    sdpMLineIndex=candidate["sdpMLineIndex"]
                )
                await pc.addIceCandidate(ice_candidate)
                logger.info("Added ICE candidate from server")
            else:
                logger.warning("Incomplete ICE candidate received: %s", candidate)
        except Exception as e:
            logger.error("Error adding ICE candidate: %s", e)

async def send_heartbeat(ws):
    while True:
        try:
            await ws.send(json.dumps({"type": "ping"}))
            logger.info("Sent heartbeat to keep WebSocket alive")
        except Exception as e:
            logger.error("Error in sending heartbeat: %s", e)
            break
        await asyncio.sleep(10)  # Send heartbeat every 10 seconds

async def main():
    await connect_to_signaling_server()

asyncio.run(main())
