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

NUMBER_PLATE = "BT70WTV"

def find_teslacam_usb():
    for drive_letter in range(ord("A"), ord("Z")):
        path = f"{chr(drive_letter)}:\\TeslaCam\\SavedClips"
        if os.path.isdir(path):
            return path
    return None

def draw_text(t, timestamp):
    current_time = timestamp + timedelta(seconds=t)
    text = f"{current_time.strftime('%Y/%m/%d %H:%M:%S')}   {NUMBER_PLATE}"
    image = Image.new('RGBA', (320, 20), (0, 0, 0, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 16)  # Change the font size to 16
    draw.text((160 - draw.textsize(text, font=font)[0] // 2, 0), text, font=font, fill=(255, 255, 255, 255))
    return np.array(image)

def create_timestamp_video_clip(timestamp, duration):
    return VideoClip(make_frame=lambda t: draw_text(t, timestamp)[:,:,:3], duration=duration)

def combine_videos(input_folder, output_folder):
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

            front_clip = resize(combined_clips["front"], (640, 360)).set_position(("center", "top"))
            back_clip = resize(combined_clips["back"], (320, 180)).set_position(("center", 380))
            left_clip = resize(combined_clips["left_repeater"], (320, 180)).set_position(("left", "bottom"))
            right_clip = resize(combined_clips["right_repeater"], (320, 180)).set_position(("right", "bottom"))

            timestamp = datetime.strptime(os.path.basename(root), "%Y-%m-%d_%H-%M-%S")
            timestamp_clip = create_timestamp_video_clip(timestamp, combined_clips["front"].duration).set_position(
                ("center", 360)  # Move the timestamp to the desired position
            )

            combined_display = CompositeVideoClip(
                [front_clip, back_clip, left_clip, right_clip, timestamp_clip],
                size=(960, 540),
            )

            # Generate a 5-second preview
            preview_duration = 5
            combined_display = combined_display.subclip(0, preview_duration)

            output_filename = f"{output_folder}\\{os.path.basename(root)}-combined-preview.mp4"
            print(f"Saving combined video preview: {output_filename}")

            combined_display.write_videofile(
                output_filename,
                fps=15,
                bitrate="500k",
                codec="h264_nvenc",  # Use NVIDIA GPU-accelerated encoding
                threads=8,  # Increase number of threads for faster processing
                ffmpeg_params=["-preset", "fast"],  # Use a faster preset for encoding
            )

if __name__ == "__main__":
    teslacam_path = find_teslacam_usb()

    if teslacam_path is None:
        print("TeslaCam USB stick not found!")
        sys.exit(1)

    output_path = "C:\\TeslaCam"
    Path(output_path).mkdir(exist_ok=True)

    combine_videos(teslacam_path, output_path)

    print("Done! Combined video previews saved in C:\\TeslaCam")