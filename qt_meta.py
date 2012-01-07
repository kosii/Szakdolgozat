import struct
import collections
import itertools

def _take(n, iterable):
    return ''.join(itertools.islice(iterable, n))

def string_reader(string_data):
    # ch == 0x00 nem mukodott. utanajarni hogy miert nem
    return ''.join(itertools.takewhile(lambda ch: not (ch == '\x00'), string_data))
"""
ahhoz, hogy faszan hozzaferhessunk az adatokhoz, felul kell irni hogy 
bizonyosokhoz hogy hogyan ferunk hozza. nehanyat at kell szamolni fizikai cimre,
nehanybol a stringet kell kapni, nehanyat 
uint(honeypot::High) <-  ilyen formaban akarunk visszakapni.
"""

def descriptor_metaclass(name, bases, dict):
    if 'struct' in dict and 'fields' in dict:
        dict['struct'] = struct.Struct(dict['struct'])
        bases += (collections.namedtuple(name, dict['fields']), )
    return type(name, bases, dict)

class Descriptor(object):
    __metaclass__ = descriptor_metaclass
    strings=set()

    def __new__(cls, memory_image, string_metadata=None):
        if not hasattr(cls, 'struct') or not hasattr(cls, 'fields'):
            raise NotImplementedError("Define inherited class' struct and fields attributes")
        if cls.strings and not string_metadata:
            raise RuntimeError("TODO!")
        
        instance = super(Descriptor, cls).__new__(cls, *cls.struct.unpack(_take(cls.struct.size, memory_image)))
        return instance._replace(**dict( (s, string_reader(string_metadata[getattr(instance, s):])) for s in cls.strings))

class QMetaClassInfoDescriptor(Descriptor):
    __metaclass__  = descriptor_metaclass
    strings = set(('name', ))
    struct = 'ii'
    fields = 'name, key'

class QMetaMethodDescriptor(Descriptor):
    __metaclass__  = descriptor_metaclass
    strings = set(('signature', 'parameters', 'type', ))
    struct = 'iiiii'
    fields = 'signature, parameters, type, tag, flags'

class QMetaPropertyDescriptor(Descriptor):
    __metaclass__ = descriptor_metaclass
    strings = set(('name', 'type', ))
    struct = 'iiii'
    fields = 'name, type, flags, notify_changed'

class QMetaEnumDescriptor(Descriptor):
    __metaclass__ = descriptor_metaclass
    strings = set(('name'))
    struct = 'iiii'
    fields = 'name, flags, count, data'

class QMetaEnumDataDescriptor(Descriptor):
    __metaclass__ = descriptor_metaclass
    strings = set(('key', ))
    struct = 'ii'
    fields = 'key, value'

class QMetaObjectDataDescriptor(Descriptor):
    __metaclass__ = descriptor_metaclass
    struct = 'iiiiiiiiiiiiii'
    strings = set(('classname', ))
    fields = ('revision, classname, classinfoCount, '
        'classinfos, methodCount, methods, propertyCount, properties, enumCount, enums, '
        'constuctorCount, constructors, flags, signals')

class QMetaObjectDescriptor(Descriptor):
    __metaclass__ = descriptor_metaclass
    fields = 'parent_staticMetaObject, qt_meta_stringdata, qt_meta_data, zero'
    struct = 'iiii'

    def __str__(self):
        return '%s(parent_staticMetaObject=%s, qt_meta_stringdata=%s, qt_meta_data=%s, zero=%s)'\
            %(self.__class__.__name__, hex(self.parent_staticMetaObject), hex(self.qt_meta_stringdata), hex(self.qt_meta_data), hex(self.zero))

class QT(object):
    """
    """
    def __init__(self):
        pass