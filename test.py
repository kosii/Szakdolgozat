import os
import sys
import re
import mmap
import contextlib
from pprint import pprint
from itertools import takewhile
import itertools
import operator
import pefile
import struct

_0x = hex

def get_sectionordinal_by_physical_address(pe, phys_addr):
    for i, section in enumerate(pe.sections):
        if section.PointerToRawData <= phys_addr and phys_addr < section.PointerToRawData + section.SizeOfRawData:
            return i
    raise ValueError("Invalid PhyisicalAddress")

def get_sectionname_by_physical_address(pe, phys_addr):
    ordinal = get_sectionordinal_by_physical_address(pe, phys_addr)
    return pe.sections[ordinal].Name

def get_sectionordinal_by_virtual_address(pe, virtual_addr):
    for i, section in enumerate(pe.sections):
        if pe.OPTIONAL_HEADER.ImageBase + section.VirtualAddress <= virtual_addr and virtual_addr < pe.OPTIONAL_HEADER.ImageBase + section.VirtualAddress + section.SizeOfRawData:
            return i
    raise ValueError("Invalid VirtualAddress")

def get_sectionname_by_virtual_address(pe, virtual_addr):
    ordinal = get_sectionordinal_by_virtual_address(pe, virtual_addr)
    return pe.sections[ordinal].Name

def virtual_address_to_physical_address(pe, virt_addr):
    sectionordinal = get_sectionordinal_by_virtual_address(pe, virt_addr)
    section = pe.sections[sectionordinal]
    return virt_addr-pe.OPTIONAL_HEADER.ImageBase - section.VirtualAddress + section.PointerToRawData 

def physical_address_to_virtual_address(pe, phys_addr):
    sectionordinal = get_sectionordinal_by_physical_address(pe, phys_addr)
    section = pe.sections[sectionordinal]
    return phys_addr - section.PointerToRawData + pe.OPTIONAL_HEADER.ImageBase + section.VirtualAddress

def little_endian_string_to_number(address):
    return reduce(lambda x, y: x*256 + y, reversed(map(ord, address)))

def integer(iterator, byte=4):

    def magnitude(base):
        i = 1
        while True:
            yield i
            i *= base
    
    return sum(map(operator.mul, itertools.islice(iterator, 0, byte), magnitude(256)))

def string_reader(address):
    # ch == 0x00 nem mukodott. utanajarni hogy miert nem
    return takewhile(lambda ch: not (ch == '\x00'), address)

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
compiled_regexp = re.compile(regexp_pattern, flags=re.DOTALL)

def info_writer(pe, match_object, mmaped_file):
    metaObjectVirtualAddress = little_endian_string_to_number(match_object.group(1))
    metaObjectPhysicalAddress = virtual_address_to_physical_address(pe, metaObjectVirtualAddress)
    print "found metaObject() function at %s psysical address, at %s virtual address, with metaObject at %s virtual address and %s physical address"%\
      (_0x(match_object.start()), _0x(physical_address_to_virtual_address(pe, match_object.start())), _0x(metaObjectVirtualAddress), _0x(metaObjectPhysicalAddress))
    someParentVirtualAddress = struct.unpack("<i",mmaped_file[metaObjectPhysicalAddress:][:4])[0]
    textInfoVirtualAddress = struct.unpack("<i", mmaped_file[metaObjectPhysicalAddress+4:][:4])[0]
    textInfoPhysicalAddress = virtual_address_to_physical_address(pe, textInfoVirtualAddress)
    metaInfoVirtualAddress = little_endian_string_to_number(mmaped_file[metaObjectPhysicalAddress+8:][:4])
    metaInfoPhysicalAddress = virtual_address_to_physical_address(pe, metaInfoVirtualAddress)
    print "class name: %s"%''.join(string_reader(mmaped_file[textInfoPhysicalAddress:]))
    #print len(list(string_reader(mmaped_file[textInfoPhysicalAddress:100])))
    #print ''.join(string_reader(mmaped_file[textInfoPhysicalAddress:100]))
    print "\t%s %s %s"%\
      (_0x(someParentVirtualAddress),_0x(textInfoVirtualAddress), _0x(metaInfoVirtualAddress))


fd = os.open('ftp.exe', os.O_RDWR)
with contextlib.closing(mmap.mmap(fd, length=0)) as mmapped_file:
    pe = pefile.PE(data=mmapped_file)
    pprint(pe)
    print hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint)
    print hex(pe.OPTIONAL_HEADER.ImageBase)
    for section in pe.sections:
        pprint(section)
        print section.Name, section.VirtualAddress, hex(section.VirtualAddress), type(section.VirtualAddress), section.SizeOfRawData
    for i, matchObject in enumerate(compiled_regexp.finditer(mmapped_file)):
        if i > 10:
            break
        info_writer(pe, matchObject, mmapped_file)
        #print i, get_sectionname_by_physical_address(pe, matchObject.start()), hex(matchObject.start()), get_sectionname_by_virtual_address(pe, little_endian_string_to_number(matchObject.group(1))), hex(little_endian_string_to_number(matchObject.group(1)))
        #print hex(physical_address_to_virtual_address(pe, matchObject.start()))
    