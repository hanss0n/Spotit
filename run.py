from flask import Flask
from app.controller.song_list_controller import song_list
from app.controller.auth_controller import auth

app = Flask(__name__)
app.register_blueprint(song_list)
app.register_blueprint(auth)

if __name__ == '__main__':
    app.run()
