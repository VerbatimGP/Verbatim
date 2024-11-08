from flask import Flask, render_template, request, redirect, flash
import os
from processing.transcriber import transcribe_audio
from processing.summarizer import generate_summary
from utils.recorder import record_audio

app = Flask(__name__)
app.secret_key = 'ff8c83b221f13086d99650ad3c226c6f'
UPLOAD_FOLDER = 'assets/uploads/'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/live_record', methods=['POST'])
def live_record():
    record_audio()
    result = transcribe_audio("assets/temp/live_output.wav")
    transcription = ' '.join([segment['text'] for segment in result["segments"]])
    summary = generate_summary(transcription) if len(transcription.split()) > 50 else "Text too short for summarization"
    
    return render_template('index.html', transcription=transcription, summary=summary)

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
        try:
            result = transcribe_audio(file_path)
            transcription = ' '.join([segment['text'] for segment in result["segments"]])
            summary = generate_summary(transcription) if len(transcription.split()) > 50 else "Text too short for summarization"
            
            return render_template('index.html', transcription=transcription, summary=summary)
        except RuntimeError as e:
            flash(f"Error processing file: {str(e)}")
            return redirect(request.url)
    else:
        flash('File type not supported. Please upload a valid audio file (.wav, .mp3, .m4a)')
        return redirect(request.url)

if __name__ == "__main__":
    app.run(debug=True)
