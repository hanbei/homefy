import popen2
import threading
import time

class Status:
	def __init__(self, song_length=0, elapsed_time=0.0, remaining_time=0.0):
		self.song_length = song_length
		self.elapsed_time = elapsed_time
		self.remaining_time = remaining_time
		
	def copy(self):
		s = Status(self.song_length, self.elapsed_time, self.remaining_time)
		return s
	
class Player(threading.Thread):
	
	def __init__(self, ):
		threading.Thread.__init__(self)		
		self.lock = threading.Lock()
		self.from_player, self.to_player = popen2.popen2("mpg123 -Rq", 0)
		self.playing = False
		self.paused = False
		self.current_status = Status()
		self.start()
		
	def load(self, songs):
		self.playlist = songs
		self.current_song = 0
		print self.playlist
		
	def play(self):		
		if(self.playing):
			self.stop()
		print self.playlist[self.current_song]
		self._start_play()
			
	def stop(self):
		self._send('s')
		self.playing = False
		
	def pause(self):
		self._send('p')
		self.paused = not self.paused
		
	def next(self):
		"""Play the next song in the playlist."""
		if(self.playing):
			self.stop()
		self.current_song += 1
		if(self.current_song >= len(self.playlist)):
			self.stop()
		else:
			self._start_play()
		
	def prev(self):
		"""Play the song that was played before. 
		   
		The current song will be stopped and the song that has been played
		previously will be played. 
		"""
		if(self.playing):
			self.stop()
		self.current_song -= 1
		if(self.current_song < 0):
			self.stop()
		else:
			self._start_play()
		
	def close(self):
		"""Close the player and terminate the mpg123 subprocess. 
	
		After close() was called this instance can not be reused.
		"""
		if(self.playing):
			self.stop()
			
		self._running = False
		self._send('q')
		
		self.lock.acquire()
		buf = self.from_player.read()
		self.lock.release()
		self.from_player.close()
		self.to_player.close
	
	def status(self):
		self.lock.acquire()
		s = self.current_status.copy()
		self.lock.release()
		return s
		
	def _start_play(self):
		self._send('l', self.playlist[self.current_song])		
		self.playing = True
		
	def _send(self, command, data=''):
		if(data == ''):
			self.to_player.write("%s\n" % (command))
		else:
			self.to_player.write("%s %s\n" % (command, data))

	def run(self):
		self._running = True
		while self._running:
			self.lock.acquire()
			line = self.from_player.readline()
			self._parse_line(line)
			self.lock.release()
			
	def _parse_line(self, line):
		splitted_line = line.split(' ')
		if splitted_line[0] == '@S':
			self.current_status.song_length = int(splitted_line[11])
		elif splitted_line[0] == '@P':
			if splitted_line[1].strip() == '0':
				self.playing = False
				self.next()
		elif splitted_line[0] == '@I':
			pass
		elif splitted_line[0] == '@F':
			self.current_status.elapsed_time = float(splitted_line[3])
			self.current_status.remaining_time = float(splitted_line[4])
		else:
			pass

class StatusPrinter(threading.Thread):
	def __init__(self, player):
		threading.Thread.__init__(self)		
		self.player = player
		self.running = True
		
	def run(self):
		while self.running:
			status = self.player.status()
			print "%f/%d" % (status.elapsed_time, status.song_length)
			time.sleep(1)

if __name__ == "__main__":
    import sys


    p = Player()
    sp = StatusPrinter(p)
    
    p.load(sys.argv[1:])
    p.play()
    #time.sleep(0.5)
    #p.stop()
    #time.sleep(10)
    #p.next()
    #time.sleep(10)
    #p.next()
    #time.sleep(1)
    sp.start()
    while p.playing:
		time.sleep(1)
		
    p.close()
    
    
    
    
