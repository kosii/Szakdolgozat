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

def get_sectionordinal_by_physical_address(pe, phys_addr):
    for i, section in enumerate(pe.sections):
        if section.PointerToRawData <= phys_addr <  section.PointerToRawData + section.SizeOfRawData:
            return i
    raise ValueError("Invalid PhyisicalAddress")

def get_sectionname_by_physical_address(pe, phys_addr):
    ordinal = get_sectionordinal_by_physical_address(pe, phys_addr)
    return pe.sections[ordinal].Name

def get_sectionordinal_by_virtual_address(pe, virtual_addr):
    for i, section in enumerate(pe.sections):
        if pe.OPTIONAL_HEADER.ImageBase + section.VirtualAddress <= virtual_addr < pe.OPTIONAL_HEADER.ImageBase + section.VirtualAddress + section.SizeOfRawData:
            return i
    raise ValueError("Invalid VirtualAddress")

def get_sectionname_by_virtual_address(pe, virtual_addr):
    ordinal = get_sectionordinal_by_virtual_address(pe, virtual_addr)
    return pe.sections[ordinal].Name

def vtop(pe, virt_addr):
    if not virt_addr:
        return 0
    sectionordinal = get_sectionordinal_by_virtual_address(pe, virt_addr)
    section = pe.sections[sectionordinal]
    return virt_addr - pe.OPTIONAL_HEADER.ImageBase - section.VirtualAddress + section.PointerToRawData 

def ptov(pe, phys_addr):
    if not phys_addr:
        return 0
    sectionordinal = get_sectionordinal_by_physical_address(pe, phys_addr)
    section = pe.sections[sectionordinal]
    return phys_addr - section.PointerToRawData + pe.OPTIONAL_HEADER.ImageBase + section.VirtualAddress

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

from collections import namedtuple
QMetaObject = namedtuple('QMetaObject', 'parent_staticMetaObject qt_meta_stringdata qt_meta_data zero')
QMetaObjectReader = struct.Struct("iiii")

QMetaObjectData = namedtuple('QMetaObjectData', 'revision classname classinfoCount \
  classinfos methodCount methods propertyCount properties enumCount enums \
  constuctorCount constructors flags signals'
)
QMetaObjectDataReader = struct.Struct("iiiiiiiiiiiiii")

def info_writer(pe, match_object, mmapped_file):
    metaObjectVirtualAddress = struct.Struct('i').unpack(match_object.group(1))[0]
    print hex(metaObjectVirtualAddress)
    metaObjectPhysicalAddress = vtop(pe, metaObjectVirtualAddress)
    print hex(metaObjectPhysicalAddress)
    meta_obj_descr = QMetaObjectDescriptor(islice(mmapped_file, metaObjectPhysicalAddress, None))
    print 'sdf', meta_obj_descr
    qmetaobject_data = islice(mmapped_file, pe.vtop(meta_obj_descr.qt_meta_data), None)
    meta_obj_data_descr = QMetaObjectDataDescriptor(qmetaobject_data)
    print meta_obj_data_descr
    metaObjectMemoryImage = mmapped_file[metaObjectPhysicalAddress:][:4*4]
    parsedMetaObject = QMetaObject._make(QMetaObjectReader.unpack(metaObjectMemoryImage))
    parsedMetaObjectPhysAddress = QMetaObject._make(map(lambda virtualaddress: vtop(pe, virtualaddress), parsedMetaObject))
    print "found metaObject() function at %s psysical address, at %s virtual address, with metaObject at %s virtual address and %s physical address"%\
      (_0x(match_object.start()), _0x(ptov(pe, match_object.start())), _0x(metaObjectVirtualAddress), _0x(metaObjectPhysicalAddress))
    
    print "class name: %s" % ''.join(string_reader(mmapped_file[parsedMetaObjectPhysAddress.qt_meta_stringdata:]))
    metaObjectDataMemoryImage = mmapped_file[parsedMetaObjectPhysAddress.qt_meta_data:][:14*4]
    parsedQMetaObjectData = QMetaObjectData._make(QMetaObjectDataReader.unpack(metaObjectDataMemoryImage))
    for i in xrange(parsedQMetaObjectData.classinfoCount):
        pass
    #print len(list(string_reader(mmapped_file[textInfoPhysicalAddress:100])))
    #print ''.join(string_reader(mmapped_file[textInfoPhysicalAddress:100]))
    #print "\t%s %s %s"%\
    #  (_0x(someParentVirtualAddress),_0x(textInfoVirtualAddress), _0x(metaInfoVirtualAddress))

#fd = os.open('HoneyPot/HoneyPot.exe', os.O_RDWR)
fd = os.open('ftp.exe', os.O_RDWR)
with contextlib.closing(mmap.mmap(fd, length=0)) as mmapped_file:
    pe = pefile_mod.PE(data=mmapped_file)
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
        #print hex(ptov(pe, matchObject.start()))
