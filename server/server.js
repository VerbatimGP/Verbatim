const WebSocket = require('ws');
const wrtc = require('wrtc');
const { spawn } = require('child_process');

const PORT = process.env.PORT || 3010; // Using environment variable for flexibility
const wss = new WebSocket.Server({ port: PORT });
console.log(`WebSocket signaling server started on ws://multi-asr-server:${PORT}`);

// Handle each WebSocket signaling connection
wss.on('connection', (ws) => {
    console.log("New signaling connection established");

    ws.on('message', async (message) => {
        console.log("Received message from client:", message);
        const { type, sdp } = JSON.parse(message);

        if (type === 'offer') {
            const peerConnection = await handleWebRTCConnection(ws, sdp);
            setupTranscription(peerConnection);
        } else if (type === 'candidate') {
            await addIceCandidate(ws, JSON.parse(message));
        }
    });
});

// Function to handle WebRTC connection setup
async function handleWebRTCConnection(ws, sdpOffer) {
    const peerConnection = new wrtc.RTCPeerConnection();

    // Handle ICE candidates
    peerConnection.onicecandidate = (event) => {
        if (event.candidate) {
            ws.send(JSON.stringify({ type: 'candidate', candidate: event.candidate }));
            console.log("Sent ICE candidate to client:", event.candidate);
        }
    };

    // Logging connection state changes
    peerConnection.onconnectionstatechange = () => {
        console.log(`Connection state: ${peerConnection.connectionState}`);
    };
    peerConnection.onsignalingstatechange = () => {
        console.log(`Signaling state: ${peerConnection.signalingState}`);
    };

    // Set the remote SDP offer
    await peerConnection.setRemoteDescription(new wrtc.RTCSessionDescription({ type: 'offer', sdp: sdpOffer }));

    // Create and send SDP answer
    const sdpAnswer = await peerConnection.createAnswer();
    await peerConnection.setLocalDescription(sdpAnswer);
    ws.send(JSON.stringify({ type: 'answer', sdp: sdpAnswer.sdp }));
    console.log("Sent SDP answer to client");

    return peerConnection;
}

// Function to handle incoming ICE candidate
async function addIceCandidate(ws, candidate) {
    try {
        await peerConnection.addIceCandidate(new wrtc.RTCIceCandidate(candidate));
        console.log("Added ICE candidate from client");
    } catch (error) {
        console.error("Error adding ICE candidate:", error);
    }
}

// Function to handle transcription
function setupTranscription(peerConnection) {
    peerConnection.ontrack = (event) => {
        console.log("New audio track received for transcription");

        const audioTrack = event.track;
        if (audioTrack.kind === 'audio') {
            const pythonProcess = spawn('python3', ['asr/asr_engine.py']);

            audioTrack.ondata = (data) => {
                pythonProcess.stdin.write(data);
            };

            pythonProcess.stdout.on('data', (transcription) => {
                console.log(`Transcription: ${transcription.toString()}`);
            });

            pythonProcess.stderr.on('data', (error) => {
                console.error(`Error: ${error.toString()}`);
            });

            pythonProcess.on('exit', (code) => {
                console.log(`Python process exited with code ${code}`);
            });
        }
    };
}
