from app.service.cluster_service import cluster
from app.service.spotify_service import get_playlist_id_list, fetch_features
import json


def get_cluster_by_list_id(list_id):
    song_ids = get_playlist_id_list(list_id)
    song_features = fetch_features(song_ids)
    features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'speechiness']
    return cluster(song_features, features, 5)


def convert_cluster_to_json(cluster):
    tracks = {'track_list': []}
    for track in cluster:
        track_info = fetch_track(track['song_id'])
        track_info['cluster_id'] = track['cluster_id']
        tracks['track_list'].append(track_info)

    return json.dumps(tracks)

