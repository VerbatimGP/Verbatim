from flask import Flask, render_template, request, redirect, url_for, flash
import whisper
import os
import pyaudio
import wave

app = Flask(__name__)
app.secret_key = 'ff8c83b221f13086d99650ad3c226c6f'  # To use flash messages

model = whisper.load_model("base")

# Ensure the 'uploads' directory exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Supported audio formats
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a'}

# Audio recording settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "live_output.wav"


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def record_audio():
    audio = pyaudio.PyAudio()

    # Start recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Recording...")

    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio as a .wav file
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/live_record', methods=['POST'])    
def live_record():
    # Record live audio
    record_audio()

    # Transcribe using Whisper (strictly in English)
    result = model.transcribe(WAVE_OUTPUT_FILENAME, language='en')

    return render_template('index.html', transcription=result['text'])


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
            # Transcribe using Whisper (strictly in English)
            result = model.transcribe(file_path, language='en')
            return render_template('index.html', transcription=result['text'])
        except RuntimeError as e:
            flash(f"Error processing file: {str(e)}")
            return redirect(request.url)
    else:
        flash('File type not supported. Please upload a valid audio file (.wav, .mp3, .m4a)')
        return redirect(request.url)


if __name__ == "__main__":
    app.run(debug=True)
