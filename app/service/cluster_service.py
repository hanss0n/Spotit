from sklearn.cluster import MiniBatchKMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np


def __track_to_arr(feature_dict, features):
    song_id = feature_dict[0]
    track = [song_id]
    for i in range(len(features)):
        track.append(feature_dict[1][features[i]])
    return track


def __to_data_frame(song_list, cluster_features):
    tracks = []
    for song in song_list.items():
        tracks.append(__track_to_arr(song, cluster_features))

    song_data = pd.DataFrame(tracks, columns=['id'] + cluster_features)
    df_labels = song_data['id']
    df_songs = song_data[cluster_features]

    return df_songs, df_labels


def __cluster_data_frame(df_songs, df_labels, num_cluster):
    cluster = np.array(df_songs)
    scaler = StandardScaler()
    scaler.fit(cluster)
    cluster = scaler.transform(cluster)

    kmeans = MiniBatchKMeans(n_clusters=num_cluster, init='k-means++', random_state=111)
    kmeans = kmeans.fit(cluster).labels_
    cluster_dict = {cluster_label: [] for cluster_label in range(num_cluster)}

    for song_id, cluster_label in enumerate(kmeans):
        cluster_dict[cluster_label].append(df_labels[song_id])

    return cluster_dict


def cluster(song_list, features, num_clusters):
    df_songs, df_labels = __to_data_frame(song_list, features)
    return __cluster_data_frame(df_songs, df_labels, num_clusters)
