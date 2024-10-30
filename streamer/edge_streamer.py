import asyncio
import websockets
import json
import av  # PyAV for managing audio streams
from aiortc import RTCPeerConnection, MediaStreamTrack, RTCSessionDescription, RTCIceCandidate

SIGNALING_SERVER_URI = "ws://multi-asr-server:3010"  # Docker Compose service name

async def connect_to_signaling_server():
    async with websockets.connect(SIGNALING_SERVER_URI) as ws:
        print("Connected to signaling server")
        await initiate_webrtc_connection(ws)

        # Start a heartbeat to keep the WebSocket alive
        asyncio.create_task(send_heartbeat(ws))

        # Listen for messages from the server
        async for message in ws:
            print("Listening for messages from server...")
            try:
                data = json.loads(message)
                print("Received message from server:", data)  # Log received message

                if data["type"] == "answer":
                    await handle_sdp_answer(data, pc)
                elif data["type"] == "candidate":
                    await handle_ice_candidate(data, pc)
            except json.JSONDecodeError:
                print("Error decoding message from server:", message)
            except Exception as e:
                print("Error handling message:", e)

async def initiate_webrtc_connection(ws):
    global pc
    pc = RTCPeerConnection()

    # Logging state changes
    pc.on_connectionstatechange = lambda: print("Connection state:", pc.connectionState)
    pc.on_signalingstatechange = lambda: print("Signaling state:", pc.signalingState)

    # Add audio track
    pc.addTrack(GenerateAudioStreamTrack())

    # Create SDP offer and send to signaling server
    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)
    await ws.send(json.dumps({"type": "offer", "sdp": pc.localDescription.sdp}))
    print("Sent SDP offer to signaling server")

async def handle_sdp_answer(data, pc):
    sdp = data["sdp"]
    await pc.setRemoteDescription(RTCSessionDescription(sdp, "answer"))
    print("Received SDP answer from server")

async def handle_ice_candidate(data, pc):
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
                print("Added ICE candidate from server")
            else:
                print("Incomplete ICE candidate received:", candidate)
        except Exception as e:
            # Log the error but do not stop the message processing loop
            print("Error adding ICE candidate:", e)

class GenerateAudioStreamTrack(MediaStreamTrack):
    kind = "audio"

    async def recv(self):
        # Dummy audio frame for testing purposes
        frame = av.AudioFrame(format="s16", layout="mono", samples=480)
        for plane in frame.planes:
            plane.update(bytes([0] * len(plane)))

        await asyncio.sleep(0.02)  # Approximate 50 fps for audio frames
        return frame

async def send_heartbeat(ws):
    while True:
        try:
            await ws.send(json.dumps({"type": "ping"}))
            print("Sent heartbeat to keep WebSocket alive")
        except Exception as e:
            print("Error in sending heartbeat:", e)
            break
        await asyncio.sleep(10)  # Send heartbeat every 10 seconds

async def main():
    await connect_to_signaling_server()

asyncio.run(main())
