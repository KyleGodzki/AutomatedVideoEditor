import cv2
import numpy as np

def find_template_in_video(video_path, template_path, threshold=0.8):
    # Load and preprocess the template image
    print("Loading template image...")
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        print(f"Error: Cannot load template image from {template_path}")
        return
    w, h = template.shape[::-1]

    # Open the video file
    print("Opening video file...")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Cannot open video file {video_path}")
        return

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Video FPS: {fps}, Total Frames: {frame_count}")

    matches = []
    last_logged_percent = -10  
    last_match_time = -9999   
    frame_idx = 0

    print("Starting frame-by-frame processing...")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Reached end of video.")
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        timestamp = frame_idx / fps
        if max_val >= threshold and (timestamp - last_match_time >= 3):
            matches.append(timestamp)
            last_match_time = timestamp
            print(f"Image found at {timestamp:.2f} seconds (Frame {frame_idx})")

        percent = (frame_idx / frame_count) * 100
        if percent >= last_logged_percent + 10:
            last_logged_percent += 10
            print(f"Processed {last_logged_percent}% of video...")

        frame_idx += 1

    cap.release()

    rounded_matches = [round(num, 2) for num in matches]
    return rounded_matches

def execute(video_file, template_image):
    match_threshold = 0.5  # Adjust this value as needed
    images_found = find_template_in_video(video_file, template_image, threshold=match_threshold)
    return images_found
