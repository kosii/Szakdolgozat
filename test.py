import os
import sys
import re
import mmap
import contextlib
from pprint import pprint

import pefile

def get_sectionname_by_physical_address(pe, phys_addr):

    for section in pe.sections:
        if section.PointerToRawData <= phys_addr and phys_addr < section.PointerToRawData + section.SizeOfRawData:
            return section.Name
    return None

def get_sectionname_by_virtual_address(pe, virtual_address):

    for section in pe.sections:
        if pe.OPTIONAL_HEADER.ImageBase + section.VirtualAddress <= virtual_address and virtual_address < pe.OPTIONAL_HEADER.ImageBase + section.VirtualAddress + section.SizeOfRawData:
            return section.Name
    return None 

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
    pe = pefile.PE(data=mmapped_file)
    pprint(pe)
    print hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint)
    print hex(pe.OPTIONAL_HEADER.ImageBase)
    print pe.sections['.text']
    for section in pe.sections:
        pprint(section)
        print section.Name, section.VirtualAddress, hex(section.VirtualAddress), type(section.VirtualAddress), section.SizeOfRawData
    #print len(mmapped_file)
    #print len(compiled_regexp.findall(mmapped_file))
    #print "asda:", len(re.findall(bytes([0x8B, 0x41, 0x04, 0x8b, 0x40, 0x18, 0x85, 0xc0, 0x75,0x05, 0xb8, ord('('), ord('.'), ord('.'), ord('.'), ord('.'), ord(')'), 0xc3]), mmapped_file))
    for i, matchObject in enumerate(compiled_regexp.finditer(mmapped_file)):
        pass
        #print [hex(ord(b)) for b in matchObject.group(1)]
        print i, get_sectionname_by_physical_address(pe, matchObject.start()), hex(matchObject.start()), get_sectionname_by_virtual_address(pe, little_endian_string_to_number(matchObject.group(1))), hex(little_endian_string_to_number(matchObject.group(1)))