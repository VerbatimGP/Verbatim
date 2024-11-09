import whisperx
import torch
import gc

def transcribe_audio(audio_file):
    # Configure model settings
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = "large-v2"
    batch_size = 16
    compute_type = "int8"
    
    # Model directory
    model_dir = "../assets/model/"

    # Load and transcribe audio
    model_t = whisperx.load_model(model, device, compute_type=compute_type, download_root=model_dir)
    audio = whisperx.load_audio(audio_file)
    result = model_t.transcribe(audio, batch_size=batch_size)
    
    # Free resources
    gc.collect()
    torch.cuda.empty_cache()
    del model_t

    # Perform alignment
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
    
    # Free resources
    gc.collect()
    torch.cuda.empty_cache()
    del model_a

    # Speaker diarization
    token = "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"
    diarize_model = whisperx.DiarizationPipeline(use_auth_token=token, device=device)
    diarize_segments = diarize_model(audio, min_speakers=1, max_speakers=16)
    
    # Assign speakers to segments
    result = whisperx.assign_word_speakers(diarize_segments, result)
    
    return result
