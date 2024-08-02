import sys
import os
import inquirer
import subprocess

from pathlib import Path

from _songhelper import SongHelper

def process_audio(song_id, audio_path):
    helper = SongHelper(song_id)

    output_file = Path(helper.song_folder, f"audio/{song_id}.ogg".lower()).resolve()

    # Define ffmpeg command options
    cmd = [
        'ffmpeg',
        '-y',  # Overwrite output files without asking
        '-i', str(audio_path),
        str(output_file)
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"Audio processed and saved as '{output_file}' for song ID '{song_id}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error processing audio: {e}")

def main():
    # Handle drag-and-drop or CLI path input
    if len(sys.argv) > 1:
        audio_path = Path(sys.argv[1])
    else:
        if not sys.stdin.isatty():
            audio_path = Path(sys.stdin.read().strip())
        else:
            audio_path = None

    if audio_path is None:
        print("No audio path provided. Please drag and drop the file onto the script or provide it via CLI.")
        return

    audio_path = Path(audio_path)

    if not audio_path.is_file():
        print(f"Error: The file '{audio_path}' does not exist.")
        return

    # Ask for song ID using inquirer
    questions = [
        inquirer.Text('song_id',
                      message="What's the songId?")
    ]
    answers = inquirer.prompt(questions)
    song_id = answers["song_id"]

    # Process the audio
    process_audio(song_id, audio_path)

if __name__ == '__main__':
    main()
