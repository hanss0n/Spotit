from app.service.cluster_service import cluster
from app.service.spotify_service import get_tracks_by_list_id, fetch_features, fetch_track
import json


def get_cluster_by_track_ids(track_ids, num_of_clusters=5):
    features_to_consider = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'speechiness']
    song_features = fetch_features(track_ids, features_to_consider)
    return cluster(song_features, features_to_consider, num_of_clusters)


def get_json_track_list_by_list_id(list_id):
    # Get a list of tracks
    track_list = get_tracks_by_list_id(list_id)

    # Extract the ids of the tracks
    track_ids = [track['track']['id'] for track in track_list]

    # Create a cluster from the tracks
    cluster = get_cluster_by_track_ids(track_ids)

    # Append the cluster_id to the track_list
    for track in track_list:
        # Add the cluster_id (as a normal int, as opposed to int32)
        track['track']['cluster_id'] = int(cluster[track['track']['id']])

    # Convert the cluster into json format
    return json.dumps(track_list, indent=4)
