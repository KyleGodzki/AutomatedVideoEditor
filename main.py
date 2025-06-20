import audioDetector
import colorDetector
import imageDetector
import textDetector
import OBSInteractor
import ffmpegInitializer
import os
import sys

running = True

def main():
    while running:
        program_setup = input("Type 1 to start OBS recording of your screen or type 2 to link an already existing video on your computer: ")
        if program_setup == "1":
            OBS()
        elif program_setup == "2":
            video_path = input("Please give the link to the video to edit in any valid video format (.mp4, .mkv, etc): ")
            if not os.path.isfile(video_path):
                print("Video not found on computer... Exiting program")
                exit()
        else:
            print("Invalid option")
    

def exit():
    running = False
    sys.exit()

def OBS():
    password = input("Please enter your OBS password: ")
    OBSInteractor.OBS_PASSWORD = password
    file_name = input("Please enter what you want to name this video (don't include any file extensions): ")
    OBSInteractor.video_name = file_name
    OBSInteractor.execute()
main()
