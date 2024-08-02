import os, json
from pathlib import Path

song_export_folder = "./_songs"

class SongHelper:
    def __init__(self, song_id):
        self.song_id = song_id
        self.song_folder = Path("./_songs", self.song_id.lower()).resolve()
        self.song_folders = ["audio", "textures", "timeline", "video"]

        # Create all necessary files for a song
        for folder in self.song_folders:
            f = Path(self.song_folder, folder).resolve()
            if not f.exists():
                f.mkdir(parents=True)

    def save_dh(self, path, data):
        file_path = Path(self.song_folder, path).resolve()
        # Create the parent folder if it doesn't exist (ex: audio/, timeline/ etc.)
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True)
        
        with open(file_path, 'w') as f:
            f.write(json.dumps(data, indent=4))
        
        return file_path