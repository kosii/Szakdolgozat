import sys
import itertools, time
import threading

class Eyecandy(threading.Thread):
    def __init__(self):
        super(Eyecandy, self).__init__()
        self.pattern = '|\-/'
        self.flag = True

    def run(self):
        for i in itertools.cycle(self.pattern):
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.08)
            sys.stdout.write('\r')
            sys.stdout.flush()
            if not self.flag:
                print
                return

    def stop(self):
        self.flag = False
    
