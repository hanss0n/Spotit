import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

if os.getenv('SPOTIPY_CLIENT_ID') is not None:
    client_id = os.getenv('SPOTIPY_CLIENT_ID')
else:
    print('Enter client id:')
    client_id = str(input())
    os.environ['SPOTIPY_CLIENT_ID'] = client_id

if os.getenv('SPOTIPY_CLIENT_SECRET') is not None:
    client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
else:
    print('Enter client secret:')
    client_secret = str(input())
    os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret

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
