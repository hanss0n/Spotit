# TODO: get rid of all spotify service code from here
import app.service.spotify_service as ss
import pandas as pd


def to_dataframe(song_features):
    tracks = []
    song_list = ss.get_playlist_id_list('spotify:playlist:1VAN3ouvQGhuGkgDdldSoi')
    song_list = ss.preprocess_features(song_list)

    for song in song_list.items():
        id = song[0]
        danceability = song[1]['danceability']
        energy = song[1]['energy']
        key = song[1]['key']
        loudness = song[1]['loudness']
        mode = song[1]['mode']
        speechiness = song[1]['speechiness']
        acousticness = song[1]['acousticness']
        instrumentalness = song[1]['instrumentalness']
        liveness = song[1]['liveness']
        valence = song[1]['valence']
        tempo = song[1]['tempo']
        time_signature = song[1]['time_signature']

        track = [id, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness,
                 valence, tempo, time_signature]
        tracks.append(track)

    song_data = pd.DataFrame(tracks,
                             columns=['id', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                                      'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
                                      'time_signature'])
    song_data.to_csv('song_data.csv', sep=',')
    df = pd.read_csv('song_data.csv')
    pd.options.display.max_columns = len(df.columns)
    print(df)


def cluster_songs(num_clusters, song_features):
    print("lol")

    # song_data = pd.DataFrame(song_list, columns=['id', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
    #                                             'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
    #                                             'time_signature'])
    # song_data.to_csv('song_data.csv', sep=',')


if __name__ == '__main__':
    to_dataframe("lololol")
