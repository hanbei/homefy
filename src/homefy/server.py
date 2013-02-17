__author__ = 'hanbei'
from flask import Flask

from resources import artists
from resources import albums
from resources import tracks
from resources import player

app = Flask(__name__)
app.register_blueprint(artists.resource)
app.register_blueprint(albums.resource)
app.register_blueprint(tracks.resource)
app.register_blueprint(player.resource)


if __name__ == '__main__':
    app.run(debug=True)