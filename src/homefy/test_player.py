import unittest
from player import Player

class TestPlayer(unittest.TestCase):


    def setUp(self):
        self.player = Player()

    def tearDown(self):
        self.player.close()

    def test_singleton(self):
        player2 = Player()
        self.assertEquals(id(self.player),id(player2))
        player2.close()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPlayer)
    unittest.TextTestRunner(verbosity=2).run(suite)
