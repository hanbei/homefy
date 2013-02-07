__author__ = 'hanbei'
from flask import Flask

from resources import artists

app = Flask(__name__)
app.register_blueprint(artists.resource)

if __name__ == '__main__':
    app.run(debug=True)