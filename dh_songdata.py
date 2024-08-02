import click, json
from pathlib import Path

from _songhelper import SongHelper

@click.command()
@click.option('--song-id', prompt='Enter the song ID', help='The unique identifier for the song.')
@click.option('--title', prompt='Enter the title', help='The title of the song.')
@click.option('--artist', prompt='Enter the artist', help='The artist of the song.')
@click.option('--coaches', prompt='Enter the number of coaches (1-6)', type=click.IntRange(1, 6), help='Number of coaches for the song.')
@click.option('--difficulty', prompt='Enter the difficulty (1: easy, 2: normal, 3: hard, 4: extreme)', type=click.Choice(['1', '2', '3', '4']), help='Difficulty level of the song.')
@click.option('--credits', prompt='Enter credits', help='Credits for the song.')
@click.option('--length', prompt='Enter the length of the song in seconds', type=int, help='Length of the song in seconds.')
@click.option('--is-available', prompt='Is the song available? (yes/no)', type=click.Choice(['yes', 'no']), help='Availability of the song.')
def create_song_data(song_id, title, artist, coaches, difficulty, credits, length, is_available):
    is_available = is_available == 'yes'

    helper = SongHelper(song_id)
    
    song_data = {
        "songId": song_id,
        "title": title,
        "artist": artist,
        "coaches": coaches,
        "difficulty": int(difficulty),
        "credits": credits,
        "length": length,
        "isAvailable": is_available
    }
    
    # Save to songFolder/songdata.dh
    output_path = helper.save_dh("songdata.dh", song_data)
    
    print(f"Generated songData for song '{song_id}', it was saved to f{output_path}")

if __name__ == '__main__':
    create_song_data()