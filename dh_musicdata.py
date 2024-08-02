import click
import json

from _songhelper import SongHelper

@click.command()
@click.option('--song-id', prompt='Enter the song ID', help='The unique identifier for the song.')
@click.option('--bpm', prompt='Enter the BPM (beats per minute)', type=int, help='Beats per minute of the music.')
@click.option('--video-offset', prompt='Enter the video offset (in seconds)', type=int, help='Offset for the video in seconds.')
@click.option('--audio-offset', prompt='Enter the audio offset (in seconds)', type=float, help='Offset for the audio in seconds.')
def create_music_data(song_id, bpm, video_offset, audio_offset):
    helper = SongHelper(song_id)

    # Create the music data dictionary
    music_data = {
        "bpm": bpm,
        "videoOffset": video_offset,
        "audioOffset": audio_offset
    }
    
    # Save to songFolder/audio/musicdata.dh
    output_path = helper.save_dh("audio/musicdata.dh", music_data)
    
    print(f"Generated songData for song '{song_id}', it was saved to f{output_path}")

if __name__ == '__main__':
    create_music_data()