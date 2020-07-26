from flask import Blueprint

song_list = Blueprint('song_list', __name__)


@song_list.route("/", methods=["GET"])
def test():
    return "this is a test"
