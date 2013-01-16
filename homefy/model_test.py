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
			title_terms = list(searcher.lexicon('title'))
			self.assertEqual(2, len(title_terms))
			self.assertEqual(u'titlebla', title_terms[0])
			self.assertEqual(u'titlebla2', title_terms[1])
			path_terms = list(searcher.lexicon('picture_path'))
			self.assertEqual(2, len(path_terms))
			self.assertEqual(u"test/tset/test.jpg", path_terms[0])
			self.assertEqual(u'test/tset/test2.jpg', path_terms[1])


	def test_add_album(self):
		self.indexer.add_artist(model.Artist(title=u'TitleBla', picture_path=u"test/tset/test.jpg"))
		self.indexer.add_artist(model.Artist(title=u'TitleBla2', picture_path=u"test/tset/test2.jpg"))
		self.indexer.commit()
		
		with open_dir(self.index_dir, indexname='artists').searcher() as searcher:
			title_terms = list(searcher.lexicon('title'))
			self.assertEqual(2, len(title_terms))
			self.assertEqual(u'titlebla', title_terms[0])
			self.assertEqual(u'titlebla2', title_terms[1])
			path_terms = list(searcher.lexicon('picture_path'))
			self.assertEqual(2, len(path_terms))
			self.assertEqual(u"test/tset/test.jpg", path_terms[0])
			self.assertEqual(u'test/tset/test2.jpg', path_terms[1])


	def tearDown(self):
		shutil.rmtree(self.index_dir)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIndexer)
    unittest.TextTestRunner(verbosity=2).run(suite)
