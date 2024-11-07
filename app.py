from flask import Flask, render_template, request, redirect, url_for, flash
import whisper
import os
import pyaudio
import wave
import re
from collections import defaultdict
from heapq import nlargest

app = Flask(__name__)
app.secret_key = 'ff8c83b221f13086d99650ad3c226c6f'

# Initialize whisper model
whisper_model = whisper.load_model("base")

# Ensure the 'uploads' directory exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Audio settings
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a'}
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 30
WAVE_OUTPUT_FILENAME = "live_output.wav"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def record_audio():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                       rate=RATE, input=True,
                       frames_per_buffer=CHUNK)
    print("Recording...")
    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Finished recording.")
    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

def generate_summary(text, num_sentences=3):
    def clean_text(text):
        # Remove special characters and extra whitespace
        text = re.sub(r'[^\w\s.]', '', text)
        return text.strip()

    def get_sentences(text):
        # Split text into sentences
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        return sentences

    def calculate_word_freq(text):
        # Calculate word frequencies
        words = text.lower().split()
        freq = defaultdict(int)
        for word in words:
            freq[word] += 1
        return freq

    def score_sentences(sentences, word_freq):
        # Score sentences based on word frequency
        scores = defaultdict(int)
        for i, sentence in enumerate(sentences):
            for word in sentence.lower().split():
                scores[i] += word_freq[word]
            scores[i] = scores[i] / max(len(sentence.split()), 1)
        return scores

    # Main summarization process
    if not text or len(text.split()) < 20:
        return "Text too short for summarization"

    # Clean the text
    cleaned_text = clean_text(text)
    
    # Get sentences
    sentences = get_sentences(cleaned_text)
    
    if len(sentences) <= num_sentences:
        return text
    
    # Calculate word frequency
    word_freq = calculate_word_freq(cleaned_text)
    
    # Score sentences
    sentence_scores = score_sentences(sentences, word_freq)
    
    # Select top sentences
    summary_indexes = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    summary_indexes.sort()  # Keep original order
    
    # Construct summary
    summary = '. '.join(sentences[i] for i in summary_indexes) + '.'
    
    return summary

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/live_record', methods=['POST'])
def live_record():
    record_audio()
    result = whisper_model.transcribe(WAVE_OUTPUT_FILENAME, language='en')
    transcription = result['text']
    
    # Generate summary if transcription is long enough
    summary = generate_summary(transcription) if len(transcription.split()) > 50 else "Text too short for summarization"
    
    return render_template('index.html', 
                         transcription=transcription,
                         summary=summary)

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
            result = whisper_model.transcribe(file_path, language='en')
            transcription = result['text']
            summary = generate_summary(transcription) if len(transcription.split()) > 50 else "Text too short for summarization"
            
            return render_template('index.html', 
                                 transcription=transcription,
                                 summary=summary)
        except RuntimeError as e:
            flash(f"Error processing file: {str(e)}")
            return redirect(request.url)
    else:
        flash('File type not supported. Please upload a valid audio file (.wav, .mp3, .m4a)')
        return redirect(request.url)

if __name__ == "__main__":
    app.run(debug=True)
