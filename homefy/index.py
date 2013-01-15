import os.path
from whoosh.index import *
from whoosh.fields import Schema, TEXT, ID, NUMERIC
import tagger

frame_to_schema = {
'TBPM':'bpm',
'TPE2':'artist',
'TALB':'album',
'TIT2':'track_name',
'TRCK':'track_number',
'TYER':'year',
'TCON':'genre',
'TLEN':'length'
}

index_writer = None

def schema():
	return Schema(id=ID(stored=True), 
				artist=TEXT(stored=True), 
				album=TEXT(stored=True), 
				track_name=TEXT(stored=True), 
				track_number=NUMERIC(stored=True), 
				year=NUMERIC(stored=True),
				length=NUMERIC(stored=True),
				path=ID(stored=True),
				genre=TEXT(stored=True)
			)

def create_index(index_dir):
	global index_writer
	if not os.path.exists(index_dir):
		os.mkdir(index_dir)    			
    		  
	index = create_in(index_dir, schema())
	index_writer = index.writer()

def close_index():
	index_writer.commit()
	

def add_track(track, path):
	print path
	for frame in track.frames:
		print frame.fid, frame.strings
		
		
create_index("../index")
for dirpath, dirnames, filenames in os.walk("/home/hanbei/Music/Air"):
    # use os.walk to iterate someDir's contents recursively. No
    # need to implement recursion yourself if stdlib does it for you
    for f in filenames:
        ext = os.path.splitext(f)[1]
        if ext.lower() == '.mp3':
			abspath = os.path.join(dirpath, f)
			tag = tagger.ID3v2(abspath)
			add_track(tag, abspath)
close_index()
