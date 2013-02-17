'''
Created on Feb 16, 2013

@author: hanbei
'''
from flask import Blueprint, jsonify 
from homefy.injector import p as player

resource = Blueprint('player', __name__, template_folder='templates')

@resource.route('/player/stop/')
def stop():
    player.stop()
    return "stopped"

@resource.route('/player/next/')
def next():
    player.next()
    return "next"

@resource.route('/player/prev/')
def prev():
    player.prev()
    return "prev"

@resource.route('/player/pause/')
def pause():
    player.pause()
    return "pause"

@resource.route('/player/playlist/')
def playlist():
    s = "<ul>"
    for t in player.playlist:
        s += "<li>"
        s += t
        s += "</li>"
    s += "</ul>"  
    return s

@resource.route('/player/status/')
def status():
    status = player.status()
    return jsonify(status.to_json())


@resource.route('/player/kill/')
def kill():
    player.close()
    return "killed"