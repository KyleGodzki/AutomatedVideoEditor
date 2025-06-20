import cv2
import numpy as np
import time
from obswebsocket import obsws, requests, exceptions
import pyautogui
import sys
import os

# OBS WebSocket config
OBS_HOST = "localhost"
OBS_PORT = 4455
OBS_PASSWORD = "Kyle01281274$$"

# Detection parameters
STILLNESS_THRESHOLD = 5       # seconds of still screen before stopping
PIXEL_DIFF_THRESHOLD = 30000  # how much change counts as "motion"
FRAME_INTERVAL = 1            # seconds between checks

video_name = "Temp"

def connect_obs():
    try:
        ws = obsws(OBS_HOST, OBS_PORT, OBS_PASSWORD)
        ws.connect()
        print("✅ Connected to OBS WebSocket")
        return ws
    except exceptions.ConnectionFailure as e:
        print(f"❌ Failed to connect to OBS: {e}")
        sys.exit()

def capture_screen_cv2():
    screenshot = pyautogui.screenshot()
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    return frame

def screen_is_still(prev_frame, curr_frame):
    diff = cv2.absdiff(prev_frame, curr_frame)
    non_zero_count = np.count_nonzero(diff)
    return non_zero_count < PIXEL_DIFF_THRESHOLD

def stop_and_get_output(ws):
    stop_response = ws.call(requests.StopRecord())
    output_path = stop_response.getOutputPath()

    print(f"📁 Original output path: {output_path}")
    time.sleep(3)
    if output_path and os.path.exists(output_path):
        directory = os.path.dirname(output_path)
        new_path = os.path.join(directory, video_name + ".mkv")

        try:
            os.rename(output_path, new_path)
            print(f"✅ Renamed to: {new_path}")
        except Exception as e:
            print(f"⚠️ Could not rename file: {e}")
    else:
        print("⚠️ Output path invalid or file not found.")

def execute():
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
                    print("⏹️ Screen still too long. Stopping recording.")
                    stop_and_get_output(ws)
                    break
            else:
                last_change_time = time.time()

            prev_frame = curr_frame

    except KeyboardInterrupt:
        print("❌ Interrupted. Stopping OBS recording.")
        stop_and_get_output(ws)

    ws.disconnect()
    print("✅ OBS WebSocket disconnected. Done.")

