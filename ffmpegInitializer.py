import ffmpeg
import os
import shutil
from moviepy import *

def execute(file_name, file_location, input_file, video_timestamps, edit_mode):
    total_clips = 0

    probe = ffmpeg.probe(input_file)
    original_video_length = float(probe['format']['duration'])

    start_times = video_timestamps[0]
    end_times = video_timestamps[1]

    keep_intervals = merge_overlapping_ranges(start_times, end_times)
    if edit_mode == 2: # 1 means delete not detected content. 2 means delete detected content, thus invert what we want to keep in the video.
        keep_intervals = invert_intervals(keep_intervals, original_video_length)

    for start, end in keep_intervals:
        duration = end - start
        output_file = os.path.join(file_location, file_name + f"{total_clips}.mp4")
        stream = (
            ffmpeg
            .input(input_file, ss = start, t = duration)  # Start at ss, last for t seconds
            .output(output_file)
        )
        ffmpeg.run(stream)

        total_clips += 1

    
    clips = []
    for i in range(total_clips):
        clip_path = os.path.join(file_location, f"{file_name}{i}.mp4")
        clips.append(VideoFileClip(clip_path))

    final_clip = concatenate_videoclips(clips)
    final_output_path = os.path.join(file_location, f"{file_name}_final.mp4") # Final video
    final_clip.write_videofile(final_output_path, codec="libx264")

    final_clip.close()  # Close each clip to avoid permission error
    for clip in clips:
        clip.close()
    
    
    archive_folder = os.path.join(file_location, "archived_clips")
    os.makedirs(archive_folder, exist_ok=True)

    try:
        for i in range(total_clips):
            clip_path = os.path.join(file_location, f"{file_name}{i}.mp4")
            if os.path.exists(clip_path):
                shutil.move(clip_path, archive_folder) # Concatenated clips to reference
    except PermissionError as e:
        print(f"Warning: Could not move file {clip_path} — it's still in use. Error: {e}")


    final_input = input(f"Saved trimmed video to: {final_output_path}. Press 1 to show all the timestamps that were deleted from your original video: ")
    if final_input == "1":
        for idx, (start_time, end_time) in enumerate(zip(start_times, end_times)):
            print(f"Start time: {start_time}, End time: {end_time}\n")
    print("Exiting...")

def merge_overlapping_ranges(starts, ends):
        intervals = sorted(zip(starts, ends), key=lambda x: x[0])
        merged = []

        for current in intervals:
            if not merged:
                merged.append(current)
            else:
                prev_start, prev_end = merged[-1]
                curr_start, curr_end = current

                if curr_start <= prev_end:  # Overlap or touching
                    merged[-1] = (prev_start, max(prev_end, curr_end))  # Merge
                else:
                    merged.append(current)
        return merged

def invert_intervals(deletion_intervals, video_length):
    keep_intervals = []
    prev_end = 0

    for start, end in deletion_intervals:
        if start > prev_end:
            keep_intervals.append((prev_end, start))
        prev_end = end

    if prev_end < video_length:
        keep_intervals.append((prev_end, video_length))

    return keep_intervals
