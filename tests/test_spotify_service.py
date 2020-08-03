from unittest import TestCase
from spotipy import SpotifyException
from service.spotify_service import get_playlist_id_list, fetch_features


class TestSpotifyService(TestCase):

    # Test normal case for fetching all song_ids from a playlist
    def test_valid_get_playlist_id_list(self):
        test_list_uri = 'spotify:playlist:2OE6T7SwseiNXoBGk0Pcmx'
        song_ids = set(get_playlist_id_list(test_list_uri))
        expected_ids = {'7ytR5pFWmSjzHJIeQkgog4', '1xQ6trAsedVPCdbtDAmk0c', '0VjIjW4GlUZAMYd2vXMi3b',
                        '6UelLqGlWMcVH1E5c4H7lY', '24Yi9hE78yPEbZ4kxyoXAI'}
        self.assertEqual(song_ids, expected_ids)

    # Test exception on bad uri
    def test_error_bad_uri_get_playlist_id_list(self):
        self.assertRaises(SpotifyException, get_playlist_id_list, 'asdasdg')

    # Test exception on empty uri
    def test_error_empty_uri_get_playlist_id_list(self):
        self.assertRaises(SpotifyException, get_playlist_id_list, '')

    # ------------------------------------------------------------------------------------------------------------------

    # Test normal case with 1 id
    def test_valid_one_id_fetch_features(self):
        ids = {'06AKEBrKUckW0KREUWRnvT'}
        features_to_consider = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'speechiness']
        features = fetch_features(ids, features_to_consider)
        self.assertEqual(features['06AKEBrKUckW0KREUWRnvT']['acousticness'], 0.514)
        self.assertEqual(features['06AKEBrKUckW0KREUWRnvT']['danceability'], 0.735)
        self.assertEqual(features['06AKEBrKUckW0KREUWRnvT']['energy'], 0.578)
        self.assertEqual(features['06AKEBrKUckW0KREUWRnvT']['instrumentalness'], 0.0902)
        self.assertEqual(features['06AKEBrKUckW0KREUWRnvT']['speechiness'], 0.0461)

    # Test normal case with 2 ids
    def test_valid_multiple_ids_fetch_features(self):
        ids = {'06AKEBrKUckW0KREUWRnvT', '7ytR5pFWmSjzHJIeQkgog4'}
        features_to_consider = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'speechiness']
        features = fetch_features(ids, features_to_consider)
        self.assertEqual(features['06AKEBrKUckW0KREUWRnvT']['acousticness'], 0.514)
        self.assertEqual(features['06AKEBrKUckW0KREUWRnvT']['danceability'], 0.735)
        self.assertEqual(features['06AKEBrKUckW0KREUWRnvT']['energy'], 0.578)
        self.assertEqual(features['06AKEBrKUckW0KREUWRnvT']['instrumentalness'], 0.0902)
        self.assertEqual(features['06AKEBrKUckW0KREUWRnvT']['speechiness'], 0.0461)

        self.assertEqual(features['7ytR5pFWmSjzHJIeQkgog4']['acousticness'], 0.247)
        self.assertEqual(features['7ytR5pFWmSjzHJIeQkgog4']['danceability'], 0.746)
        self.assertEqual(features['7ytR5pFWmSjzHJIeQkgog4']['energy'], 0.69)
        self.assertEqual(features['7ytR5pFWmSjzHJIeQkgog4']['instrumentalness'], 0)
        self.assertEqual(features['7ytR5pFWmSjzHJIeQkgog4']['speechiness'], 0.164)

    # Test that the only the correct features are considered
    def test_valid_filter_fetch_features(self):
        ids = {'06AKEBrKUckW0KREUWRnvT'}
        features_to_consider = {'acousticness', 'danceability', 'energy', 'instrumentalness', 'speechiness'}
        features = fetch_features(ids, features_to_consider)
        self.assertEqual(features['06AKEBrKUckW0KREUWRnvT'].keys(), features_to_consider)

        # Test that all features are scaled between 0-1

    # Test that supplying an empty list of features to consider leads to that all numerical features are considered
    def test_valid_empty_filter_fetch_features(self):
        ids = {'06AKEBrKUckW0KREUWRnvT'}
        features_to_consider = {}
        features = fetch_features(ids, features_to_consider)
        self.assertEqual(features['06AKEBrKUckW0KREUWRnvT'].keys(), {
            'key', 'mode', 'acousticness', 'danceability', 'energy',
            'instrumentalness', 'liveness', 'loudness', 'speechiness',
            'valence', 'tempo'
        })

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

