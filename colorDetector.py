import cv2
import numpy as np

# Function to convert Hex to RGB
def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    
    # Convert hex to RGB tuple
    rgb = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
    
    return rgb

# Function to convert RGB to HSV
def rgb_to_hsv(rgb):
    # Convert the RGB values to HSV
    bgr = np.uint8([[list(rgb)]])
    hsv = cv2.cvtColor(bgr, cv2.COLOR_RGB2HSV)
    return hsv[0][0]

def detect_color_in_video(video_path, hex_color, min_time_gap=5):
    rgb_color = hex_to_rgb(hex_color)
    hsv_color = rgb_to_hsv(rgb_color)

    lower_bound = np.array([hsv_color[0] - 1, 90, 90]) 
    upper_bound = np.array([hsv_color[0] + 1, 110, 110])  

    cap = cv2.VideoCapture(video_path)
    

    last_detection_time = -min_time_gap  
    matches = []  

    frame_idx = 0
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)
        
        if np.count_nonzero(mask) > 0:
            timestamp = frame_idx / fps  

            if timestamp - last_detection_time >= min_time_gap:
                matches.append(timestamp)
                last_detection_time = timestamp 
                print(f"Color detected at {timestamp:.2f} seconds (Frame {frame_idx})")

        frame_idx += 1

    cap.release()

    rounded_matches = [round(num, 2) for num in matches]
    return rounded_matches

def execute(video_path, hex_color):
    colors_found = detect_color_in_video(video_path, hex_color)
    return colors_found