import sys
import os
import inquirer

from pathlib import Path
from PIL import Image

from _songhelper import SongHelper

# Define available texture types
TEXTURE_TYPES = {
    'flowcover': {
        "name": "Flow cover",
        "format": "png",
        "size": [960, 520],
        "suffix": "_flowcover.png"
    },
    'flowcoach':  {
        "name": "Flow cover",
        "format": "png",
        "size": [1024, 1024],
        "suffix": "_flowcoach.png"
    },
    'background':  {
        "name": "Flow cover",
        "format": "png",
        "size": [1920, 1080],
        "suffix": "_bkg.png"
    }
}

def process_texture(song_id, texture_path, texture_type):
    helper = SongHelper(song_id)

    if texture_type not in TEXTURE_TYPES:
        print(f"Error: Unknown texture type '{texture_type}'.")
        return

    texture_info = TEXTURE_TYPES[texture_type]
    suffix = texture_info["suffix"]
    texture_output_path = Path(helper.song_folder, f"textures/{song_id}{suffix}".lower()).resolve()

    # Open the image
    with Image.open(texture_path) as img:
        # Resize the image
        img_resized = img.resize(texture_info["size"])

        # Save the resized image
        img_resized.save(texture_output_path, format=texture_info["format"].upper())
        print(f"Texture processed and saved as '{texture_output_path}'.")

def main():
    # Handle drag-and-drop or CLI path input
    if len(sys.argv) > 1:
        texture_path = Path(sys.argv[1])
    else:
        if not sys.stdin.isatty():
            texture_path = Path(sys.stdin.read().strip())
        else:
            texture_path = None

    if texture_path is None:
        print("No texture path provided. Please drag and drop the file onto the script or provide it via CLI.")
        return

    texture_path = Path(texture_path)

    if not texture_path.is_file():
        print(f"Error: The file '{texture_path}' does not exist.")
        return

    # Ask for texture type using inquirer
    questions = [
        inquirer.Text('song_id',
                      message="What's the songId?"),
        inquirer.List('texture_type',
                      message="Select texture type",
                      choices=list(TEXTURE_TYPES.keys()))
    ]
    answers = inquirer.prompt(questions)
    song_id = answers["song_id"]
    texture_type = answers['texture_type']

    # Process the texture
    process_texture(song_id, texture_path, texture_type)

if __name__ == '__main__':
    main()