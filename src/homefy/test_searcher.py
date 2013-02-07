import model
import unittest
import hashlib
import shutil

class TestSearcher(unittest.TestCase):
    def setUp(self):
        self.index_dir = 'test'
        indexer = model.Indexer(self.index_dir)
        indexer.add_artist(model.Artist(title=u'Z', picture_path=u"z.jpg"))
        indexer.add_artist(model.Artist(title=u'C', picture_path=u"test2.jpg"))
        indexer.add_artist(model.Artist(title=u'ArtistTest', picture_path=u"test/tset/test.jpg"))
        indexer.add_album(
            model.Album(title=u'TestAlbum', picture_path=u"test/tset/test.jpg", artist=u'ArtistTest', year=2002))
        indexer.add_album(
            model.Album(title=u'TestAlbum2', picture_path=u"test/tset/test2.jpg", artist=u'ArtistTest', year=2004))
        indexer.add_track(
            model.Track(title=u'TitleBla', artist=u'ArtistTest', album=u'TestAlbum', path='path1', track_no=2))
        indexer.add_track(
            model.Track(title=u'TitleBla2', artist=u'ArtistTest', album=u'TestAlbum', path='path2', track_no=3))
        indexer.add_track(
            model.Track(title=u'TitleBla3', artist=u'ArtistTest', album=u'TestAlbum', path='path3', track_no=4))
        indexer.commit()
        self.searcher = model.Searcher(self.index_dir)

    def tearDown(self):
        self.searcher.close()
        shutil.rmtree(self.index_dir)

    def test_get_artist(self):
        artist_hash = hashlib.md5(u'ArtistTest' + u"test/tset/test.jpg").hexdigest()
        artist = self.searcher.artist(artist_hash)
        self.assertEquals(artist_hash, artist.id)
        self.assertEquals(u'ArtistTest', artist.title)
        self.assertEquals(u"test/tset/test.jpg", artist.picture_path)

    def test_get_album(self):
        album_hash = hashlib.md5(u'TestAlbum' + unicode(str(2002)) + u'ArtistTest').hexdigest()
        album = self.searcher.album(album_hash)
        self.assertEquals(album_hash, album.id)
        self.assertEquals(u'TestAlbum', album.title)
        self.assertEquals(u"test/tset/test.jpg", album.picture_path)
        self.assertEquals(2002, album.year)
        self.assertEquals('ArtistTest', album.artist)

    def test_get_track(self):
        track_hash = hashlib.md5(u'path1').hexdigest()
        track = self.searcher.track(track_hash)
        self.assertEquals(track_hash, track.id)
        self.assertEquals(u'TitleBla', track.title)
        self.assertEquals(u"TestAlbum", track.album)
        self.assertEquals(2, track.track_no)
        self.assertEquals('ArtistTest', track.artist)

    def test_album_by_artist(self):
        artist_hash = hashlib.md5(u'ArtistTest' + u"test/tset/test.jpg").hexdigest()
        albums = self.searcher.album_by_artist(artist_hash)
        self.assertEquals(2, len(albums))

        self.assertEquals(u'TestAlbum', albums[0].title)
        self.assertEquals(u"test/tset/test.jpg", albums[0].picture_path)
        self.assertEquals(2002, albums[0].year)
        self.assertEquals('ArtistTest', albums[0].artist)

        self.assertEquals(u'TestAlbum2', albums[1].title)
        self.assertEquals(u"test/tset/test2.jpg", albums[1].picture_path)
        self.assertEquals(2004, albums[1].year)
        self.assertEquals('ArtistTest', albums[1].artist)

    def test_tracks_by_albums(self):
        album_hash = hashlib.md5(u'TestAlbum' + unicode(str(2002)) + u'ArtistTest').hexdigest()
        tracks = self.searcher.tracks_by_album(album_hash)
        self.assertEquals(3, len(tracks))

        self.assertEquals(u'TitleBla', tracks[0].title)
        self.assertEquals(u"ArtistTest", tracks[0].artist)
        self.assertEquals(u'TestAlbum', tracks[0].album)
        self.assertEquals(2, tracks[0].track_no)

        self.assertEquals(u'TitleBla2', tracks[1].title)
        self.assertEquals(u"ArtistTest", tracks[1].artist)
        self.assertEquals(u'TestAlbum', tracks[1].album)
        self.assertEquals(3, tracks[1].track_no)

        self.assertEquals(u'TitleBla3', tracks[2].title)
        self.assertEquals(u"ArtistTest", tracks[2].artist)
        self.assertEquals(u'TestAlbum', tracks[2].album)
        self.assertEquals(4, tracks[2].track_no)

    def test_artists(self):
        all_artists = self.searcher.all_artists()
        self.assertEquals(3, len(all_artists))

        self.assertEquals(u'ArtistTest', all_artists[0].title)
        self.assertEquals(u"test/tset/test.jpg", all_artists[0].picture_path)

        self.assertEquals(u'C', all_artists[2].title)
        self.assertEquals(u"test2.jpg", all_artists[2].picture_path)

        self.assertEquals(u'Z', all_artists[1].title)
        self.assertEquals(u"z.jpg", all_artists[1].picture_path)

    def test_search(self):
        hits = self.searcher.search('test')
        self.assertEquals(3, len(hits))
        self.assertEquals(model.Type.ARTIST, hits[0].type)
        self.assertEquals(u'ArtistTest', hits[0].data.title)
        self.assertEquals(model.Type.ALBUM, hits[1].type)
        self.assertEquals(u'TestAlbum', hits[1].data.title)
        self.assertEquals(model.Type.ALBUM, hits[2].type)
        self.assertEquals(u'TestAlbum2', hits[2].data.title)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSearcher)
    unittest.TextTestRunner(verbosity=2).run(suite)

