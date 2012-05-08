import argparse

import conf

parser = argparse.ArgumentParser(description='')
parser.add_argument('-n', type=int, action='store', help='number of class read')
parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='turn on debug messages')
parser.add_argument('-v', '--version', action='version', version='%(prog)s {version}'.format(version=conf.version))
parser.add_argument('-r', action='store_false', dest='do_not_regenerate', help='do not reread the input file')
parser.add_argument('-c', action='store_false', dest='do_not_recompile', help='do not recompile, only launch existing binaries')
parser.add_argument('input_file')
