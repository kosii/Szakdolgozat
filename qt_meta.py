import struct
import collections

#class QMetaClassInfo(namedtuple('QMetaClassInfo', 'name, key')):
#    pass

def descriptor_metaclass(name, bases, dict):
    if 'struct' in dict:
        dict['struct'] = struct.Struct(dict['struct'])
    return type(name, bases, dict)

class Descriptor(object):

    __metaclass__ = descriptor_metaclass

    def __new__(cls, memory_image):
        if not hasattr(cls, 'struct') or not hasattr(cls, 'fields'):
            raise NotImplementedError("Define inherited class' struct and fields attributes")
        return cls.namedtuple_factory()(*cls.struct.unpack(memory_image))
    
    @classmethod
    def namedtuple_factory(cls):
        return collections.namedtuple(cls.__name__, cls.fields)

class QMetaClassInfoDescriptor(Descriptor):

    __metaclass__  = descriptor_metaclass

    struct = 'ii'
    fields = 'name, key'

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
    fields = key, value
class QMetaObject(object):
    pass
