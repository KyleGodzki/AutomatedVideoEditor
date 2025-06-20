import whisper

def execute(video):
    model = whisper.load_model("base")
    result = model.transcribe(video)
    segments = result.get("segments", [])
    simple_segments = [
        {
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"]
        }
        for seg in segments
    ]
    return simple_segments


