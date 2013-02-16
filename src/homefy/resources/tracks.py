'''
Created on Feb 16, 2013

@author: hanbei
'''
from flask import Blueprint, render_template, request 
import homefy.injector
from flask.helpers import jsonify

resource = Blueprint('tracks', __name__, template_folder='templates')

@resource.route('/tracks/')
def list_tracks():
    all_tracks = homefy.injector.searcher.all_tracks()
    if request_wants_json():
        return jsonify(tracks=[x.to_json() for x in all_tracks])
    return render_template('list_tracks.html', tracks=all_tracks)

@resource.route('/artists/<artist_id>/albums/<album_id>/track/<track_id>/')
def track(artist_id, album_id, track_id):
    track = homefy.injector.searcher.track(track_id)
    if request_wants_json():
        return jsonify(track.to_json())
    return render_template('track.html', track=track)


@resource.route('/artists/<artist_id>/albums/<album_id>/track/<track_id>/play/')
def play_track(artist_id, album_id, track_id):
    track = homefy.injector.searcher.track(track_id)
    homefy.injector.p.load([track.path])
    homefy.injector.p.play()
    return track.path


def request_wants_json():
    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return best == 'application/json' and request.accept_mimetypes[best] > request.accept_mimetypes['text/html']
