import struct
import collections

#class QMetaClassInfo(namedtuple('QMetaClassInfo', 'name, key')):
#    pass

def struct_compiler(name, bases, dict):
    if 'struct' in dict:
        dict['struct'] = struct.Struct(dict['struct'])
    return type(name, bases, dict)



class MetaClassParser(object):

    __metaclass__ = struct_compiler

    def __new__(cls, memory_image):
        if not hasattr(cls, 'struct') or not hasattr(cls, 'fields'):
            raise NotImplementedError("Define inherited class' struct and fields attributes")
        return cls.namedtuple_factory()(*cls.struct.unpack(memory_image))
    
    @classmethod
    def namedtuple_factory(cls):
        return collections.namedtuple(cls.__name__, cls.fields)

MetaClassParser.__class__ = struct_compiler
print 1, type(MetaClassParser)

class QMetaClassInfo(MetaClassParser):
    struct = "ii"
    fields = 'name, key'

print QMetaClassInfo.struct
print QMetaClassInfo('\01\00\00\00\00\01\00\00')

class QMetaMethod(object):

    def methodIndex(self):
        pass
    
    def methodType(self):
        pass
    
    def parameterNames(self):
        pass
    
    def parameterTypes(self):
        pass
    
    def signature(self):
        pass
    
    def tag(self):
        pass
    
    def typeName(self):
        pass
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
