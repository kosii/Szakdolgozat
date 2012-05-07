import os, sys, re, mmap, contextlib
import argparse, subprocess
import threading, datetime
from pprint import pprint

import SCons.Script
import zmq


from qt_meta import QTFile
from context_managers import filedescriptor, restore_cwd
import conf

# C:/Users/kosi/AppData/Local/Amazon/Kindle/application/Kindle.exe
# 'HoneyPot/HoneyPot.exe'
# "C:/Program Files (x86)/Full Tilt Poker.Fr/FullTiltPokerFr.exe"
# 'C:/Program Files (x86)/Skype/Phone/Skype.exe'

def launcher(input_file):
	with restore_cwd():
		input_file = os.path.abspath(input_file)
		os.chdir('injector')
		subprocess.call('start /WAIT injector.exe "{input_file}"'.format(input_file=input_file), shell=True)

class Receiver(threading.Thread):
	daemon = True
	
	def run(self):
		now = datetime.datetime.now()
		context = zmq.Context()
		socket = context.socket(zmq.PULL)
		socket.bind("tcp://127.0.0.1:5556")
		while True:
			message = socket.recv()
			delta = datetime.datetime.now() - now
			print "{delta} {message}".format(delta=delta, message=message)



parser = argparse.ArgumentParser(description='')
parser.add_argument('-n', type=int, action='store', help='number of class read')
parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='turn on debug messages')
parser.add_argument('-v', '--version', action='version', version='%(prog)s {version}'.format(version=conf.version))
parser.add_argument('-r', action='store_false', dest='do_not_regenerate', help='do not regenerate')
parser.add_argument('-c', action='store_false', dest='do_not_recompile', help='do not recompile')
parser.add_argument('input_file')

args = parser.parse_args(['-d', 'C:/Program Files (x86)/Full Tilt Poker.Fr/FullTiltPokerFr.exe'])
conf.debug = bool(args.debug)

if args.do_not_regenerate:
	with filedescriptor(args.input_file, os.O_RDONLY) as fd:
		with contextlib.closing(mmap.mmap(fd, length=0, access=mmap.ACCESS_READ)) as mmapped_file:
		    with open('injector/injected.cpp', 'w') as injected:
		    	injected.write(QTFile(mmapped_file, n=args.n).render())

if args.do_not_recompile:
	with restore_cwd():
		os.environ['SCONSFLAGS'] = "-C injector -Q -s"
		try:
			SCons.Script.main()
		except SystemExit as e:
			if e.code:
				raise

threading.Thread(
	target=launcher, kwargs={'input_file': args.input_file}
).start()
Receiver().start()