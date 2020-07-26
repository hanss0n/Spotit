from flask import Blueprint

auth = Blueprint('auth', __name__)


# TODO: fix this garb
@auth.route("/auth", methods=['GET'])
def kek():
    return "you are authenticated"
