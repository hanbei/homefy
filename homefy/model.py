from whoosh.index import *
from whoosh.fields import Schema, TEXT, ID, NUMERIC

class Artist:
    def __init__(self, title, picture_path = ''):
        self.title = title
        self.picture_path = picture_path
        self.id = title + picture_path

class Album:
    def __init__(self, artist, title, year = '', picture_path = ''):
        self.title = title
        self.artist = artist
        self.year = year
        self.picture_path = picture_path
        self.id = title + year + artist

class Track:
    def __init__(self, artist, album, title):
        self.artist = artist
        self.album = album
        self.title = title
        self.genre = ''
        self.length = 0
        self.track_no = 0
        self.volume_no = 0
        self.id = artist + album + title + str(track_no)

class Type:
    def __init__(self):
        self.ARTIST = 0
        self.ALBUM = 2
        self.TRACK = 4

class Indexer:
	
	
    def __init__(self, index_dir):
		artist_schema = Schema(id=ID(stored=True), 
			title=TEXT(analzer=LowercaseFilter()), 
			_stored_title=STORED, 
			picture_path=ID(stored=True))
		album_schema = Schema(id=ID(stored=True), 
			title=TEXT(analzer=LowercaseFilter()), 
			_stored_title=STORED, 
			picture_path=ID(stored=True),
			year=NUMERIC(stored=True),
			artist=TEXT(stored=True))
		track_schema = Schema(id=ID(stored=True), 
			title=TEXT(analzer=LowercaseFilter()), 
			_stored_title=STORED, 
			artist=TEXT(stored=True),
			album=TEXT(stored=True),
			genre=TEXT(stored=True),
			length=NUMERIC(stored=True),
			track_no=NUMERIC(stored=True),
			volumne_no=TEXT(stored=True))
		
		self.artist_index_writer = index.create_index(index_dir, schema=artist_schema, indexname="artists").writer()
		self.album_index_writer = index.create_index(index_dir, schema=album_schema, indexname="albums").writer()
		self.track_index_writer = index.create_index(index_dir, schema=track_schema, indexname="tracks").writer()

    def add_artist(self, artist):
        self.artist_index_writer.add_document(id=artist.id, title=artist.title, picture_path=artist.picture_path)

    def add_album(self, album):
        self.album_index_writer.add_document(id=album.id, title=album.title, artist=album.artist, 
			picture_path=album.picture_path, year=album.year)

    def add_track(self, track):
        self.track_index_writer.add_document(artist=track.artist, album=track.album,
			title=track.title, genre=title.genre, length=track.length, track_no=track.track_no,
			volume_no=track.volumne_no, id=track.id)

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
    
