'''
Created on Feb 7, 2013

@author: hanbei
'''
import model
import player

searcher = model.Searcher(index_dir=u'../../index')
p = player.Player()

def renew_player():
    p.close()
    p = player.Player()


