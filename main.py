import audioDetector
import colorDetector
import imageDetector
import textDetector
import OBSInteractor
import ffmpegInitializer
import os
import sys
import re

restarting = True
running = False

audio_analyzed = 0
colors_analyzed = 0
images_analyzed = 0
text_analyzed = 0

queued_actions = {}

edit_buffers = 3

start = 1
end = 0
final_video_timestamps = [[], []]

def main():
    global restarting
    global running
    global audio_analyzed
    global colors_analyzed
    global images_analyzed
    global text_analyzed
    global edit_buffers
    
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
        "5 - Exit and export video \n"
        f"6 - Edit amount of time before/after edits (Currently {edit_buffers} seconds\n")
        switch_modes(editing_mode)

    if "Audio" in queued_actions:
        video_audio = audioDetector.execute(path)
        for audio_key, audio_to_find in queued_actions["Audio"].items():
            for segment in video_audio:
                if audio_to_find in segment["text"].lower():
                    start = segment["start"]
                    end = segment["end"]
                    print(f"Audio found from {start} to {end} second segments")
                    final_video_timestamps[0].append(start)
                    final_video_timestamps[1].append(end)

    if "Color" in queued_actions:
        for color_key, color_to_find in queued_actions["Color"].items():
            video_color = colorDetector.execute(path, color_to_find)
            for color in video_color:
                start = color - edit_buffers
                end = color + edit_buffers
                if start < 0:
                    start = 0
                final_video_timestamps[0].append(start)
                final_video_timestamps[1].append(end)

    if "Images" in queued_actions:
        for image_key, image_to_find in queued_actions["Images"].items():
            video_image = imageDetector.execute(path, image_to_find)
            for image in video_image:
                start = image - edit_buffers
                end = image + edit_buffers
                if start < 0:
                    start = 0
                final_video_timestamps[0].append(start)
                final_video_timestamps[1].append(end)

    if "Text" in queued_actions:
        video_text = textDetector.execute(path)
        for text_key, text_to_find in queued_actions["Text"].items():
            for timestamp, text in video_text:
                if text_to_find in text:
                    start = timestamp - edit_buffers
                    end = timestamp + edit_buffers
                    if start < 0:
                        start = 0
                    final_video_timestamps[0].append(start)
                    final_video_timestamps[1].append(end)

    # final_video_timestamps.sort()
    print(final_video_timestamps)


def switch_modes(option):
    global running
    global audio_analyzed
    global colors_analyzed
    global images_analyzed
    global text_analyzed
    global edit_buffers

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
            colors_analyzed += 1
            finished_analysis = False
            while not finished_analysis:
                color = input("Input the color you want to find in this video as a hex value (Ex: #FF00CC): ")
                if re.fullmatch(r"#[0-9A-Fa-f]{6}", color):
                    queued_actions["Color"][colors_analyzed] = color
                    finished_analysis = True
                else:
                    print("Invalid hex color")
        case "3":
            if not "Images" in queued_actions:
                queued_actions.update({"Images": {}})
            images_analyzed += 1
            finished_analysis = False
            while not finished_analysis:
                image_path = input("Input a image from your computer that you want to find in this video as a valid image format: ")
                if os.path.isfile(image_path):
                    queued_actions["Images"][images_analyzed] = image_path
                    finished_analysis = True
                else:
                    print("Image not found on computer")
        case "4":
            if not "Text" in queued_actions:
                queued_actions.update({"Text": {}})
            text_analyzed += 1
            text = input("Input the text you want to find in this video: ").lower()
            queued_actions["Text"][text] = text
        case "5":
            print("Editing...")
            running = False
        case "6":
            new_buffers = input("Input the amount of time (as an integer) before and after the located clip that is shown and not deleted. \n" \
            "By default, 3 seconds before and after any given clip are saved. Max is 30 seconds. Set this to 0 to only have detected content in the final video: ")
            try:
                new_buffers = int(new_buffers)
                if new_buffers > 30:
                    print("Buffers can't be greater than 30 seconds")
                else:
                    edit_buffers = new_buffers
            except ValueError:
                print("Error: Input is not a valid integer")
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
