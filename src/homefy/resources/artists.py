'''
Created on Feb 7, 2013

@author: hanbei
'''
from flask import Blueprint, render_template, request 
import homefy.injector
from flask.helpers import jsonify

resource = Blueprint('artists', __name__, template_folder='templates')

@resource.route('/artists')
def list_artists():
    all_artists= homefy.injector.searcher.all_artists()
    if request_wants_json():
        return jsonify(artists=[x.to_json() for x in all_artists])
    return render_template('list_artists.html', artists=all_artists)


def request_wants_json():
    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return best == 'application/json' and request.accept_mimetypes[best] > request.accept_mimetypes['text/html']
