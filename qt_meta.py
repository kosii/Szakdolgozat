import struct
from collections import namedtuple

class QMetaClassInfo(object):
    t = namedtuple
    def __init__(self, name, key):
        self.name = name
        self.key = key
    def name(self):
        return self.name
    def key(self):
        return self.key

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