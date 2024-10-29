const WebSocket = require('ws');
const wrtc = require('wrtc');
const { spawn } = require('child_process');

const PORT = 3010;  // WebSocket signaling server port
const wss = new WebSocket.Server({ port: PORT });
console.log(`WebSocket signaling server started on ws://localhost:${PORT}`);

// Handle each WebSocket signaling connection
wss.on('connection', (ws) => {
    console.log("New signaling connection established");

    ws.on('message', async (message) => {
        const { type, sdp } = JSON.parse(message);

        if (type === 'offer') {
            const peerConnection = await handleWebRTCConnection(ws, sdp);
            setupTranscription(peerConnection);
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
        }
    };

    // Set the remote SDP offer
    await peerConnection.setRemoteDescription(new wrtc.RTCSessionDescription({ type: 'offer', sdp: sdpOffer }));

    // Create an SDP answer
    const sdpAnswer = await peerConnection.createAnswer();
    await peerConnection.setLocalDescription(sdpAnswer);
    ws.send(JSON.stringify({ type: 'answer', sdp: sdpAnswer.sdp }));

    return peerConnection;
}

// Function to handle the transcription process
function setupTranscription(peerConnection) {
    peerConnection.ontrack = (event) => {
        console.log("New audio track received for transcription");

        const audioTrack = event.track;
        if (audioTrack.kind === 'audio') {
            // Spawn a new child process to run asr_engine.py
            const pythonProcess = spawn('python3', ['asr/asr_engine.py']);

            // Feed audio stream to the Python transcription process
            audioTrack.ondata = (data) => {
                pythonProcess.stdin.write(data);
            };

            // Handle transcription output from asr_engine.py
            pythonProcess.stdout.on('data', (transcription) => {
                console.log(`Transcription: ${transcription.toString()}`);
            });

            // Error handling
            pythonProcess.stderr.on('data', (error) => {
                console.error(`Error: ${error.toString()}`);
            });

            pythonProcess.on('exit', (code) => {
                console.log(`Python process exited with code ${code}`);
            });
        }
    };
}
