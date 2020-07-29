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


def preprocess_features(track_ids):
    # Fetch the audio features of each track
    features = spotify.audio_features(track_ids)

    # Store by id for simplicitys sake
    features_by_track_id = {features[i]['id']: features[i] for i in range(len(features))}

    # Filter out unwanted features
    filtered_features_by_id = filter_features(features_by_track_id)

    return filtered_features_by_id


def filter_features(features_by_id):
    for track_features in features_by_id.items():

        # Filter out the non-number attributes
        filtered_features = {feature: value for (feature, value) in track_features[1].items() if isinstance(value, numbers.Number)}

        # And discard the unwanted number-attributes
        del filtered_features['duration_ms']
        del filtered_features['key']
        del filtered_features['mode']
        del filtered_features['time_signature']
        del filtered_features['liveness']
        del filtered_features['loudness']
        del filtered_features['valence']
        del filtered_features['tempo']
        
        # Replace the non-filtered attributes
        features_by_id[track_features[0]] = filtered_features

    return features_by_id

