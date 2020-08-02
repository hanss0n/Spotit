from flask import Blueprint, request
from app.service import song_list_service
import json

song_list = Blueprint('song_list', __name__)


@song_list.route("/spotify_list/<list_uri>", methods=["GET"])
def cluster_from_uri(list_uri):
    return json.dumps(song_list_service.get_cluster_by_list_id(list_uri), indent=4)
