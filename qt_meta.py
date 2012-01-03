import struct
import collections
import itertools

def _take(n, iterable):
    return ''.join(itertools.islice(iterable, n))


"""
ahhoz, hogy faszan hozzaferhessunk az adatokhoz, felul kell irni hogy 
bizonyosokhoz hogy hogyan ferunk hozza. nehanyat at kell szamolni fizikai cimre,
nehanybol a stringet kell kapni, nehanyat 
uint(honeypot::High) <-  ilyen formaban akarunk visszakapni.
"""
def descriptor_metaclass(name, bases, dict):
    if 'struct' in dict and 'fields':
        dict['struct'] = struct.Struct(dict['struct'])
        bases += (collections.namedtuple(name, dict['fields']), )
    return type(name, bases, dict)

class Descriptor(object):

    __metaclass__ = descriptor_metaclass
    strings=set()

    def __getattribute__(self, attr):
        v = super(Descriptor, self).__getattribute__(attr)
        if not attr.startswith('_') and attr in self.__class__.string:
            print self.__class__.string
            return 'HOLA'
        return v

    def __new__(cls, memory_image, string_metadata=None):
        if not hasattr(cls, 'struct') or not hasattr(cls, 'fields'):
            raise NotImplementedError("Define inherited class' struct and fields attributes")
        if cls.strings and not string_metadata:
            raise 
        return super(Descriptor, cls).__new__(cls, *cls.struct.unpack(_take(cls.struct.size, memory_image)))

    
class QMetaClassInfoDescriptor(Descriptor):
    __metaclass__  = descriptor_metaclass
    strings = set(('name', ))
    struct = 'ii'
    fields = 'name, key'

class QMetaMethodDescriptor(Descriptor):
    __metaclass__  = descriptor_metaclass

    strings = set(['signature, parameters'])
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
    struct = 'ii'
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

class QT(object):
    """
    """
    def __init__(self):
        pass