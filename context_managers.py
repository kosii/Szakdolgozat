import os, contextlib
from utils import Eyecandy

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

@contextlib.contextmanager
def eyecandy():
	e = Eyecandy()
	e.start()
	try:
		yield
	except KeyboardInterrupt as a:
		raise a
	finally:
		e.stop()