import struct
import collections
import itertools
import re

import pystache

import conf
def _take(n, iterable):
    return ''.join(itertools.islice(iterable, n))

def string_reader(string_data):
    # ch == 0x00 nem mukodott. utanajarni hogy miert nem
    return ''.join(itertools.takewhile(lambda ch: not (ch == '\x00'), string_data))

class DescriptorMetaclass(type):
    def __new__(cls, name, bases, dict):
        if 'struct' in dict and 'fields' in dict:
            dict['struct'] = struct.Struct(dict['struct'])
            bases += (collections.namedtuple(name, dict['fields']), )
        return super(DescriptorMetaclass, cls).__new__(cls, name, bases, dict)

# akartam valami fasza valtoztatast csinalni! ;D
# csak elfelejtettem :(
# de valszeg a descriptorokkal vagy a __slot__ tal kapcsolatos volt. vagy lehet hogy teljesen massal
# janem! abs-szel kell kikenyszeriteni az attributumok felulirasanak a kenyszeret!


class Descriptor(object):
    __metaclass__ = DescriptorMetaclass
    strings=set()

    def __new__(cls, memory_image, string_metadata=None):
        if not hasattr(cls, 'struct') or not hasattr(cls, 'fields'):
            raise NotImplementedError("Define inherited class' struct and fields attributes")
        if cls.strings and not string_metadata:
            raise RuntimeError("TODO!")
        
        instance = super(Descriptor, cls).__new__(cls, *cls.struct.unpack(_take(cls.struct.size, memory_image)))
        return instance._replace(**dict( (s, string_reader(string_metadata[getattr(instance, s):])) for s in cls.strings))

class QMetaClassInfoDescriptor(Descriptor):
    strings = set(('name', ))
    struct = 'ii'
    fields = 'name, key'

class QMetaMethodDescriptor(Descriptor):
    strings = set(('signature', 'parameters', 'type', ))
    struct = 'iiiii'
    fields = 'signature, parameters, type, tag, flags'

class QMetaPropertyDescriptor(Descriptor):
    strings = set(('name', 'type', ))
    struct = 'iii'
    fields = 'name, type, flags'
    
    def read_data(self, memory_image):
        # we had to check whether we have a notification changed method
        return QMetaPropertyChangedDescriptor(memory_image) if True else None
    
class QMetaPropertyChangedDescriptor(Descriptor):
    struct = 'i'
    fields = 'notifyChanged'
    
class QMetaEnumDescriptor(Descriptor):
    strings = set(('name', ))
    struct = 'iiii'
    fields = 'name, flags, count, data'

class QMetaEnumDataDescriptor(Descriptor):
    strings = set(('key', ))
    struct = 'ii'
    fields = 'key, value'

class QMetaObjectDataDescriptor(Descriptor):
    struct = 'iiiiiiiiiiiiii'
    strings = set(('classname', ))
    fields = ('revision, classname, classinfoCount, '
        'classinfos, methodCount, methods, propertyCount, '
        'properties, enumCount, enums, '
        'constuctorCount, constructors, flags, signals')

class QMetaObjectDescriptor(Descriptor):
    fields = 'parent_staticMetaObject, qt_meta_stringdata, qt_meta_data, zero'
    struct = 'iiii'

    def __str__(self):
        return '{0}(parent_staticMetaObject={1}, qt_meta_stringdata={2}, '
        'qt_meta_data={3}, zero={4})'.format(
            self.__class__.__name__, hex(self.parent_staticMetaObject), 
            hex(self.qt_meta_stringdata), hex(self.qt_meta_data), 
            hex(self.zero)
        )

