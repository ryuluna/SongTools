import sys
import os
import inquirer
import subprocess

from pathlib import Path

from _songhelper import SongHelper

def process_video(song_id, video_path):
    helper = SongHelper(song_id)

    input_dir = video_path.parent
    filename = video_path.stem

    output_file = Path(helper.song_folder, f"video/{song_id}.ogv".lower()).resolve()

    # Define ffmpeg command options
    cmd = [
        'ffmpeg',
        '-y',  # Overwrite output files without asking
        '-i', str(video_path),
        '-c:v', 'libtheora',
        '-q:v', '7',
        '-b:v', '8000k',
        '-qscale:v', '10',
        '-r', '25',
        '-an',  # Disable audio
        str(output_file)
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"Video processed and saved as '{output_file}' for song ID '{song_id}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error processing video: {e}")

def main():
    # Handle drag-and-drop or CLI path input
    if len(sys.argv) > 1:
        video_path = Path(sys.argv[1])
    else:
        if not sys.stdin.isatty():
            video_path = Path(sys.stdin.read().strip())
        else:
            video_path = None

    if video_path is None:
        print("No video path provided. Please drag and drop the file onto the script or provide it via CLI.")
        return

    video_path = Path(video_path)

    if not video_path.is_file():
        print(f"Error: The file '{video_path}' does not exist.")
        return

    # Ask for song ID using inquirer
    questions = [
        inquirer.Text('song_id',
                      message="What's the songId?")
    ]
    answers = inquirer.prompt(questions)
    song_id = answers["song_id"]

    # Process the video
    process_video(song_id, video_path)

if __name__ == '__main__':
    main()
