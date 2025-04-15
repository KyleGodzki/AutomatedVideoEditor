import ffmpeg
import os

# Get path to Desktop
desktop_path = r'C:\Users\kyleg\OneDrive\Desktop'
output_file = os.path.join(desktop_path, "output.mp4")


# Input file (make sure the path and name are correct)
input_file = r'C:\Users\kyleg\OneDrive\Desktop\XXXXXX.mkv' 

# Trim and export
stream = (
    ffmpeg
    .input(input_file, ss=10, t=15)  # Start at 10s, last for 15s
    .output(output_file)
)

ffmpeg.run(stream)

print(f"Saved trimmed video to: {output_file}")

class ffmpegInitializer:
    def __init__(self):
        pass
