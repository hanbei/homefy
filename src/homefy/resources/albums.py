'''
Created on Feb 15, 2013

@author: hanbei
'''
from flask import Blueprint, render_template, request, redirect, url_for 
import homefy.injector
from flask.helpers import jsonify

resource = Blueprint('albums', __name__, template_folder='templates')

@resource.route('/albums/')
def list_albums():
    all_albums = homefy.injector.searcher.all_albums()
    if request_wants_json():
        return jsonify(albums=[x.to_json() for x in all_albums])
    return render_template('list_albums.html', albums=all_albums)

@resource.route('/artists/<artist_id>/albums/')
def albums(artist_id):
    return redirect(url_for('artists.artist', artist_id=artist_id))

@resource.route('/artists/<artist_id>/albums/<album_id>/')
def albums_by_artists(artist_id, album_id):
    return "Albums By Artist" + artist_id + "/" + album_id 


def request_wants_json():
    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return best == 'application/json' and request.accept_mimetypes[best] > request.accept_mimetypes['text/html']
