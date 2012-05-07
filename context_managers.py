import os, contextlib

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