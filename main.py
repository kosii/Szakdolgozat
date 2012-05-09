import os, sys, re, mmap, contextlib
import threading, datetime
from pprint import pprint

import SCons.Script

import workers
from arguments import parser
from qt_meta import QTFile
from context_managers import filedescriptor, restore_cwd
import conf

# C:/Users/kosi/AppData/Local/Amazon/Kindle/application/Kindle.exe
# 'HoneyPot/HoneyPot.exe'
# "C:/Program Files (x86)/Full Tilt Poker.Fr/FullTiltPokerFr.exe"
# 'C:/Program Files (x86)/Skype/Phone/Skype.exe'


args = parser.parse_args(['HoneyPot/HoneyPot.exe'])
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
	target=workers.launcher, kwargs={'input_file': args.input_file}
).start()
workers.Receiver().start()