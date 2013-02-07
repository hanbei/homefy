'''
Created on Feb 7, 2013

@author: hanbei
'''
from flask import Blueprint, render_template 
import homefy.injector

resource = Blueprint('artists', __name__, template_folder='templates')

@resource.route('/artists')
def list_artists():
    all_artists= homefy.injector.searcher.all_artists()
    return render_template('list_artists.html', artists=all_artists)
