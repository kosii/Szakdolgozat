import os, sys, re, mmap, contextlib
import threading, datetime
from pprint import pprint

sys.path.append('.')

import scons
import SCons.Script
import workers
from arguments import parser
from qt_meta import QTFile
from context_managers import filedescriptor, restore_cwd, eyecandy
from utils import Eyecandy
import conf

# C:/Users/kosi/AppData/Local/Amazon/Kindle/application/Kindle.exe 
args = parser.parse_args([r'C:\Users\kosii\AppData\Local\Amazon\Kindle\application\Kindle.exe'])
conf.debug = bool(args.debug)

if args.do_not_regenerate:
	with filedescriptor(args.input_file, os.O_RDONLY) as fd:
		with contextlib.closing(mmap.mmap(fd, length=0, access=mmap.ACCESS_READ)) as mmapped_file:
		    with open('injector/injected.cpp', 'w') as injected_dll_source:
		    	print 'Identifying Qt classes in {input_file} ...'.format(input_file=args.input_file)
		    	with eyecandy():
			    	injected_dll_source.write(QTFile(mmapped_file, n=args.n).render())

if args.do_not_recompile:
	with restore_cwd():
		os.environ['SCONSFLAGS'] = "-C injector -Q -s"
		try:
			print "Compiling injected dll ..."
			with eyecandy():
				SCons.Script.main()
		except SystemExit as e:
			if e.code:
				raise

print "Starting injector ..."
threading.Thread(
	target=workers.launcher, kwargs={'input_file': args.input_file}
).start()
workers.Receiver().start()