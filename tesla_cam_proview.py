import os
import sys
from pathlib import Path
from moviepy.editor import (
    VideoFileClip,
    CompositeVideoClip,
    concatenate_videoclips
)
from moviepy.video.fx.all import resize

def find_teslacam_usb():
    for drive_letter in range(ord('A'), ord('Z')):
        path = f"{chr(drive_letter)}:\\TeslaCam\\SavedClips"
        if os.path.isdir(path):
            return path
    return None

def combine_videos(input_folder, output_folder):
    for root, dirs, files in os.walk(input_folder):
        files = [file for file in files if file.lower().endswith('.mp4')]
        
        if files:
            files.sort()
            print(f"Processing folder: {root}")

            combined_clips = {'front': [], 'back': [], 'left_repeater': [], 'right_repeater': []}

            for file in files:
                angle = None
                if 'front' in file.lower():
                    angle = 'front'
                elif 'back' in file.lower():
                    angle = 'back'
                elif 'left_repeater' in file.lower():
                    angle = 'left_repeater'
                elif 'right_repeater' in file.lower():
                    angle = 'right_repeater'

                if angle:
                    combined_clips[angle].append(VideoFileClip(os.path.join(root, file)))

            for angle in combined_clips.keys():
                combined_clips[angle] = concatenate_videoclips(combined_clips[angle])

            front_clip = resize(combined_clips['front'], (640, 360)).set_position(('center', 'top'))
            back_clip = resize(combined_clips['back'], (320, 180)).set_position(('center', 'bottom'))
            left_clip = resize(combined_clips['left_repeater'], (320, 180)).set_position(('left', 'bottom'))
            right_clip = resize(combined_clips['right_repeater'], (320, 180)).set_position(('right', 'bottom'))

            back_clip = back_clip.set_position(('center', 380))  # Lower the back_clip by setting the y-coordinate manually

            combined_display = CompositeVideoClip([front_clip, back_clip, left_clip, right_clip], size=(960, 540))

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
            
    for root, dirs, files in os.walk(input_folder):
        files = [file for file in files if file.lower().endswith('.mp4')]
        
        if files:
            files.sort()
            print(f"Processing folder: {root}")

            combined_clips = {'front': [], 'back': [], 'left_repeater': [], 'right_repeater': []}

            for file in files:
                angle = None
                if 'front' in file.lower():
                    angle = 'front'
                elif 'back' in file.lower():
                    angle = 'back'
                elif 'left_repeater' in file.lower():
                    angle = 'left_repeater'
                elif 'right_repeater' in file.lower():
                    angle = 'right_repeater'

                if angle:
                    combined_clips[angle].append(VideoFileClip(os.path.join(root, file)))

            for angle in combined_clips.keys():
                combined_clips[angle] = concatenate_videoclips(combined_clips[angle])

            front_clip = resize(combined_clips['front'], (640, 360)).set_position(('center', 'top'))
            back_clip = resize(combined_clips['back'], (320, 180)).set_position(('center', 380))
            left_clip = resize(combined_clips['left_repeater'], (320, 180)).set_position(('left', 'bottom'))
            right_clip = resize(combined_clips['right_repeater'], (320, 180)).set_position(('right', 'bottom'))

            back_clip = back_clip.set_position(lambda t: ('center', left_clip.screenpos(t)[1] + 20))  # Lower the back_clip by 20 pixels

            combined_display = CompositeVideoClip([front_clip, back_clip, left_clip, right_clip], size=(960, 540))

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

    for root, dirs, files in os.walk(input_folder):
        files = [file for file in files if file.lower().endswith('.mp4')]
        
        if files:
            files.sort()
            print(f"Processing folder: {root}")

            combined_clips = {'front': [], 'back': [], 'left_repeater': [], 'right_repeater': []}

            for file in files:
                angle = None
                if 'front' in file.lower():
                    angle = 'front'
                elif 'back' in file.lower():
                    angle = 'back'
                elif 'left_repeater' in file.lower():
                    angle = 'left_repeater'
                elif 'right_repeater' in file.lower():
                    angle = 'right_repeater'

                if angle:
                    combined_clips[angle].append(VideoFileClip(os.path.join(root, file)))

            for angle in combined_clips.keys():
                combined_clips[angle] = concatenate_videoclips(combined_clips[angle])

            front_clip = resize(combined_clips['front'], (640, 360)).set_position(('center', 'top'))
            back_clip = resize(combined_clips['back'], (320, 180)).set_position(('center', 'bottom'))
            left_clip = resize(combined_clips['left_repeater'], (320, 180)).set_position(('left', 'bottom'))
            right_clip = resize(combined_clips['right_repeater'], (320, 180)).set_position(('right', 'bottom'))

            back_clip = back_clip.set_y(lambda t: left_clip.screenpos(t)[1] + 20)  # Lower the back_clip by 20 pixels

            combined_display = CompositeVideoClip([front_clip, back_clip, left_clip, right_clip], size=(960, 540))

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