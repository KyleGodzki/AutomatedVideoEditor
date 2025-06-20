import audioDetector
import colorDetector
import imageDetector
import textDetector
import OBSInteractor
import ffmpegInitializer
import os
import sys

restarting = True
running = False

audio_analyzed = 0
colors_analyzed = 0
images_analyzed = 0
text_analyzed = 0

queued_actions = {}

final_video_timestamps = []

def main():
    global restarting
    global running
    global audio_analyzed
    global colors_analyzed
    global images_analyzed
    global text_analyzed
    
    while restarting:
        program_setup = input("Type 1 to start OBS recording of your screen or type 2 to link an already existing video on your computer: ")
        if program_setup == "1":
            path = OBS()
        elif program_setup == "2":
            video_path = input("Please give the link to the video to edit in any valid video format (.mp4, .mkv, etc): ")
            if not os.path.isfile(video_path):
                print("Video not found on computer... Exiting program")
                exit()
            path = video_path
        else:
            print("Invalid option")
        if program_setup == "1" or program_setup == "2":
            print("This video will now be accessed: " + path) 
            running = True
            restarting = False

    while running:
        editing_mode = input("Choose what you want to edit and/or detect: \n" \
        "1 - Audio \n" \
        "2 - Color \n" \
        "3 - Images \n" \
        "4 - Text \n" \
        "5 - Exit and export video \n")
        switch_modes(editing_mode)

    if "Audio" in queued_actions:
        video_text = audioDetector.execute(path)
        for audio_key, audio_to_find in queued_actions["Audio"].items():
            for segment in video_text:
                if audio_to_find in segment["text"].lower():
                    start = segment["start"]
                    end = segment["end"]
                    final_video_timestamps.append((start, end))
        final_video_timestamps.sort()
        print(final_video_timestamps)

    if "Color" in queued_actions:
        pass

    if "Images" in queued_actions:
        pass

    if "Text" in queued_actions:
        pass


def switch_modes(option):
    global running
    global audio_analyzed
    global colors_analyzed
    global images_analyzed
    global text_analyzed
    
    match option:
        case "1":
            if not "Audio" in queued_actions:
                queued_actions.update({"Audio": {}})
            audio_analyzed += 1
            audio_script = input("Input the audio you want to find in this video as text: ").lower()
            queued_actions["Audio"][audio_analyzed] = audio_script
        case "2":
            if not "Color" in queued_actions:
                queued_actions.update({"Color": {}})
            color_analyzed += 1
            color = input("Input the color you want to find in this video as a hex value: ").lower()
            queued_actions["Color"][color_analyzed] = color
        case "3":
            if not "Images" in queued_actions:
                queued_actions.update({"Images": {}})
            images_analyzed += 1
            image = input("Input the image you want to find in this video as a valid image format: ").lower()
            queued_actions["Images"][images_analyzed] = image
        case "4":
            if not "Text" in queued_actions:
                queued_actions.update({"Text": {}})
            text_analyzed += 1
            text = input("Input the text you want to find in this video as text: ").lower()
            queued_actions["Text"][text] = text
        case "5":
            print("Editing...")
            running = False
        case _:
            print("Invalid option")

def exit():
    sys.exit()

def OBS():
    password = input("Please enter your OBS password: ")
    OBSInteractor.OBS_PASSWORD = password
    file_name = input("Please enter what you want to name this video (don't include any file extensions): ")
    OBSInteractor.video_name = file_name
    final_path = OBSInteractor.execute()
    return final_path
    

main()
