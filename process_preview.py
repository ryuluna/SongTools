import sys, inquirer, subprocess, re

from pathlib import Path
from datetime import datetime, timedelta

from _songhelper import SongHelper

PREVIEW_MAX_LENGTH = 30

def validate_time_format(_, current):
    pattern = r'^\d{2}:\d{2}$'
    if not re.match(pattern, current):
        raise inquirer.errors.ValidationError('', reason="The time must be in the format MM:SS")
    return True

def process_audio_preview(song_id, preview_start):
    helper = SongHelper(song_id)

    input_path = Path(helper.song_folder, f"audio/{song_id}.ogg".lower()).resolve()
    if not input_path.exists():
        raise Exception(f"Audio file does not exist for song '{song_id}'!")
    
    output_file = Path(helper.song_folder, f"audio/{song_id}_audiopreview.ogg".lower()).resolve()

    # Define ffmpeg command options
    cmd = [
        'ffmpeg',
        '-y',  # Overwrite output files without asking
        '-i', str(input_path),
        '-ss', f'00:{preview_start}',
        '-t', f'30s',
        str(output_file)
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"Audio preview processed and saved as '{output_file}' for song ID '{song_id}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error processing audio preview: {e}")

def process_video_preview(song_id, preview_start):
    helper = SongHelper(song_id)

    input_path = Path(helper.song_folder, f"video/{song_id}.ogv".lower()).resolve()
    if not input_path.exists():
        raise Exception(f"Video file does not exist for song '{song_id}'!")
    
    output_file = Path(helper.song_folder, f"video/{song_id}_videopreview.ogv".lower()).resolve()

    # Define ffmpeg command options
    cmd = [
        'ffmpeg',
        '-y',  # Overwrite output files without asking
        '-i', str(input_path),
        '-c:v', 'libtheora',
        '-q:v', '7',
        '-b:v', '8000k',
        '-qscale:v', '10',
        '-r', '25',
        '-ss', f'00:{preview_start}',
        '-t', f'30s',
        '-an',  # Disable audio
        str(output_file)
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"Video preview processed and saved as '{output_file}' for song ID '{song_id}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error processing video preview: {e}")


def main():
    print("WARNING: You will need a processed audio and a video for this script.")
    print("If you don't have any, process them with 'process_audio' and 'process_video'.")

    # Ask for song ID using inquirer
    questions = [
        inquirer.Text('song_id',
                      message="What's the songId?"),
        inquirer.Text('preview_start',
                      message="When does the preview start? (In this format: 00:40 or 02:03)", 
                      validate=validate_time_format)
    ]
    answers = inquirer.prompt(questions)
    song_id = answers["song_id"]
    preview_start = answers["preview_start"]

    # Process audio and video preview
    process_audio_preview(song_id, preview_start)
    process_video_preview(song_id, preview_start)

    print("\nAll done!")

if __name__ == '__main__':
    main()
