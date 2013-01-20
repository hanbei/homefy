import os
import model

frame_to_schema = {
    'TBPM': 'bpm',
    'TPE2': 'artist',
    'TALB': 'album',
    'TIT2': 'track_name',
    'TRCK': 'track_number',
    'TYER': 'year',
    'TCON': 'genre',
    'TLEN': 'length'
}

def picture_path(pic_path, pic_name):
    abs_path = os.path.abspath(pic_path)
    pic = os.path.join(abs_path, pic_name+'.jpg')
    if os.path.exists(pic):
        return pic

    pic = os.path.join(os.path.abspath(pic_path), pic_name+'.png')
    if os.path.exists(pic):
        return pic

    pic = os.path.join(os.path.abspath(pic_path), pic_name+'jpg')
    if os.path.exists(pic):
        return pic

    return None


def index_artist(artist_dir):
    artist_name = os.path.split(artist_dir)[1]
    if os.path.isfile(artist_dir):
        print 'file: ' + + artist_name
    else:
        pic_path = picture_path(artist_dir, 'artist')
        if pic_path:
            print pic_path
        indexer.add_artist(model.Artist(artist_name, pic_path))
    album_dirs = os.listdir(artist_dir)
    for album_dir in album_dirs:
        if os.path.isdir(os.path.join(artist_dir, album_dir)):
            index_albums(os.path.join(artist_dir, album_dir))


def index_albums(album_path):
    print album_path

indexer = model.Indexer('index')

music_dir = "/home/hanbei/Music"
artist_dirs = os.listdir(music_dir)
for artist_dir in artist_dirs:
    index_artist(os.path.join(music_dir, artist_dir))

indexer.commit()
