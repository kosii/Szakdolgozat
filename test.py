import os
import sys
import re
import mmap
import contextlib
from pprint import pprint

from itertools import takewhile, islice
import itertools
import operator
import pefile_mod
import struct

from qt_meta import *

_0x = hex

#fd = os.open('HoneyPot/HoneyPot.exe', os.O_RDWR)
#fd = os.open(r"C:/Program Files (x86)/Full Tilt Poker.Fr/FullTiltPokerFr.exe", os.O_RDWR)
#fd = os.open(r'C:/Program Files (x86)/Skype/Phone/Skype.exe', os.O_RDONLY)
fd = os.open(r'C:/Users/kosi/AppData/Local/Amazon/Kindle/application/Kindle.exe', os.O_RDONLY)
with contextlib.closing(mmap.mmap(fd, length=0, access=mmap.ACCESS_READ)) as mmapped_file:
    qtfile = QTFile(mmapped_file)
    # for qtclass in qtfile.classes:
    #     print qtclass.name, hex(qtclass.metacall_function_address)
    with open('injector/injected.cpp', 'w') as injected:
    	injected.write(qtfile.render())