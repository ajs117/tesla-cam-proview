import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

from moviepy.editor import (
    VideoFileClip,
    CompositeVideoClip,
    concatenate_videoclips,
    VideoClip
)
from moviepy.video.fx.all import resize
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def find_teslacam_usb():
    for drive_letter in range(ord("A"), ord("Z")):
        path = f"{chr(drive_letter)}:\\TeslaCam\\SavedClips"
        if os.path.isdir(path):
            return path
    return None

def draw_text(t, timestamp, number_plate):
    current_time = timestamp + timedelta(seconds=t)
    text = f"{current_time.strftime('%Y/%m/%d %H:%M:%S')}   {number_plate}"
    image = Image.new('RGBA', (320, 20), (0, 0, 0, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 16)  # Change the font size to 16
    draw.text((160 - draw.textsize(text, font=font)[0] // 2, 0), text, font=font, fill=(255, 255, 255, 255))
    return np.array(image)

def create_timestamp_video_clip(timestamp, duration, number_plate):
    return VideoClip(make_frame=lambda t: draw_text(t, timestamp, number_plate)[:,:,:3], duration=duration)

def combine_videos(input_folder, output_folder, number_plate, quality_setting):
    if quality_setting == "low":
        fps = 1
        bitrate = "50k"
        codec = "libx264"
        ffmpeg_params = ["-preset", "ultrafast"]
        high_quality_factor = 1
    elif quality_setting == "medium":
        fps = 24
        bitrate = "5M"
        codec = "libx264"
        ffmpeg_params = ["-preset", "fast"]
        high_quality_factor = 1
    else: # quality_setting == "high"
        fps = 30
        bitrate = "15M"
        codec = "libx264"
        ffmpeg_params = ["-preset", "medium"]
        high_quality_factor = 2

    for root, dirs, files in os.walk(input_folder):
        files = [file for file in files if file.lower().endswith(".mp4")]

        if files:
            files.sort()
            print(f"Processing folder: {root}")

            combined_clips = {
                "front": [],
                "back": [],
                "left_repeater": [],
                "right_repeater": [],
            }

            for file in files:
                angle = None
                if "front" in file.lower():
                    angle = "front"
                elif "back" in file.lower():
                    angle = "back"
                elif "left_repeater" in file.lower():
                    angle = "left_repeater"
                elif "right_repeater" in file.lower():
                    angle = "right_repeater"

                if angle:
                    combined_clips[angle].append(VideoFileClip(os.path.join(root, file)))

            for angle in combined_clips.keys():
                combined_clips[angle] = concatenate_videoclips(combined_clips[angle])

            front_clip_width = 640 * high_quality_factor
            other_clip_width = 320 * high_quality_factor
            front_clip_height = 360 * high_quality_factor
            other_clip_height = 180 * high_quality_factor

            front_clip = resize(combined_clips["front"], (front_clip_width, front_clip_height)).set_position(("center", "top"))
            back_clip = resize(combined_clips["back"], (other_clip_width, other_clip_height)).set_position(("center", "top")).set_position(("center", front_clip_height + 20))
            left_clip = resize(combined_clips["left_repeater"], (other_clip_width, other_clip_height)).set_position(("right", "bottom"))
            right_clip = resize(combined_clips["right_repeater"], (other_clip_width, other_clip_height)).set_position(("left", "bottom"))

            timestamp = datetime.strptime(os.path.basename(root), "%Y-%m-%d_%H-%M-%S")
            timestamp_clip = create_timestamp_video_clip(timestamp, combined_clips["front"].duration, number_plate).set_position(
                ("center", front_clip_height)  # Move the timestamp to the desired position
            )

            combined_display = CompositeVideoClip(
                [front_clip, back_clip, left_clip, right_clip, timestamp_clip],
                size=(960 * high_quality_factor, 540 * high_quality_factor),
            )

            # # Generate a 5-second preview
            # preview_duration = 5
            # combined_display = combined_display.subclip(0, preview_duration)

            output_filename = f"{output_folder}\\{os.path.basename(root)}-{number_plate}.mp4"
            print(f"Saving combined video preview: {output_filename}")

            combined_display.write_videofile(
                output_filename,
                fps=fps,
                bitrate=bitrate,
                codec=codec,
                threads=8,
                ffmpeg_params=ffmpeg_params,
            )

def main():
    try:
        if getattr(sys, 'frozen', False):
            executable_path = sys.executable
        else:
            executable_path = os.path.abspath(__file__)
        
        executable_filename = os.path.basename(executable_path)

        # Extract number plate and quality setting from the filename
        quality_setting = None
        if '-' in executable_filename:
            parts = executable_filename.split('-')
            number_plate = parts[1]

            # Check if there is a quality setting after the number plate
            if len(parts) > 2 and parts[2].rstrip('.exe'):
                quality_setting = parts[2].rstrip('.exe')

    except:
        number_plate = ""
        quality_setting = None

    print(f"Number plate: {number_plate}")
    print(f"Quality setting: {quality_setting}")

    teslacam_path = find_teslacam_usb()

    if teslacam_path is None:
        print("TeslaCam USB stick not found!")
        sys.exit(1)

    output_path = os.path.dirname(executable_path)
    Path(output_path).mkdir(exist_ok=True)

    combine_videos(teslacam_path, output_path, number_plate, quality_setting)

    print("Done! Combined video previews saved in C:\\TeslaCam")

if __name__ == "__main__":
    main()