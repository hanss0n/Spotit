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
    song_list = ss.get_playlist_id_list('spotify:playlist:37i9dQZF1DWTK0zSEQRNUd')
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

    km = MiniBatchKMeans(n_clusters=k, init='k-means++', random_state=123)
    km = km.fit(cluster).labels_
    cluster_labels = [[] for i in range(k)]

    for i, j in enumerate(km):
        cluster_labels[j].append(labels[i])

    print(cluster_labels)
    return song_data


def cluster_songs(num_clusters, song_features):
    print("lol")


if __name__ == '__main__':
    to_data_frame("lololol")
