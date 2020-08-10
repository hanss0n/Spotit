from unittest import TestCase
from spotipy import SpotifyException
from service.spotify_service import get_tracks_by_list_id, fetch_features, filter_features, rescale_features


class TestSpotifyService(TestCase):

    # Test normal case for fetching all song_ids from a playlist
    def test_valid_get_tracks_by_list_id(self):
        test_list_uri = 'spotify:playlist:2OE6T7SwseiNXoBGk0Pcmx'
        track_list = get_tracks_by_list_id(test_list_uri)
        expected_ids = {'7ytR5pFWmSjzHJIeQkgog4', '1xQ6trAsedVPCdbtDAmk0c', '0VjIjW4GlUZAMYd2vXMi3b',
                        '6UelLqGlWMcVH1E5c4H7lY', '24Yi9hE78yPEbZ4kxyoXAI'}
        fetched_ids = set([track['track']['id'] for track in track_list])
        self.assertEqual(fetched_ids, expected_ids)

    # Test exception on bad uri
    def test_error_bad_uri_get_playlist_id_list(self):
        self.assertRaises(SpotifyException, get_tracks_by_list_id, 'asdasdg')

    # Test exception on empty uri
    def test_error_empty_uri_get_playlist_id_list(self):
        self.assertRaises(SpotifyException, get_tracks_by_list_id, '')

    # ------------------------------------------------------------------------------------------------------------------

    # Test normal case with 1 id
    def test_valid_one_id_fetch_features(self):
        ids = {'06AKEBrKUckW0KREUWRnvT'}
        features_to_consider = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'speechiness']
        features = fetch_features(ids, features_to_consider)
        expected_features = {'06AKEBrKUckW0KREUWRnvT': {'acousticness': 0.514, 'danceability': 0.735, 'energy': 0.578,
                                                        'instrumentalness': 0.0902, 'speechiness': 0.0461}
                             }
        self.assertEqual(features, expected_features)

    # Test normal case with 2 ids
    def test_valid_multiple_ids_fetch_features(self):
        ids = {'06AKEBrKUckW0KREUWRnvT', '7ytR5pFWmSjzHJIeQkgog4'}
        features_to_consider = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'speechiness']
        features = fetch_features(ids, features_to_consider)

        expected_features = {'06AKEBrKUckW0KREUWRnvT': {'acousticness': 0.514, 'danceability': 0.735, 'energy': 0.578,
                                                        'instrumentalness': 0.0902, 'speechiness': 0.0461},
                             '7ytR5pFWmSjzHJIeQkgog4': {'acousticness': 0.247, 'danceability': 0.746, 'energy': 0.69,
                                                        'instrumentalness': 0, 'speechiness': 0.164}
                             }
        self.assertEqual(features, expected_features)

    # Test that the only the correct features are considered
    def test_valid_filter_fetch_features(self):
        ids = {'06AKEBrKUckW0KREUWRnvT'}
        features_to_consider = {'acousticness', 'danceability', 'energy', 'instrumentalness', 'speechiness'}
        features = fetch_features(ids, features_to_consider)
        self.assertEqual(features['06AKEBrKUckW0KREUWRnvT'].keys(), features_to_consider)

    # Test that supplying an empty list of features to consider leads to that all numerical features are considered
    def test_valid_empty_filter_fetch_features(self):
        ids = {'06AKEBrKUckW0KREUWRnvT'}
        features_to_consider = {}
        features = fetch_features(ids, features_to_consider)
        expected_features = {'acousticness', 'danceability', 'energy', 'instrumentalness', 'speechiness'}
        self.assertEqual(features['06AKEBrKUckW0KREUWRnvT'].keys(), expected_features)

    # Test that all features are scaled between 0-1
    def test_valid_scale_fetch_features(self):
        ids = {'06AKEBrKUckW0KREUWRnvT'}
        features_to_consider = {}
        features = fetch_features(ids, features_to_consider)
        for value in features['06AKEBrKUckW0KREUWRnvT'].values():
            self.assertTrue(0 <= value <= 1)

    # Test exception on bad id
    def test_error_bad_id_fetch_features(self):
        ids = ['adasdasd']
        features_to_consider = {'acousticness', 'danceability', 'energy', 'instrumentalness', 'speechiness'}
        self.assertRaises(SpotifyException, fetch_features, ids, features_to_consider)

    # Test exception on empty id
    def test_error_empty_id_fetch_features(self):
        ids = []
        features_to_consider = {'acousticness', 'danceability', 'energy', 'instrumentalness', 'speechiness'}
        self.assertRaises(SpotifyException, fetch_features, ids, features_to_consider)

    # ------------------------------------------------------------------------------------------------------------------

    # Test that the only the correct features are considered
    def test_valid_filter_filter_features(self):
        features_by_id = {
            '06AKEBrKUckW0KREUWRnvT': {'danceability': 0.735, 'energy': 0.578, 'key': 5, 'loudness': -11.84, 'mode': 0,
                                       'speechiness': 0.0461, 'acousticness': 0.514, 'instrumentalness': 0.0902,
                                       'liveness': 0.159, 'valence': 0.636, 'tempo': 98.002, 'type': 'audio_features',
                                       'id': '06AKEBrKUckW0KREUWRnvT', 'uri': 'spotify:track:06AKEBrKUckW0KREUWRnvT',
                                       'track_href': 'https://api.spotify.com/v1/tracks/06AKEBrKUckW0KREUWRnvT',
                                       'analysis_url': 'https://api.spotify.com/v1/audio-analysis'
                                                       '/06AKEBrKUckW0KREUWRnvT',
                                       'duration_ms': 255349, 'time_signature': 4}
        }
        features_to_consider = {'acousticness', 'danceability', 'energy', 'instrumentalness', 'speechiness'}
        features = filter_features(features_by_id, features_to_consider)
        self.assertEqual(features['06AKEBrKUckW0KREUWRnvT'].keys(), features_to_consider)

    # Test that all numeric features are considered
    def test_no_filter_filter_features(self):
        features_by_id = {
            '06AKEBrKUckW0KREUWRnvT': {'danceability': 0.735, 'energy': 0.578, 'key': 5, 'loudness': -11.84, 'mode': 0,
                                       'speechiness': 0.0461, 'acousticness': 0.514, 'instrumentalness': 0.0902,
                                       'liveness': 0.159, 'valence': 0.636, 'tempo': 98.002, 'type': 'audio_features',
                                       'id': '06AKEBrKUckW0KREUWRnvT', 'uri': 'spotify:track:06AKEBrKUckW0KREUWRnvT',
                                       'track_href': 'https://api.spotify.com/v1/tracks/06AKEBrKUckW0KREUWRnvT',
                                       'analysis_url': 'https://api.spotify.com/v1/audio-analysis'
                                                       '/06AKEBrKUckW0KREUWRnvT',
                                       'duration_ms': 255349, 'time_signature': 4}
        }
        features_to_consider = {}
        expected_features = {'acousticness', 'danceability', 'energy', 'instrumentalness', 'speechiness'}
        features = filter_features(features_by_id, features_to_consider)
        self.assertEqual(features['06AKEBrKUckW0KREUWRnvT'].keys(), expected_features)

    # Test that duraion_ms is not considered
    def test_no_duration_filter_features(self):
        features_by_id = {
            '06AKEBrKUckW0KREUWRnvT': {'danceability': 0.735, 'energy': 0.578, 'key': 5, 'loudness': -11.84, 'mode': 0,
                                       'speechiness': 0.0461, 'acousticness': 0.514, 'instrumentalness': 0.0902,
                                       'liveness': 0.159, 'valence': 0.636, 'tempo': 98.002, 'type': 'audio_features',
                                       'id': '06AKEBrKUckW0KREUWRnvT', 'uri': 'spotify:track:06AKEBrKUckW0KREUWRnvT',
                                       'track_href': 'https://api.spotify.com/v1/tracks/06AKEBrKUckW0KREUWRnvT',
                                       'analysis_url': 'https://api.spotify.com/v1/audio-analysis'
                                                       '/06AKEBrKUckW0KREUWRnvT',
                                       'duration_ms': 255349, 'time_signature': 4}
        }
        features_to_consider = {'acousticness', 'danceability', 'energy', 'instrumentalness', 'speechiness',
                                'duration_ms'}
        expected_features = {'acousticness', 'danceability', 'energy', 'instrumentalness', 'speechiness'}
        features = filter_features(features_by_id, features_to_consider)
        self.assertEqual(features['06AKEBrKUckW0KREUWRnvT'].keys(), expected_features)

    # Test that all time_signature is not considered
    def test_no_time_signature_filter_features(self):
        features_by_id = {
            '06AKEBrKUckW0KREUWRnvT': {'danceability': 0.735, 'energy': 0.578, 'key': 5, 'loudness': -11.84, 'mode': 0,
                                       'speechiness': 0.0461, 'acousticness': 0.514, 'instrumentalness': 0.0902,
                                       'liveness': 0.159, 'valence': 0.636, 'tempo': 98.002, 'type': 'audio_features',
                                       'id': '06AKEBrKUckW0KREUWRnvT', 'uri': 'spotify:track:06AKEBrKUckW0KREUWRnvT',
                                       'track_href': 'https://api.spotify.com/v1/tracks/06AKEBrKUckW0KREUWRnvT',
                                       'analysis_url': 'https://api.spotify.com/v1/audio-analysis'
                                                       '/06AKEBrKUckW0KREUWRnvT',
                                       'duration_ms': 255349, 'time_signature': 4}
        }
        features_to_consider = {'acousticness', 'danceability', 'energy', 'instrumentalness', 'speechiness',
                                'time_signature'}
        expected_features = {'acousticness', 'danceability', 'energy', 'instrumentalness', 'speechiness'}
        features = filter_features(features_by_id, features_to_consider)
        self.assertEqual(features['06AKEBrKUckW0KREUWRnvT'].keys(), expected_features)

    # Test that non-numeric features are not considered
    def test_no_non_numeric_filter_features(self):
        features_by_id = {
            '06AKEBrKUckW0KREUWRnvT': {'danceability': 0.735, 'energy': 0.578, 'key': 5, 'loudness': -11.84, 'mode': 0,
                                       'speechiness': 0.0461, 'acousticness': 0.514, 'instrumentalness': 0.0902,
                                       'liveness': 0.159, 'valence': 0.636, 'tempo': 98.002, 'type': 'audio_features',
                                       'id': '06AKEBrKUckW0KREUWRnvT', 'uri': 'spotify:track:06AKEBrKUckW0KREUWRnvT',
                                       'track_href': 'https://api.spotify.com/v1/tracks/06AKEBrKUckW0KREUWRnvT',
                                       'analysis_url': 'https://api.spotify.com/v1/audio-analysis'
                                                       '/06AKEBrKUckW0KREUWRnvT',
                                       'duration_ms': 255349, 'time_signature': 4}
        }
        features_to_consider = {'acousticness', 'danceability', 'energy', 'instrumentalness', 'speechiness',
                                'type', 'id', 'uri', 'track_href', 'analysis_url'}
        expected_features = {'acousticness', 'danceability', 'energy', 'instrumentalness', 'speechiness'}
        features = filter_features(features_by_id, features_to_consider)
        self.assertEqual(features['06AKEBrKUckW0KREUWRnvT'].keys(), expected_features)

    # ------------------------------------------------------------------------------------------------------------------

    # Test valid rescaling of key, loudness and tempo
    def test_valid_rescale_features(self):
        features = {'06AKEBrKUckW0KREUWRnvT': {'key': 5, 'loudness': -11.84, 'tempo': 98.002}}
        rescaled_features = rescale_features(features)
        for value in rescaled_features['06AKEBrKUckW0KREUWRnvT'].values():
            self.assertTrue(0 <= value <= 1)

    # Test rescaling when none of key, loudness or tempo are used. This should not raise an error
    def test_valid_no_rescale_features(self):
        features = {'06AKEBrKUckW0KREUWRnvT': {'acousticness': 0.514, 'danceability': 0.735, 'energy': 0.578,
                                               'instrumentalness': 0.0902, 'speechiness': 0.0461}
                    }
        try:
            rescale_features(features)
        except KeyError:
            self.fail('rescaled_feature() raised a KeyError unexpectedly')
