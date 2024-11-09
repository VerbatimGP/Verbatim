import whisperx
import torch
import gc
import sys
from multiprocessing import Process

def clear_gpu_memory():
    gc.collect()
    torch.cuda.empty_cache()
    torch.cuda.ipc_collect()

def transcribe_audio(audio_file):
    device = "cuda"
    model_name = "large-v2"
    batch_size = 16
    compute_type = "int8"
    model_dir = "../assets/model/"

    with torch.no_grad():
        model = whisperx.load_model(model_name, device, compute_type=compute_type, download_root=model_dir)
        audio = whisperx.load_audio(audio_file)
        result = model.transcribe(audio, batch_size=batch_size)
    print("Transcription:", result["segments"])

    del model
    clear_gpu_memory()

    with torch.no_grad():
        model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
        result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
    print("Alignment:", result["segments"])

    del model_a
    clear_gpu_memory()

    token = "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"
    with torch.no_grad():
        diarize_model = whisperx.DiarizationPipeline(use_auth_token=token, device=device)
        diarize_segments = diarize_model(audio, min_speakers=1, max_speakers=16)
    
    result = whisperx.assign_word_speakers(diarize_segments, result)
    print("Diarization:", diarize_segments)
    print("Final Segments:", result["segments"])

    del diarize_model
    clear_gpu_memory()

    return result

def run_transcription_process(audio_file):
    p = Process(target=transcribe_audio, args=(audio_file,))
    p.start()
    p.join()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        audio_path = sys.argv[1]
        run_transcription_process(audio_path)
    else:
        print("Please provide an audio file path as an argument.")