class QTClass(object):
    @property
    def name(self):
        return self.meta_obj_data_descr.classname
    
    @property
    def safe_name(self):
        return self.name.replace(':', '_')

    @property
    def metacall_address_name(self):
        return "{name}_metacall_address".format(name=self.safe_name)

    @property
    def metacall_hook_name(self):
        return "{name}_metacall_address_hook".format(name=self.safe_name)

    @property
    def metaobject_function(self):
        return self._metaobject_function
    
    @property
    def metacall_function_address(self):
        return getattr(self, '_metacall_function_address', None)
    
    @property
    def metacall_super_function_address(self):
        return getattr(self, '_metacall_super_function_address', None)

    def _calculate_metacall_function_address(self):
        pattern = struct.pack('i', self.metaobject_function)
        escaped_pattern = re.escape(pattern)
        section = self.pe.GetSectionnameSection('.rdata')
        metacall_virtual_addresses = set([
            struct.unpack('i', section.get_data()[match_object.start()+8:match_object.start()+12])[0]
            for match_object in re.finditer(escaped_pattern, section.get_data()) 
            if not match_object.start()%4
        ])
        if len(metacall_virtual_addresses) > 1:
            raise ValueError("more than one possible {name}::qt_metacall function address candidate in .rdata section".format(name=self.name))
        elif not metacall_virtual_addresses:
            raise ValueError("{name}::qt_metacall function address not found in .rdata section".format(name=self.name))
        self._metacall_function_address = hex(metacall_virtual_addresses.pop())

    def _calculate_metacall_super_function_address(self):
        import distorm3 as distorm
        metacall_function_address = int(self.metacall_function_address, base=16)
        metacall_function_physical_address = self.pe.vtop(metacall_function_address)
        super_calls = (
            (mnemonic, hex_string)
            for offset, size, mnemonic, hex_string 
            in distorm.DecodeGenerator(
                metacall_function_address, 
                self.pe.__data__[
                    metacall_function_physical_address:metacall_function_physical_address+0x40
                ], distorm.Decode32Bits)
            if mnemonic.startswith('CALL') or mnemonic.startswith('JMP')
        )
        mnemonic, hex_string = super_calls.next()
        if mnemonic.startswith('JMP'):
            self.do = False
            return
        pattern = re.compile('\[?(0x[0-9A-Fa-f]+)\]?')
        match_object = pattern.search(mnemonic)
        self._metacall_super_function_address = match_object.group(1)
        self.indirection = match_object.group(0).startswith('[')

    def __init__(self, mmapped_file, match_object, pe):
        self.pe = pe
        self.do = True
        self.indirection = True

        self._metaobject_function = pe.ptov(match_object.start())
        self._calculate_metacall_function_address()
        self._calculate_metacall_super_function_address()

        qmetaObject_virtual_address = struct.Struct('i').unpack(match_object.group(1))[0]
        qmetaobject_physical_address = pe.vtop(qmetaObject_virtual_address)
        self.qmetaobject_descriptor = QMetaObjectDescriptor(mmapped_file[qmetaobject_physical_address:])

        qt_meta_stringdata = mmapped_file[pe.vtop(self.qmetaobject_descriptor.qt_meta_stringdata):]
        qt_meta_data = itertools.islice(mmapped_file, pe.vtop(self.qmetaobject_descriptor.qt_meta_data), None)
        
        self.meta_obj_data_descr = QMetaObjectDataDescriptor(qt_meta_data, qt_meta_stringdata)
        
        self.class_infos = []
        for i in xrange(self.meta_obj_data_descr.classinfoCount):
            self.class_infos.append(
                QMetaClassInfoDescriptor(
                    qt_meta_data, qt_meta_stringdata
                )
            )
        self.methods = []
        for i in xrange(self.meta_obj_data_descr.methodCount):
            mmd = QMetaMethodDescriptor(
                qt_meta_data, qt_meta_stringdata
            )
            mmd.id = i
            self.methods.append(mmd)
        self.properties = []
        for i in xrange(self.meta_obj_data_descr.propertyCount):
            self.properties.append(
                QMetaPropertyDescriptor(
                    qt_meta_data, qt_meta_stringdata
                )
            )
        self.property_notifications = []
        for i in xrange(self.meta_obj_data_descr.propertyCount):
            self.property_notifications.append(
                QMetaPropertyChangedDescriptor(
                    qt_meta_data
                )
            )
        self.enums = []
        for i in xrange(self.meta_obj_data_descr.enumCount):
            self.enums.append(
                QMetaEnumDescriptor(
                    qt_meta_data, qt_meta_stringdata
                )
            )
        self.enums_data = {}
        for enum_descriptor in self.enums:
            for i in xrange(enum_descriptor.count):
                self.enums_data.setdefault(enum_descriptor.name, []).append(
                    QMetaEnumDataDescriptor(
                        qt_meta_data, qt_meta_stringdata
                    )
                )
    
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

class QTFile(pystache.View):
    template_name = 'qtfile'

    def __init__(self, mmapped_file, n=None):
        super(QTFile, self).__init__()
        import pefile_mod
        self.pe = pefile_mod.PE(data=mmapped_file)
        self.classes = []
        for i, match_object in enumerate(compiled_regexp.finditer(mmapped_file)):
            if i == n: break
            qt_class = QTClass(mmapped_file, match_object, self.pe)
            if conf.debug:
                print "QT class found with:\n"\
                    "\tname: {name}\n"\
                    "\tmetaObject function@0x{metaObject_function}\n"\
                    "\tqt_metacall function@{qt_metacall_function}\n"\
                    "\tsuper's qt_metacall_function@{metacall_super_function_address}".format(
                        name=qt_class.name, 
                        metaObject_function=hex(qt_class.metaobject_function),
                        qt_metacall_function=qt_class.metacall_function_address,
                        metacall_super_function_address=qt_class.metacall_super_function_address
                    )
            self.classes.append(qt_class)
    
