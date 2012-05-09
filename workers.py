import threading, os, datetime, subprocess

import zmq

from context_managers import restore_cwd

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
