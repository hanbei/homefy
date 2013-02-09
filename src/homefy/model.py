import os.path
from whoosh import analysis, query
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID, NUMERIC
from whoosh.qparser import QueryParser
import hashlib

UTF8 = 'utf-8'

class Artist:
	def __init__(self, title, picture_path=''):
		self.title = title.encode(UTF8)
		if picture_path:
			self.picture_path = picture_path.encode(UTF8)
		else:
			self.picture_path = ''
		hash_id = hashlib.md5()
		hash_id.update(self.title)
		hash_id.update(self.picture_path)
		self.id = hash_id.hexdigest().encode(UTF8)


class Album:
	def __init__(self, artist, title, year=0, picture_path=''):
		self.title = title.encode(UTF8)
		self.artist = artist.encode(UTF8)
		self.year = year
		if picture_path:
			self.picture_path = picture_path.encode(UTF8)
		else:
			self.picture_path = ''
		hash_id = hashlib.md5()
		hash_id.update(self.title)
		hash_id.update(str(year).encode(UTF8))
		hash_id.update(self.artist)
		self.id = hash_id.hexdigest().encode(UTF8)

class Track:
	def __init__(self, artist, album, title, path, genre='', track_no=0, length=0.0, volume_no=0):
		self.artist = artist.encode(UTF8)
		self.album = album.encode(UTF8)
		self.title = title.encode(UTF8)
		self.genre = genre.encode(UTF8)
		self.length = length
		self.track_no = track_no
		self.volume_no = volume_no
		self.path = path.encode(UTF8)
		self.id = hashlib.md5(self.path).hexdigest().encode(UTF8)

	def toString(self):
		s = ''
		s = s + str(self.track_no)
		s = s + "-"
		s = s + self.title
		return s

class Type:
	ARTIST = 'ARTIST'
	ALBUM = 'ALBUM'
	TRACK = 'TRACK'


class Indexer:
	def __init__(self, index_dir):
		title_analyzer = analysis.SpaceSeparatedTokenizer() | analysis.LowercaseFilter() | analysis.NgramFilter(2)
		artist_schema = Schema(id=ID(stored=True), title=TEXT(analyzer=title_analyzer, stored=True),
			picture_path=ID(stored=True))
		album_schema = Schema(id=ID(stored=True), title=TEXT(analyzer=title_analyzer, stored=True),
			picture_path=ID(stored=True),
			year=ID(stored=True), artist=TEXT(stored=True))
		track_schema = Schema(id=ID(stored=True), title=TEXT(analyzer=title_analyzer, stored=True),
			artist=TEXT(stored=True),
			album=TEXT(stored=True), genre=TEXT(stored=True), length=NUMERIC(stored=True),
			track_no=NUMERIC(stored=True), volume_no=NUMERIC(stored=True), path=ID(stored=True))

		if not os.path.exists(index_dir):
			os.mkdir(index_dir)

		self.artist_index_writer = create_in(index_dir, schema=artist_schema, indexname="artists").writer()
		self.album_index_writer = create_in(index_dir, schema=album_schema, indexname="albums").writer()
		self.track_index_writer = create_in(index_dir, schema=track_schema, indexname="tracks").writer()

	def add_artist(self, artist):
		self.artist_index_writer.add_document(id=unicode(artist.id, UTF8), title=unicode(artist.title, UTF8),
			picture_path=unicode(artist.picture_path, UTF8))

	def add_album(self, album):
		self.album_index_writer.add_document(id=unicode(album.id, UTF8), title=unicode(album.title, UTF8),
			artist=unicode(album.artist, UTF8), picture_path=unicode(album.picture_path, UTF8),
			year=unicode(str(album.year)))

	def add_track(self, track):
		self.track_index_writer.add_document(artist=unicode(track.artist, UTF8), album=unicode(track.album, UTF8),
			title=unicode(track.title, UTF8), genre=unicode(track.genre, UTF8), length=track.length,
			track_no=track.track_no, volume_no=track.volume_no, id=unicode(track.id, UTF8), path=unicode(track.path, UTF8))

	def commit(self):
		self.artist_index_writer.commit()
		self.album_index_writer.commit()
		self.track_index_writer.commit()


