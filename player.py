import popen2
import threading
import time

class Status(threading.Thread):
    def __init__(self, player):
        threading.Thread.__init__(self)
        self.setDaemon(1)
        self.player = player

    def run(self):
        while 1:
            try:
                print self.player.time, self.player.frame
            except AttributeError:
                pass
            time.sleep(1)


class Player(threading.Thread):
	
	def __init__(self, ):
		threading.Thread.__init__(self)		
		self.from_player, self.to_player = popen2.popen2("mpg123 -Rq", 0)
		self.playing = False
		self.paused = False
		self.start()
		
	def load(self, songs):
		self.playlist = songs
		self.current_song = 0
		print self.playlist
		
	def play(self):		
		if(self.playing):
			self.stop()
		self.playing = True
		print self.playlist[self.current_song]
		self._send('l', self.playlist[self.current_song])
			
	def stop(self):
		self._send('s')
		self.playing = False
		
	def pause(self):
		self._send('p')
		self.paused = not self.paused
		
	def next(self):
		if(self.playing):
			self.stop()
		self.current_song += 1
		self._send('l', self.playlist[self.current_song])		
		
	def prev(self):
		if(self.playing):
			self.stop()
		self.current_song -= 1
		self._send('l', self.playlist[self.current_song])		
		
	def close(self):
		if(self.playing):
			self.stop()
			
		self.running = False
		self._send('q')
		buf = self.from_player.read()
		self.from_player.close()
		self.to_player.close

		
	def _send(self, command, data=''):
		if(data == ''):
			self.to_player.write("%s\n" % (command))
		else:
			self.to_player.write("%s %s\n" % (command, data))

	def run(self):
		self.running = True
		while self.running:
			print self.from_player.readline()

if __name__ == "__main__":
    import sys

    p = Player()
    p.load(sys.argv[1:])
    p.play()
    time.sleep(10)
    p.stop()
    p.close()
    
    
    
    
