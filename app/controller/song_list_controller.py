from flask import Blueprint, request

song_list = Blueprint('song_list', __name__)


# TODO: implement
@song_list.route("/spotify_list/edges", methods=["GET"])
def edges():
    return "edges"


# TODO: implement
@song_list.route("/spotify_list/vertices", methods=["GET"])
def vertices():
    return "vertices"


# TODO: implement
@song_list.route("/spotify_list/<list_uri>", methods=["POST"])
def spotify_list_uri(list_uri):
    return list_uri
