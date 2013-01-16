import os
from whoosh.index import *
from whoosh.fields import Schema, TEXT, ID, NUMERIC, STORED
from whoosh.analysis import LowercaseFilter

class Artist:
    def __init__(self, title, picture_path = ''):
        self.title = unicode(title)
        self.picture_path = unicode(picture_path)
        self.id = unicode(title + picture_path)

class Album:
    def __init__(self, artist, title, year = '', picture_path = ''):
        self.title = unicode(title)
        self.artist = unicode(artist)
        self.year = year
        self.picture_path = unicode(picture_path)
        self.id = unicode(title + str(year) + artist)

class Track:
    def __init__(self, artist, album, title, genre='', track_no=0, length=0, volumne_no=0):
        self.artist = unicode(artist)
        self.album = unicode(album)
        self.title = unicode(title)
        self.genre = unicode(genre)
        self.length = length
        self.track_no = track_no
        self.volume_no = volumne_no
        self.id = unicode(artist + album + title + str(track_no))

class Type:
    def __init__(self):
        self.ARTIST = 0
        self.ALBUM = 2
        self.TRACK = 4

class Indexer:
	
    def __init__(self, index_dir):
		artist_schema = Schema(id=ID(stored=True), 
			title=TEXT(stored=True), 
			picture_path=ID(stored=True))
		album_schema = Schema(id=ID(stored=True), 
			title=TEXT(stored=True), 
			picture_path=ID(stored=True),
			year=ID(stored=True),
			artist=TEXT(stored=True))
		track_schema = Schema(id=ID(stored=True), 
			title=TEXT(stored=True), 
			artist=TEXT(stored=True),
			album=TEXT(stored=True),
			genre=TEXT(stored=True),
			length=NUMERIC(stored=True),
			track_no=NUMERIC(stored=True),
			volume_no=NUMERIC(stored=True))

		if not os.path.exists(index_dir):
			os.mkdir(index_dir)    			

		self.artist_index_writer = create_in(index_dir, schema=artist_schema, indexname="artists").writer()
		self.album_index_writer = create_in(index_dir, schema=album_schema, indexname="albums").writer()
		self.track_index_writer = create_in(index_dir, schema=track_schema, indexname="tracks").writer()

    def add_artist(self, artist):
		self.artist_index_writer.add_document(id=artist.id, title=artist.title, picture_path=artist.picture_path)

    def add_album(self, album):
        self.album_index_writer.add_document(id=album.id, title=album.title, artist=album.artist, 
			picture_path=album.picture_path, year=unicode(str(album.year)))

    def add_track(self, track):
        self.track_index_writer.add_document(artist=track.artist, album=track.album,
			title=track.title, genre=track.genre, length=track.length, track_no=track.track_no,
			volume_no=track.volume_no, id=track.id)

    def commit(self):
        self.artist_index_writer.commit()
        self.album_index_writer.commit()
        self.track_index_writer.commit()

class Searcher:
    def __init__(self, index_dir):
        pass

    def artist(self, id):
        pass

    def album(self, id):
        pass

    def search(self, query, page = -1, page_size = 10):
        pass

    def album_by_artist(self, artist_id, page = -1, page_size = 10):
        pass

    def tracks_by_album(self, album, page = -1, page_size = 10):
        pass

    def artists(self, page = -1, page_size = 10):
        pass

class SearchResult:
    def __init__(self, type, title, id):
        self.type = type
        self.title = title
        self.id = id
    
