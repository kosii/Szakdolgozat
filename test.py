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

def info_writer(pe, match_object, mmapped_file):
    metaObjectVirtualAddress = struct.Struct('i').unpack(match_object.group(1))[0]
    print hex(metaObjectVirtualAddress)
    metaObjectPhysicalAddress = pe.vtop(metaObjectVirtualAddress)
    print hex(metaObjectPhysicalAddress)
    meta_obj_descr = QMetaObjectDescriptor(islice(mmapped_file, metaObjectPhysicalAddress, None))
    print 'sdf', meta_obj_descr

    qmetaobject_data = islice(mmapped_file, pe.vtop(meta_obj_descr.qt_meta_data), None)
    qmetaobject_stringdata = mmapped_file[pe.vtop(meta_obj_descr.qt_meta_stringdata):]

    meta_obj_data_descr = QMetaObjectDataDescriptor(qmetaobject_data, qmetaobject_stringdata)
    print meta_obj_data_descr
    for i in xrange(meta_obj_data_descr.classinfoCount):
        print QMetaClassInfoDescriptor(qmetaobject_data, qmetaobject_stringdata)
    for i in xrange(meta_obj_data_descr.methodCount):
        print QMetaMethodDescriptor(qmetaobject_data, qmetaobject_stringdata)
    for i in xrange(meta_obj_data_descr.propertyCount):
        print QMetaPropertyDescriptor(qmetaobject_data, qmetaobject_stringdata)
    for i in xrange(meta_obj_data_descr.propertyCount):
        print QMetaPropertyChangedDescriptor(qmetaobject_data)
    
    enum_count = 0
    for i in xrange(meta_obj_data_descr.enumCount):
        enum_descriptor = QMetaEnumDescriptor(qmetaobject_data, qmetaobject_stringdata)
        enum_count += enum_descriptor.count
        print enum_descriptor
    for i in xrange(enum_count):
        print QMetaEnumDataDescriptor(qmetaobject_data, qmetaobject_stringdata)
    print "found metaObject() function at %s psysical address, at %s virtual address, with metaObject at %s virtual address and %s physical address"%\
      (_0x(match_object.start()), _0x(pe.ptov(match_object.start())), _0x(metaObjectVirtualAddress), _0x(metaObjectPhysicalAddress))
    
    print "class name: %s" % ''.join(string_reader(qmetaobject_stringdata))

#fd = os.open('HoneyPot/HoneyPot.exe', os.O_RDWR)
fd = os.open('ftp.exe', os.O_RDWR)
with contextlib.closing(mmap.mmap(fd, length=0)) as mmapped_file:
    qtfile = QTFile(mmapped_file)
    for qtclass in qtfile.classes:
        print qtclass.name