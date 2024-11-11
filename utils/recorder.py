import pyaudio

def record_audio(queue, duration=30):
    chunk_size = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 16000

    audio = pyaudio.PyAudio()
    stream = audio.open(format=format, channels=channels,
                        rate=rate, input=True,
                        frames_per_buffer=chunk_size)

    print("Recording...")
    frames = []

    for _ in range(0, int(rate / chunk_size * duration)):
        data = stream.read(chunk_size)
        frames.append(data)
        queue.put(data)  # Send each chunk to the queue for processing

    print("Finished recording.")
    queue.put(None)  # Signal the end of recording

    stream.stop_stream()
    stream.close()
    audio.terminate()
