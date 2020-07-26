import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import numbers

# on error: set environment variables 'SPOTIPY_CLIENT_ID' and 'SPOTIPY_CLIENT_SECRET'
client_id = os.environ.get('SPOTIPY_CLIENT_ID')
client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_playlist_id_list(playlist_uri):
    tracks = spotify.playlist_tracks(playlist_uri, fields='items.track.id')['items']
    return [track['track']['id'] for track in tracks]


# TODO: carefully examine what features we want to include in calculations
def get_scalar_song_features(song_id):
    return [feature for feature in spotify.audio_features(song_id)[0].values() if isinstance(feature, numbers.Number)]
