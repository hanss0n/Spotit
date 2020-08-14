# Clustrify

# [TRY IT HERE](https://hanss0n.github.io/Clustrify/)

Clustrify allows Spotify users to group their playlists into clusters depending on the euclidian distance of the attributes of the songs. 
Thus, songs with similar attributes will be grouped together. This is especially useful if you're only interested in a specific type of music and don't want to listen through hours of playlists just to find the songs that suit your taste. 


## Getting Started - Backend

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

In order to run this application, you will need python3 installed, as well as the following libraries:
* Flask - [installation link](https://pypi.org/project/Flask/)
* Flask_cors - [installation link](https://pypi.org/project/Flask-Cors/1.10.3/)
* Spotipy - [installation link](https://pypi.org/project/spotipy/)
* Scikit-learn - [installation link](https://pypi.org/project/scikit-learn/)
* Numpy - [installation link](https://pypi.org/project/numpy/)
* Pandas - [installation link](https://pypi.org/project/pandas/)

All of these can be installed via the package installer pip.

### Installing

#### Spotipy

In order for the requests to the Spotify API to be valid, you also need to set up an account on their developer website. You have to create a Spotify application, with a Spotify Client ID, as well as a Spotify Client Secret. Instructions for this can be found on this [link](https://developer.spotify.com/dashboard/). 

We use the Spotipy lirary to access the API, for which you will need to add both of these keys to your environment:
```
export SPOTIPY_CLIENT_ID=client_id_here
export SPOTIPY_CLIENT_SECRET=client_secret_here

// on Windows, use `SET` instead of `export`
```
**Note that it is SpotiPy with a P, not the regular F**

#### Setup `$PYTHONPATH`
We also have to setup the `PYTHONPATH` by adding the Clustrify directory to it: 
```
export PYTHONPATH=${PYTHONPATH}:${PWD}
```

## Deployment - Backend
Finally, the backend can be deployed:
```
python3 app/run.py
```
**Note that this should be ran in the top, Clustrify directory**


### Demo 
So, now that the Clustrify backend is up and running, let's make sure that it is working. In the file ``song_list_controller.py``, you can find all the endpoints that are defined. For simplicty's sake, let's do this via the use of `Postman`, an application that let's you make HTTP requests easily. 

Pick the `POST` option, and supply the adress for the backend. Both the IP-adress and port should have been made available to you in the terminal when you started up the application. Then click the `Body` header, followed by `text` (depending on version, it might be `raw`), and finally, choose `JSON`. In the textbox appearing below, enter:
```
{
    "list_uri": "playlist_uri",
    "num_clusters" : "5",
    "attributes": ["acousticness", "danceability", "energy", "instrumentalness", "speechiness"]
}
```

To get the ``playlist_uri``, you can open up `Spotify`, rightclick on a playlist, choose `Share` and finally `Copy Spotify URI`. It should take a form similar to `spotify:playlist:59ZbFPES4DQwEjBpWHzrtC`. 

If all of this is done correctly, you will receive a JSON response containing information of all the trakcs in the choosen playlist, as well as some information detailing which cluster it belongs to. 