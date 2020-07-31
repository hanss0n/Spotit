# TODO: get rid of all spotify service code from here
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.preprocessing import StandardScaler

import app.service.spotify_service as ss
import pandas as pd
import numpy as np


def track_to_arr(feature_dict):
    identifier = feature_dict[0]
    danceability = feature_dict[1]['danceability']
    energy = feature_dict[1]['energy']
    speechiness = feature_dict[1]['speechiness']
    acousticness = feature_dict[1]['acousticness']
    instrumentalness = feature_dict[1]['instrumentalness']

    return [identifier, danceability, energy, speechiness, acousticness, instrumentalness]


def to_data_frame(song_features):
    tracks = []
    song_list = ss.get_playlist_id_list('spotify:playlist:68cbyzto5Sm9aoMgHRatb6')
    song_list = ss.preprocess_features(song_list)

    for song in song_list.items():
        tracks.append(track_to_arr(song))

    song_data = pd.DataFrame(tracks, columns=['id', 'danceability', 'energy', 'speechiness',
                                              'acousticness', 'instrumentalness'])

    features = ['danceability', 'energy', 'speechiness',
                'acousticness', 'instrumentalness']

    labels = song_data['id']

    df_cluster = song_data[features]
    cluster = np.array(df_cluster)
    scaler = StandardScaler()
    scaler.fit(cluster)
    cluster = scaler.transform(cluster)
    k = 5

    km = MiniBatchKMeans(n_clusters=k, init='k-means++', random_state=111)
    km = km.fit(cluster).labels_

    cluster_dict = {cluster_label: [] for cluster_label in range(k)}

    for song_id, cluster_label in enumerate(km):
        cluster_dict[cluster_label].append(labels[song_id])

    return cluster_dict


def cluster_songs(num_clusters, song_features):
    print("lol")


if __name__ == '__main__':
    print(to_data_frame("lololol"))
