from app.service.cluster_service import cluster
from app.service.spotify_service import get_playlist_id_list, fetch_features


def get_cluster_by_list_id(list_id, num_of_clusters=5,
                                features_to_consider=['acousticness', 'danceability', 'energy', 'instrumentalness', 'speechiness']):
    song_ids = get_playlist_id_list(list_id)
    song_features = fetch_features(song_ids, features_to_consider)
    return cluster(song_features, features_to_consider, num_of_clusters)

