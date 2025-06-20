import whisper

def execute():
    model = whisper.load_model("base")
    result = model.transcribe(r"C:\ProjectAssets - Python\dearHunterOne.mp3")
    print(result["text"])


