import cv2
import pytesseract
from PIL import Image

class textDetector:
    def __init__(self, video_path, interval_sec=2):
        self.video_path = video_path
        self.interval_sec = interval_sec

    def extract_text_every_n_seconds(self):
        cap = cv2.VideoCapture(self.video_path)

        if not cap.isOpened():
            print("Error: Cannot open video.")
            return

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps * self.interval_sec)
        frame_count = 0
        extracted_texts = []

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % frame_interval == 0:
                # Convert frame to PIL Image
                pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                # OCR
                text = pytesseract.image_to_string(pil_img)
                print(f"Text at {frame_count/fps:.2f}s")
                extracted_texts.append((frame_count/fps, text))

            frame_count += 1

        cap.release()
        return extracted_texts


def execute(video_path):
    detector = textDetector(video_path)
    text_found = detector.extract_text_every_n_seconds()
    return text_found
