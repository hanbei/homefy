import unittest
import shutil
import model
from whoosh.index import *

class TestIndexer(unittest.TestCase):
	
	def setUp(self):
		self.index_dir = 'test'
		self.indexer = model.Indexer(self.index_dir)

	def test_add_artist(self):
		self.indexer.add_artist(model.Artist(title=u'TitleBla', picture_path=u"test/tset/test.jpg"))
		self.indexer.add_artist(model.Artist(title=u'TitleBla2', picture_path=u"test/tset/test2.jpg"))
		self.indexer.commit()
		
		with open_dir(self.index_dir, indexname='artists').searcher() as searcher:
			title_terms = list(searcher.lexicon('id'))
			self.assertEqual(2, len(title_terms))
			self.assertEqual(u'da87d6f2506c306b630d8ed22082b15b', title_terms[0])
			self.assertEqual(u'dc9fa80af1d02f5550d13a0629cc38bd', title_terms[1])
			path_terms = list(searcher.lexicon('picture_path'))
			self.assertEqual(2, len(path_terms))
			self.assertEqual(u"test/tset/test.jpg", path_terms[0])
			self.assertEqual(u'test/tset/test2.jpg', path_terms[1])


	def test_add_album(self):
		self.indexer.add_album(model.Album(title=u'TitleBla', picture_path=u"test/tset/test.jpg", artist='ArtistTest', year=2002))
		self.indexer.add_album(model.Album(title=u'TitleBla2', picture_path=u"test/tset/test2.jpg", artist='ArtistTest', year=2002))
		self.indexer.commit()
		
		with open_dir(self.index_dir, indexname='albums').searcher() as searcher:
			title_terms = list(searcher.lexicon('id'))
			self.assertEqual(2, len(title_terms))
			self.assertEqual(u'4a202a41c580496e0591f8a4285c8f84', title_terms[0])
			self.assertEqual(u'cc31deaa190bc25620f9e52b8f47a4fd', title_terms[1])
			
			path_terms = list(searcher.lexicon('picture_path'))
			self.assertEqual(2, len(path_terms))
			self.assertEqual(u"test/tset/test.jpg", path_terms[0])
			self.assertEqual(u'test/tset/test2.jpg', path_terms[1])
			
			artist_terms = list(searcher.lexicon('artist'))
			self.assertEqual(1, len(artist_terms))
			self.assertEqual(u"artisttest", artist_terms[0])
			
			year_terms = list(searcher.lexicon('year'))
			self.assertEqual(1, len(year_terms))
			self.assertEqual(u'2002', year_terms[0])


	def test_add_track(self):
		self.indexer.add_track(model.Track(title=u'TitleBla', artist='ArtistTest', album='TestAlbum', path='path', genre='Metal'))
		self.indexer.add_track(model.Track(title=u'TitleBla2', artist='ArtistTest', album='TestAlbum2', path='path2', genre='Metal'))
		self.indexer.commit()
		
		with open_dir(self.index_dir, indexname='tracks').searcher() as searcher:
			title_terms = list(searcher.lexicon('id'))
			self.assertEqual(2, len(title_terms))
			self.assertEqual(u'c832fc52362cfaac7cf87a517e289c3a', title_terms[0])
			self.assertEqual(u'd6fe1d0be6347b8ef2427fa629c04485', title_terms[1])
			
			album_terms = list(searcher.lexicon('album'))
			self.assertEqual(2, len(album_terms))
			self.assertEqual(u"testalbum", album_terms[0])
			self.assertEqual(u'testalbum2', album_terms[1])
			
			artist_terms = list(searcher.lexicon('artist'))
			self.assertEqual(1, len(artist_terms))
			self.assertEqual(u"artisttest", artist_terms[0])
			
			genre_terms = list(searcher.lexicon('genre'))
			self.assertEqual(1, len(genre_terms))
			self.assertEqual(u'metal', genre_terms[0])


	def tearDown(self):
		shutil.rmtree(self.index_dir)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIndexer)
    unittest.TextTestRunner(verbosity=2).run(suite)