class Searcher:
	def __init__(self, index_dir):
		self.artist_searcher = open_dir(index_dir, indexname='artists').searcher()
		self.album_searcher = open_dir(index_dir, indexname='albums').searcher()
		self.track_searcher = open_dir(index_dir, indexname='tracks').searcher()

	def artist(self, artist_id):
		document = self.artist_searcher.document(id=unicode(artist_id))
		if document != None:
			return self._artist_from_document(document)
		return None

	def album(self, album_id):
		document = self.album_searcher.document(id=unicode(album_id))
		if document != None:
			return self._album_from_document(document)
		return None

	def track(self, track_id):
		document = self.track_searcher.document(id=unicode(track_id))
		if document != None:
			return self._track_from_document(document)
		return None

	def search(self, query, page=-1, page_size=10):
		search_results = list()
		qp_artist = QueryParser('title', self.artist_searcher.schema)
		query = qp_artist.parse(unicode(query))
		if page < 1:
			artist_hits = self.artist_searcher.search(query, limit=None, sortedby='title')
		else:
			artist_hits = self.artist_searcher.search(query, page, page_size, sortedby='title')
		for hit in artist_hits:
			search_results.append(SearchResult(self._artist_from_document(hit), Type.ARTIST))

		qp_album = QueryParser('title', self.album_searcher.schema)
		query = qp_album.parse(unicode(query))
		if page < 1:
			album_hits = self.album_searcher.search(query, limit=None, sortedby='title')
		else:
			album_hits = self.album_searcher.search(query, page, page_size, sortedby='title')
		for hit in album_hits:
			search_results.append(SearchResult(self._album_from_document(hit), Type.ALBUM))

		qp_track = QueryParser('title', self.track_searcher.schema)
		query = qp_track.parse(unicode(query))
		if page < 1:
			track_hits = self.track_searcher.search(query, limit=None, sortedby='title')
		else:
			track_hits = self.track_searcher.search(query, page, page_size, sortedby='title')
		for hit in track_hits:
			search_results.append(SearchResult(self._track_from_document(hit), Type.TRACK))

		return search_results


	def album_by_artist(self, artist_id, page=-1, page_size=10):
		artist = self.artist(artist_id)
		if artist == None:
			return None

		q = query.Term('artist', unicode(artist.title.lower()))
		if page < 1:
			documents = self.album_searcher.search(q, limit=None, sortedby='year')
		else:
			documents = self.album_searcher.search_page(q, page, page_size, sortedby='year')
		result_list = list()
		for doc in documents:
			result_list.append(self._album_from_document(doc))
		return result_list

	def tracks_by_album(self, album_id, page=-1, page_size=10):
		album = self.album(album_id)
		if album == None:
			return None

		q = query.Term('album', unicode(album.title.lower()))
		if page < 1:
			documents = self.track_searcher.search(q, limit=None, sortedby='track_no')
		else:
			documents = self.track_searcher.search_page(q, page, page_size, sortedby='track_no')
		result_list = list()
		for doc in documents:
			result_list.append(self._track_from_document(doc))
		return result_list

	def all_artists(self, page=-1, page_size=10):
		if page > 0:
			artists = self.artist_searcher.search_page(query.Every(), page, page_size, sortedby='title')
		else:
			artists = self.artist_searcher.search(query.Every(), sortedby='title', limit=None)

		result_list = list()
		print "---- Unsorted -----"
		for artist in artists:
			new_artist = self._artist_from_document(artist)
			result_list.append(new_artist)
			print new_artist.title
			
		result_list.sort(key=lambda artist: artist.title.lower())
		print "---- Sorted -----"
		for artist in result_list:
			print artist.title
			
		return result_list

	def close(self):
		self.artist_searcher.close()
		self.album_searcher.close()
		self.track_searcher.close()

	def _album_from_document(self, document):
		return Album(title=document['title'], picture_path=document['picture_path'], artist=document['artist'],
			year=int(document['year']))

	def _track_from_document(self, document):
		return Track(title=document['title'], album=document['album'], artist=document['artist'], path=document['path'],
			track_no=int(document['track_no']), length=int(document['length']), volume_no=int(document['volume_no']),
			genre=document['genre'])

	def _artist_from_document(self, document):
		return Artist(title=document['title'], picture_path=document['picture_path'])


class SearchResult:
	def __init__(self, data, type):
		self.data = data
		self.type = type

	def __repr__(self):
		return self.data.title + " " + self.type

	def __str__(self):
		return self.data.title + " " + self.type

