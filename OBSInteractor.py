import cv2
import numpy as np
import time
from obswebsocket import obsws, requests
import pyautogui

# OBS WebSocket config
OBS_HOST = "localhost"
OBS_PORT = 4455  # Use 4444 for OBS WebSocket v4, 4455 for v5
OBS_PASSWORD = "Kyle01281274$$"  # Change this to your OBS WebSocket password

# Detection parameters
STILLNESS_THRESHOLD = 10       # seconds of still screen before stopping
PIXEL_DIFF_THRESHOLD = 30000   # how much change counts as "motion"
FRAME_INTERVAL = 1             # seconds between checks

def connect_obs():
    ws = obsws(OBS_HOST, OBS_PORT, OBS_PASSWORD)
    ws.connect()
    return ws

def capture_screen_cv2():
    # Capture screen using pyautogui and convert for OpenCV
    screenshot = pyautogui.screenshot()
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    return frame

def screen_is_still(prev_frame, curr_frame):
    diff = cv2.absdiff(prev_frame, curr_frame)
    non_zero_count = np.count_nonzero(diff)
    return non_zero_count < PIXEL_DIFF_THRESHOLD

def main():
    input("📹 Press Enter to start screen recording...")

    print("🔌 Connecting to OBS...")
    ws = connect_obs()

    print("▶️ Starting OBS recording...")
    ws.call(requests.StartRecord())

    last_change_time = time.time()
    prev_frame = capture_screen_cv2()

    try:
        while True:
            time.sleep(FRAME_INTERVAL)
            curr_frame = capture_screen_cv2()

            if screen_is_still(prev_frame, curr_frame):
                if time.time() - last_change_time > STILLNESS_THRESHOLD:
                    print("⏹️ Screen has been still for too long. Stopping recording.")
                    ws.call(requests.StopRecord())
                    break
            else:
                last_change_time = time.time()

            prev_frame = curr_frame

    except KeyboardInterrupt:
        print("❌ Interrupted. Stopping OBS recording.")
        ws.call(requests.StopRecord())

    ws.disconnect()
    print("✅ Done. OBS recording stopped.")

if __name__ == "__main__":
    main()

class OBSInteractor:
    def __init__(self):
        pass

