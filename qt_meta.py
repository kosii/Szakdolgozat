import struct
import collections

#class QMetaClassInfo(namedtuple('QMetaClassInfo', 'name, key')):
#    pass

def descriptor_metaclass(name, bases, dict):
    if 'struct' in dict:
        dict['struct'] = struct.Struct(dict['struct'])
    return type(name, bases, dict)

class MetaClassParser(object):

    __metaclass__ = descriptor_metaclass

    def __new__(cls, memory_image):
        if not hasattr(cls, 'struct') or not hasattr(cls, 'fields'):
            raise NotImplementedError("Define inherited class' struct and fields attributes")
        return cls.namedtuple_factory()(*cls.struct.unpack(memory_image))
    
    @classmethod
    def namedtuple_factory(cls):
        return collections.namedtuple(cls.__name__, cls.fields)

class QMetaClassInfoDescriptor(MetaClassParser):

    __metaclass__  = descriptor_metaclass

    struct = 'ii'
    fields = 'name, key'

class QMetaMethodDesciptor = struct_compiler(
    'QMetaMethodDesciptor', (MetaClassParser, ), 
    {'struct': 'ii', 'fields': 'signature, parameters, type, tag, flags'})

QMetaEnum = struct_c

class QMetaEnum(object):
    def isFlag(self):
        pass
    def isValid(self):
        pass
    def key(self, index):
        pass
    def keyCount(self):
        pass
    def keyToValue(key):
        pass
    def keysToValue(keys):
        pass
    def name(self):
        pass
    def scope(self):
        pass
    def value(self):
        pass
    def valueToKey(self, value):
        pass
    def valueToKeys(self, value):
        pass
class QMetaProperty(object):
    pass

class QMetaObject(object):
    pass
