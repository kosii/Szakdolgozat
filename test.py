import os, sys, re, mmap, contextlib
from pprint import pprint

import SCons.Script
from qt_meta import QTFile

_0x = hex

#fd = os.open('HoneyPot/HoneyPot.exe', os.O_RDWR)
#fd = os.open(r"C:/Program Files (x86)/Full Tilt Poker.Fr/FullTiltPokerFr.exe", os.O_RDWR)
#fd = os.open(r'C:/Program Files (x86)/Skype/Phone/Skype.exe', os.O_RDONLY

@contextlib.contextmanager
def filedescriptor(filename, flags):
	fd = os.open(filename, flags)
	yield fd
	os.close(fd)

@contextlib.contextmanager
def restore_cwd():
	current_dir = os.getcwd()
	yield
	os.chdir(current_dir)

# fd = os.open(r'C:/Users/kosi/AppData/Local/Amazon/Kindle/application/Kindle.exe', os.O_RDONLY)
with filedescriptor(r'C:/Users/kosi/AppData/Local/Amazon/Kindle/application/Kindle.exe', os.O_RDONLY) as fd:
	with contextlib.closing(mmap.mmap(fd, length=0, access=mmap.ACCESS_READ)) as mmapped_file:
	    with open('injector/injected.cpp', 'w') as injected:
	    	injected.write(QTFile(mmapped_file).render())

with restore_cwd():
	os.environ['SCONSFLAGS'] = "-C injector -Q -s"
	try:
		SCons.Script.main()
	except SystemExit:
		print 'nemnem'
