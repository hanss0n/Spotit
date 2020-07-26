from flask import Flask
from app.controller.song_list_controller import song_list

app = Flask(__name__)
app.register_blueprint(song_list)

if __name__ == '__main__':
    app.run()
