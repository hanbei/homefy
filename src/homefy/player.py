import popen2
import threading
import time

class Status:
	def __init__(self, song_length=0, elapsed_time=0.0, remaining_time=0.0):
		self.song_length = song_length
		self.elapsed_time = elapsed_time
		self.remaining_time = remaining_time
		self.number_playing = -1

	def copy(self):
		s = Status(self.song_length, self.elapsed_time, self.remaining_time)
		s.number_playing = self.number_playing
		return s
	
	def to_json(self):
		return {"current_song":self.number_playing, "length":self.song_length, "elapsed":self.elapsed_time, "remaining":self.remaining_time}

#===============================================================================
# def singleton(cls):
#	instances = {}
#	def getinstance():
#		if cls not in instances:
#			instances[cls] = cls()
#		return instances[cls]
#	return getinstance
# 
# @singleton
#===============================================================================
class Player(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)		
		self.status_lock = threading.RLock()
		self.file_lock = threading.Lock()
		self.from_player, self.to_player = popen2.popen2("mpg123 -Rq", 0)
		self.playing = False
		self.paused = False
		self.closed = False
		self._current_status = Status()
		self._last_command = ""
		self.start()

	def load(self, songs):
		self.playlist = songs
		self.current_song = 0

	def play(self):
		self.status_lock.acquire()			
		if(self.playing):
			self.stop()
		self._last_command = "play"
		self._start_play()
		self.status_lock.release()


	def stop(self):
		self.status_lock.acquire()
		if self.playing:
			self._send('s')
		self.playing = False
		self._last_command = "stop"
		self.status_lock.release()


	def pause(self):
		self.status_lock.acquire()
		self._send('p')
		self.paused = not self.paused
		self._last_command = "pause"
		self.status_lock.release()

	def next(self):
		"""Play the next song in the playlist."""
		self.status_lock.acquire()
		self.current_song += 1
		self._last_command = "next"
		self._start_play()
		self.status_lock.release()


	def prev(self):
		"""Play the song that was played before. 

		The current song will be stopped and the song that has been played
		previously will be played. 
		"""
		self.status_lock.acquire()
		self.current_song -= 1
		self._last_command = "prev"
		self._start_play()
		self.status_lock.release()

	def close(self):
		"""Close the player and terminate the mpg123 subprocess. 

		After close() was called this instance can not be reused.
		"""
		if(self.playing):
			self.stop()

		self._running = False

		self.file_lock.acquire()
		if not self.closed:
			self._send('q')
			self.from_player.read()
			self.from_player.close()
			self.to_player.close
			self.closed = True
		self.file_lock.release()

	def status(self):
		self.status_lock.acquire()
		s = self._current_status.copy()
		self.status_lock.release()
		return s

	def _start_play(self):
		print "Playing " + str(self.current_song)
		self._send('l', self.playlist[self.current_song])		
		self.playing = True
		self.status_lock.acquire()
		self._current_status.number_playing = self.current_song
		self.status_lock.release()


	def _send(self, command, data=''):
		if(data == ''):
			self.to_player.write("%s\n" % (command))
		else:
			self.to_player.write("%s %s\n" % (command, data))

	def run(self):
		self._running = True
		line = ""
		while self._running:
			self.file_lock.acquire()
			if not self.from_player.closed:
				line = self.from_player.readline()
			self.file_lock.release()
			self.status_lock.acquire()
			self._parse_line(line)
			self.status_lock.release()

	def _parse_line(self, line):
		if not line:
			return
		splitted_line = line.split(' ')
		if splitted_line[0] == '@S':
			print line
			self._current_status.song_length = int(splitted_line[11])
		elif splitted_line[0] == '@P':
			print line
			if splitted_line[1].strip() == '0':
				if self.playing and self._last_command != 'stop':
					self.playing = False
					self.next()
		elif splitted_line[0] == '@I':
			pass
		elif splitted_line[0] == '@F':
			self._current_status.elapsed_time = float(splitted_line[3])
			self._current_status.remaining_time = float(splitted_line[4])
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
			print "%f/%d %s" % (status.elapsed_time, status.song_length, str(self.player.playing))
			print p._last_command
			time.sleep(0.5)

if __name__ == "__main__":
	p = Player()
	sp = StatusPrinter(p)
	

	p.load(['/home/hanbei/test2.mp3','/home/hanbei/test.mp3','/home/hanbei/test3.mp3'])
	p.play()
	
	print p._last_command
	print p.status().number_playing
	time.sleep(2)
	p.next()
	print p._last_command
	print p.status().number_playing
	time.sleep(2)
	p.next()
	print "Last Command: " + p._last_command
	print p.status().number_playing
	time.sleep(2)
	p.stop()
	
#	sp.start()
#	while p.playing:
#		time.sleep(1)
#	sp.running = False
	
	p.close()




