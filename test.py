import os
import sys
import re
import mmap
import contextlib

import pefile

def little_endian_string_to_number(address):
    return reduce(lambda x, y: x*256 + y, reversed(map(ord, address)))

def regexify(bytepattern):
    for b in bytepattern:
        if b is not None:
            yield b
        else:
            for r in '(....)':
                yield ord(r)
    return

pattern = [0x8B, 0x41, 0x04, 0x8b, 0x40, 0x18, 0x85, 0xc0, 0x75, 0x05, 0xb8, None, 0xc3]
regexp_pattern =  ''.join(map(chr, regexify(pattern)))
#regexp_pattern = ''.join(map(chr, [0x8B, 0x41, 0x04, 0x8b, 0x40, 0x18, 0x85, 0xc0, 0x75, 0x05, 0xb8]))
#print regexp_pattern
#print list(regexify(pattern))
#print len(list(regexify(pattern)))
#regex_pattern =  bytes(list(regexify(pattern)))
#print list(regex_pattern)
#print regex_pattern
#print bytes([0x8B, 0x41, 0x04, 0x8b, 0x40, 0x18, 0x85, 0xc0, 0x75, 0x05, 0xb8, ord('('), ord('.'), ord('.'), ord('.'), ord('.'), ord(')'), 0xc3])
#regex_pattern = map(chr, regex_pattern)
compiled_regexp = re.compile(regexp_pattern, flags=re.DOTALL)
#print compiled_regexp

fd = os.open('ftp.exe', os.O_RDWR)
with contextlib.closing(mmap.mmap(fd, length=0)) as mmapped_file:
    print len(mmapped_file)
    print len(compiled_regexp.findall(mmapped_file))
    #print "asda:", len(re.findall(bytes([0x8B, 0x41, 0x04, 0x8b, 0x40, 0x18, 0x85, 0xc0, 0x75,0x05, 0xb8, ord('('), ord('.'), ord('.'), ord('.'), ord('.'), ord(')'), 0xc3]), mmapped_file))
    for i, matchObject in enumerate(compiled_regexp.finditer(mmapped_file)):
        print i, hex(matchObject.start()), hex(little_endian_string_to_number(matchObject.group(1)))