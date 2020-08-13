from flask import Flask
from flask_cors import CORS
from clustrify.app.controller.song_list_controller import song_list
import os

app = Flask(__name__)
CORS(app)
app.register_blueprint(song_list)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
