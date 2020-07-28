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

    # Find out the range of the time_signature attribute for the playlist
    min, max = get_time_signature_range(filtered_features_by_id)

    # Rescale the Key, Loudness, Tempo and time_signature features to [0, 1]
    scaled_features = rescale_features(filtered_features_by_id, min, max)

    return scaled_features



def filter_features(features_by_id):
    for track_features in features_by_id.items():

        # Filter out the non-number attributes
        filtered_features = {feature: value for (feature, value) in track_features[1].items() if isinstance(value, numbers.Number)}

        # And discard the duration attribute
        del filtered_features['duration_ms']

        # Replace the non-filtered attributes
        features_by_id[track_features[0]] = filtered_features

    return features_by_id


def get_time_signature_range(features_by_id):
    first_val = features_by_id[list(features_by_id.keys())[0]]['time_signature']
    min, max = first_val, first_val
    for track_features in features_by_id.items():
        time_sig = track_features[1]['time_signature']
        if time_sig > max:
            max = time_sig
        if time_sig < min:
            min = time_sig

    return min, max


def rescale_features(features_by_id, time_sig_min, time_sig_max):
    for track_features in features_by_id.items():

        rescaled_features = track_features[1]

        # Rescale the Key, Loudness, Tempo and time_signature features to [0, 1]
        # Key is denoted by standard Pitch Class notation, where -1 is used if no key is detected
        # We alter the current notation, [-1, 11] --> [0, 1]
        rescaled_features['key'] += 1
        rescaled_features['key'] /= 12

        # Loudness is previously measured in decibel, in range [-60, 0]. We want [0, 1]
        rescaled_features['loudness'] += 60
        rescaled_features['loudness'] /= 60

        # Tempo is measured in BPM. Spotify seems to measure up to 250 BPM, which is why this values is used for scaling
        rescaled_features['tempo'] /= 250

        # Time_signature does not have a set range, and therefore the min and max arguments will be used to decide the range
        # These are based on the min and max values found throughout the entire playlist
        rescaled_features['time_signature'] -= min
        rescaled_features['time_signature'] /= (max-min)


        del rescaled_features['time_signature']

        # Save the update values
        features_by_id[track_features[0]] = rescaled_features

    return features_by_id


