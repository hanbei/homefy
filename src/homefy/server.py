__author__ = 'hanbei'
from flask import Flask

from resources import artists
from resources import albums

app = Flask(__name__)
app.register_blueprint(artists.resource)
app.register_blueprint(albums.resource)

if __name__ == '__main__':
    app.run(debug=True)