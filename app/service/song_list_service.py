from app.service.cluster_service import cluster
from app.service.spotify_service import get_tracks_by_list_id, fetch_features, fetch_track
import json


def get_cluster_by_params(track_ids, num_of_clusters, features_to_consider):
    song_features = fetch_features(track_ids, features_to_consider)
    return cluster(song_features, features_to_consider, num_of_clusters)


def get_cluster_list_json(cluster_params):
    list_id = cluster_params["list_uri"]
    features_to_consider = cluster_params["attributes"]
    num_clusters = int(cluster_params["num_clusters"])

    # Get a list of tracks
    track_list = get_tracks_by_list_id(list_id)

    # Remove unnecessary tag
    track_list = [track["track"] for track in track_list]

    # Extract the ids of the tracks
    track_ids = [track['id'] for track in track_list]

    # Create a cluster from the tracks
    feature_cluster = get_cluster_by_params(track_ids, num_clusters, features_to_consider)

    # Extract cover art
    track_list = extract_cover_art(track_list)

    # Append the cluster_id to the track_list
    for track in track_list:
        # Add the cluster_id (as a normal int, as opposed to int32)
        track['cluster_id'] = int(feature_cluster[track['id']])

    # Convert the cluster into json format
    return json.dumps(track_list, indent=4)


def extract_cover_art(track_info):
    for track_features in track_info:
        track_features["image_url"] = track_features["album"]["images"][2]["url"]
        track_features.pop("album")
    return track_info
