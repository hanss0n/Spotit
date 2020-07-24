import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

print('Enter client id:')
client_id = str(input())

print('Enter client secret:')
client_secret = str(input())

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

print("Enter artist URI:")
playlist_url = input()

results = spotify.artist_albums(playlist_url, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])
