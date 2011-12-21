import struct
import collections
import itertools

def _take(n, iterable):
    return ''.join(itertools.islice(iterable, n))

def descriptor_metaclass(name, bases, dict):
    if 'struct' in dict and 'fields':
        dict['struct'] = struct.Struct(dict['struct'])
        bases += (collections.namedtuple(name, dict['fields']), )
    return type(name, bases, dict)

class Descriptor(object):

    __metaclass__ = descriptor_metaclass

    def __new__(cls, memory_image):
        if not hasattr(cls, 'struct') or not hasattr(cls, 'fields'):
            raise NotImplementedError("Define inherited class' struct and fields attributes")
        return super(Descriptor, cls).__new__(cls, *cls.struct.unpack(_take(cls.struct.size, memory_image)))
        #return cls(*cls.struct.unpack(_take(cls.struct.size, memory_image)))
        #return cls.namedtuple_factory()(*cls.struct.unpack(_take(cls.struct.size, memory_image)))
    
class QMetaClassInfoDescriptor(Descriptor):
    __metaclass__  = descriptor_metaclass
    struct = 'ii'
    fields = 'name, key'

print QMetaClassInfoDescriptor('\00\01\00\00\01\00\01\00')

class QMetaMethodDescriptor(Descriptor):
    __metaclass__  = descriptor_metaclass
    struct = 'iiiii'
    fields = 'signature, parameters, type, tag, flags'

class QMetaPropertyDescriptor(Descriptor):
    __metaclass__ = descriptor_metaclass
    struct = 'iiii'
    fields = 'name, type, flags, notify_changed'

class QMetaEnumDescriptor(Descriptor):
    __metaclass__ = descriptor_metaclass
    struct = 'iiii'
    fields = 'name, flags, count, data'

class QMetaEnumDataDescriptor(Descriptor):
    __metaclass__ = descriptor_metaclass
    struct = 'iiii'
    fields = 'key, value'

class QMetaObjectDataDescriptor(Descriptor):
    __metaclass__ = descriptor_metaclass
    struct = 'iiiiiiiiiiiiii'
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