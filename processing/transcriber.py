import whisperx
import torch
import gc
from multiprocessing import Process
from time import sleep
import tempfile
import os

def clear_gpu_memory():
    gc.collect()
    torch.cuda.empty_cache()
    torch.cuda.ipc_collect()

def transcribe_audio(audio_queue, transcription_queue):
    device = "cpu"
    model_name = "large-v2"
    compute_type = "int8"
    language = "en"
    batch_size = 2
    model_dir = "../assets/model/"
    token = "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"

    with torch.no_grad():
        # Load the transcription and diarization models
        try:
            print("Loading transcription model...")
            model = whisperx.load_model(model_name, device, compute_type=compute_type, download_root=model_dir)
            diarize_model = whisperx.DiarizationPipeline(use_auth_token=token, device=device)
            print("Models loaded successfully.")
        except Exception as e:
            print(f"Error loading models: {str(e)}")
            return

    while True:
        if audio_queue.empty():
            sleep(0.1)
            continue

        audio_chunk = audio_queue.get()
        if audio_chunk is None:  # End signal
            break

        try:
            # Create a temporary file and write the audio chunk to it
            with tempfile.NamedTemporaryFile(delete=False) as temp_audio_file:
                temp_audio_file.write(audio_chunk)
                temp_audio_file.close()  # Ensure the file is written to disk

                # Now load the audio from the temporary file
                print("Loading audio chunk from temporary file...")
                audio = whisperx.load_audio(temp_audio_file.name)
                print("Audio loaded successfully.")

            # Remove the temporary file after loading
            os.remove(temp_audio_file.name)

        except Exception as e:
            print(f"Error loading audio: {str(e)}")
            continue  # Skip this iteration if audio can't be loaded

        try:
            print("Transcribing audio...")
            result = model.transcribe(audio, batch_size)
            language = result.get("language", "en")
            print(f"Detected language: {language}")
        except Exception as e:
            print(f"Error during transcription: {str(e)}")
            continue  # Skip this iteration if transcription fails

        try:
            print("Aligning transcription results...")
            align_model, metadata = whisperx.load_align_model(language_code=language, device=device)
            aligned_result = whisperx.align(result["segments"], align_model, metadata, audio, device)
            print("Alignment completed.")
        except Exception as e:
            print(f"Error during alignment: {str(e)}")
            continue  # Skip if alignment fails

        try:
            print("Diarizing audio...")
            diarize_segments = diarize_model(audio, min_speakers=1, max_speakers=16)
            print("Diarization completed.")
        except Exception as e:
            print(f"Error during diarization: {str(e)}")
            continue  # Skip if diarization fails

        try:
            print("Assigning speakers to words...")
            final_result = whisperx.assign_word_speakers(diarize_segments, aligned_result)
            print("Speaker assignment completed.")
        except Exception as e:
            print(f"Error during speaker assignment: {str(e)}")
            continue  # Skip if speaker assignment fails

        for segment in final_result["segments"]:
            transcription_queue.put({
                "speaker": segment.get("speaker", "Unknown"),
                "text": segment["text"]
            })
        
        del align_model
        clear_gpu_memory()

    # Cleanup
    del model, diarize_model
    clear_gpu_memory()

def run_transcription_process(audio_queue, transcription_queue):
    p = Process(target=transcribe_audio, args=(audio_queue, transcription_queue))
    p.start()
    p.join()
