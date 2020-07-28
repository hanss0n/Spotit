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


def get_scalar_song_features(song_id):
    # Fetch all of the features of the track
    features = spotify.audio_features(song_id)[0]

    # Filter out the non-number attributes
    filtered_features = {attribute: value for (attribute, value) in features.items() if isinstance(value, numbers.Number)}

    # And discard the duration attribute
    del filtered_features['duration_ms']

    # Rescale the Key, Loudness, Tempo and time_signature features to [0, 1]
    # Key is denoted by standard Pitch Class notation, where -1 is used if no key is detected
    # We alter the current notation, [-1, 11] --> [0, 1]
    filtered_features['key'] += 1
    filtered_features['key'] /= 12

    # Loudness is previously measured in decibel, in range [-60, 0]. We want [0, 1]
    filtered_features['loudness'] += 60
    filtered_features['loudness'] /= 60

    # Tempo is measured in BPM. Spotify seems to measure up to 250 BPM, which is why this values is used for scaling
    filtered_features['tempo'] /= 250

    # TODO: Time_signature
    filtered_features['time_signature'] = filtered_features['time_signature']

    return filtered_features




