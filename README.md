# Clustrify

Clustrify allows Spotify users to group their playlists into clusters depending on the euclidian distance of the attributes of the songs. 
Thus, songs with similar attributes will be grouped together. This is especially useful if you're only interested in a specific type of music and don't want to listen through hours of playlists just to find the songs that suit your taste. 


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

In order to run this application, you will need python installed, as well as the following libraries:
* Flask - [installation link](https://pypi.org/project/Flask/)
* Flask_cors - [installation link](https://pypi.org/project/Flask-Cors/1.10.3/)
* Spotipy - [installation link](https://pypi.org/project/spotipy/)
* Scikit-learn - [installation link](https://pypi.org/project/scikit-learn/)
* Numpy - [installation link](https://pypi.org/project/numpy/)
* Pandas - [installation link](https://pypi.org/project/pandas/)

All of these can be installed via the package installer pip.

#### Spotipy

In order for the requests to the Spotify API to be valid, you also need to set up an account on their developer website. You have to create a Spotify application, with a Spotify Client ID, as well as a Spotify Client Secret. Instructions for this can be found on this [link](https://developer.spotify.com/dashboard/). 

Once this is properly setup, you will need to add both of these keys as variables for your environment:
```
export SPOTIPY_CLIENT_ID=client_id_here
export SPOTIPY_CLIENT_SECRET=client_secret_here

// on Windows, use `SET` instead of `export`
```
