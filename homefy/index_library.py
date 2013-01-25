import os
import model
import tagger

def picture_path(pic_path, pic_name):
    abs_path = os.path.abspath(pic_path)
    pic = os.path.join(abs_path, pic_name + u'.jpg')
    if os.path.exists(pic):
        return pic

    pic = os.path.join(os.path.abspath(pic_path), pic_name + u'.png')
    if os.path.exists(pic):
        return pic

    pic = os.path.join(os.path.abspath(pic_path), pic_name + u'jpg')
    if os.path.exists(pic):
        return pic

    return None


def index_artist(artist_dir):
    artist_name = os.path.split(artist_dir)[1]
    if os.path.isfile(artist_dir):
        print 'file: ' + + artist_name
    else:
        pic_path = picture_path(artist_dir, u'artist')
        if pic_path:
            print pic_path
        indexer.add_artist(model.Artist(artist_name, pic_path))
    album_dirs = os.listdir(artist_dir)
    for album_dir in album_dirs:
        if os.path.isdir(os.path.join(artist_dir, album_dir)):
            index_albums(artist_name, os.path.join(artist_dir, album_dir))


def index_albums(artist_name, album_path):
    album_name = os.path.split(album_path)[1]
    name_split = album_name.split('-', 1)
    year = 0000
    if len(name_split) == 2:
        year_string = name_split[0].strip()
        try:
            year = int(year_string[1:len(year_string) - 1])
        except ValueError:
            print "Error indexing: " + album_path

    if len(name_split) == 2:
        title = name_split[1].strip()
    else:
        title = name_split[0].strip()
    album_art_path = picture_path(album_path, u'folder')
    indexer.add_album(model.Album(artist_name, title, year, album_art_path))
    for track_file in os.listdir(album_path):
        track = os.path.join(album_path, track_file)
        if os.path.isfile(track) and os.path.splitext(track)[1] == '.mp3':
            index_track(artist_name, title, track)


frame_to_schema = {
    'TBPM': 'bpm',
    'TRCK': 'track_number',
    'TLEN': 'length'
}

def index_track(artist_name, album_name, track_path):
    tag = tagger.ID3v2(track_path)
    track = model.Track(artist_name, album_name, '', track_path)
    for frame in tag.frames:
        frame_join = "".join(frame.strings)
        if frame.fid == 'TIT2':
            track.title = frame_join
        elif frame.fid == 'TCON':
            track.genre = frame_join
        elif frame.fid == 'TRCK':
            try:
                track.track_no = int(frame.strings[0])
            except:
                print '\'' + frame.strings[0] + '\'\t' + track_path
        elif frame.fid == 'TLEN':
            track.length = float(frame_join.replace(':', '.'))
        else:
            pass
            #print ""
    #print str(track)
    #indexer.add_track(track)

indexer = model.Indexer('index')

music_dir = u"/home/hanbei/Music"
artist_dirs = os.listdir(music_dir)
for artist_dir in artist_dirs:
    index_artist(os.path.join(music_dir, artist_dir))

indexer.commit()
