import os
import hashlib
from whoosh import query
from whoosh.index import *
from whoosh.fields import Schema, TEXT, ID, NUMERIC

class Artist:
    def __init__(self, title, picture_path=''):
        self.title = unicode(title)
        self.picture_path = unicode(picture_path)
        hash = hashlib.md5()
        hash.update(self.title)
        hash.update(self.picture_path)
        self.id = unicode(hash.hexdigest())


class Album:
    def __init__(self, artist, title, year='', picture_path=''):
        self.title = unicode(title)
        self.artist = unicode(artist)
        self.year = year
        self.picture_path = unicode(picture_path)
        hash = hashlib.md5()
        hash.update(self.title)
        hash.update(str(year))
        hash.update(self.artist)
        self.id = unicode(hash.hexdigest())


class Track:
    def __init__(self, artist, album, title, path, genre='', track_no=0, length=0, volume_no=0):
        self.artist = unicode(artist)
        self.album = unicode(album)
        self.title = unicode(title)
        self.genre = unicode(genre)
        self.length = length
        self.track_no = track_no
        self.volume_no = volume_no
        self.path = unicode(path)
        self.id = unicode(hashlib.md5(path).hexdigest())

class Type:
    def __init__(self):
        self.ARTIST = 0
        self.ALBUM = 2
        self.TRACK = 4


class Indexer:
    def __init__(self, index_dir):
        artist_schema = Schema(id=ID(stored=True), title=TEXT(stored=True), picture_path=ID(stored=True))
        album_schema = Schema(id=ID(stored=True), title=TEXT(stored=True), picture_path=ID(stored=True),
            year=ID(stored=True), artist=TEXT(stored=True))
        track_schema = Schema(id=ID(stored=True), title=TEXT(stored=True), artist=TEXT(stored=True),
            album=TEXT(stored=True), genre=TEXT(stored=True), length=NUMERIC(stored=True),
            track_no=NUMERIC(stored=True), volume_no=NUMERIC(stored=True), path=ID(stored=True))

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
            volume_no=track.volume_no, id=track.id, path=track.path)

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
        pass

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

    def artists(self, page=-1, page_size=10):
        if page > 0:
            artists = self.artist_searcher.search_page(query.Every(), page, page_size, sortedby='title')
        else:
            artists = self.artist_searcher.search(query.Every(), sortedby='title', limit=None)

        result_list = list()
        for artist in artists:
            result_list.append(self._artist_from_document(artist))
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
    def __init__(self, type, title, id):
        self.type = type
        self.title = title
        self.id = id

