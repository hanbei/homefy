import os
import homefy.model as model
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
    artist = None
    if os.path.isfile(artist_dir):
        print 'file: ' + + artist_name
    else:
        pic_path = picture_path(artist_dir, u'artist')
        artist = model.Artist(artist_name, pic_path)
        indexer.add_artist(artist)
    album_dirs = os.listdir(artist_dir)
    for album_dir in album_dirs:
        if os.path.isdir(os.path.join(artist_dir, album_dir)):
            index_albums(artist, os.path.join(artist_dir, album_dir))


def index_albums(artist, album_path):
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
    album = model.Album(artist.id, artist.title, title, year, album_art_path)
    indexer.add_album(album)
    for track_file in os.listdir(album_path):
        track = os.path.join(album_path, track_file)
        if os.path.isfile(track) and os.path.splitext(track)[1] == u'.mp3':
            index_track(artist, album, track)


def index_track(artist, album, track_path):
    try:
        tag = tagger.ID3v2(track_path)
    except (UnicodeDecodeError, UnicodeEncodeError) as e:
        print track_path
        print e
        print
        return

    track = model.Track(artist.title, album.title, '', track_path)
    for frame in tag.frames:
        if len(frame.strings) > 0:
            frame_join = frame.strings[0]#.encode('utf-8')
        else:
            frame_join = u''
        if frame.fid == u'TIT2':
            track.title = frame_join
        elif frame.fid == u'TCON':
            track.genre = frame_join
        elif frame.fid == u'TRCK':
            try:
                track_name = os.path.split(track_path)[1]
                name_split = track_name.split('-', 1)
                if len(name_split) <= 1:
                    name_split = track_name.split('.', 1)
                track.track_no = int(name_split[0])
            except:
                print "Error track no: " + track_path.encode('utf-8')
                print frame_join
                print
                #print '\'' + frame.strings[0] + '\'\t'
        elif frame.fid == u'TLEN':
            #track.length = float(frame_join.replace(':', '.'))
            pass
        else:
            pass
            #print ""
            #print track.toString()
            #indexer.add_track(track)

indexer = model.Indexer(u'index')

music_dir = u"/home/hanbei/Music"
artist_dirs = os.listdir(music_dir)
for artist_dir in artist_dirs:
    index_artist(os.path.join(music_dir, artist_dir))

indexer.commit()
