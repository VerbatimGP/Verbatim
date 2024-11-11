from flask import Flask, render_template, request, Response, redirect, flash
import os
import json
from multiprocessing import Queue, Process
from processing.transcriber import run_transcription_process
from processing.summarizer import generate_summary
from utils.recorder import record_audio
from time import sleep

app = Flask(__name__)
app.secret_key = 'ff8c83b221f13086d99650ad3c226c6f'
UPLOAD_FOLDER = 'assets/uploads/'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a'}

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

audio_queue = Queue()
transcription_queue = Queue()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_live_transcription', methods=['POST'])
def start_live_transcription():
    # Start recording and transcribing as parallel processes
    recorder_process = Process(target=record_audio, args=(audio_queue,))
    transcriber_process = Process(target=run_transcription_process, args=(audio_queue, transcription_queue))
    
    recorder_process.start()
    transcriber_process.start()

    return Response(stream_transcription(transcription_queue), mimetype="text/event-stream")

def stream_transcription(transcription_queue):
    transcription_text = []
    
    while True:
        if not transcription_queue.empty():
            data = transcription_queue.get()
            if data == "END":
                break
            
            speaker, text = data.get("speaker", ""), data.get("text", "")
            if speaker and text:
                transcription_text.append(f"{speaker}: {text}")
                yield f"data: {json.dumps({'speaker': speaker, 'text': text})}\n\n"
        else:
            sleep(0.1)
    
    # Generate summary once live transcription ends
    summary = generate_summary(' '.join(transcription_text))
    yield f"data: {json.dumps({'summary': summary})}\n\n"

@app.route('/stop_transcription', methods=['POST'])
def stop_transcription():
    # Signal to end the recording
    audio_queue.put(None)
    return redirect('/')

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    if 'audio_file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['audio_file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        # Create new queues for this upload request
        upload_audio_queue = Queue()
        upload_transcription_queue = Queue()

        # Start the transcription process as a separate process
        transcriber_process = Process(target=run_transcription_process, args=(upload_audio_queue, upload_transcription_queue))
        transcriber_process.start()

        try:
            # Load the audio into the queue
            with open(file_path, 'rb') as f:
                audio_data = f.read()  # Read the audio data into memory
                upload_audio_queue.put(audio_data)

            # Start streaming the transcription results
            return Response(stream_transcription(upload_transcription_queue), mimetype="text/event-stream")
        except Exception as e:
            flash(f"Error processing file: {str(e)}")
            return redirect(request.url)

    else:
        flash('File type not supported. Please upload a valid audio file (.wav, .mp3, .m4a)')
        return redirect(request.url)

if __name__ == "__main__":
    app.run(debug=True)
