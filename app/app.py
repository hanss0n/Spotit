import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

print('Enter client id:')
client_id = str(input())

print('Enter client secret:')
client_secret = str(input())

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

print("Enter artist URI:")
playlist_url = input()

results = spotify.playlist(playlist_url)
print(json.dumps(results, indent=4))
