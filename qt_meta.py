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
    struct = 'iii'
    fields = 'name, type, flags'
    
    def read_data(self, memory_image):
        # we had to check whether we have a notification changed method
        return QMetaPropertyChangedDescriptor(memory_image) if True else None
    
class QMetaPropertyChangedDescriptor(Descriptor):
    __metaclass__ = descriptor_metaclass
    struct = 'i'
    fields = 'notifyChanged'
    
class QMetaEnumDescriptor(Descriptor):
    __metaclass__ = descriptor_metaclass
    strings = set(('name', ))
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

class QTClass(object):
    def __init__(self, mmapped_file, qmetaobject_descriptor, pe):
        self.meta_obj_descr = qmetaobject_descriptor
        qt_meta_stringdata = \
            mmapped_file[pe.vtop(meta_obj_descr.qt_meta_stringdata):]
        qt_meta_data = \
            islice(mmapped_file, pe.vtop(meta_obj_descr.qt_meta_data), None)
        
        self.meta_obj_data_descr = \
            QMetaObjectDataDescriptor(qt_meta_data, qt_meta_stringdata)
        
        self.class_infos = []
        
        for i in xrange(meta_obj_data_descr.classinfoCount):
            self.class_infos.append(
                QMetaClassInfoDescriptor(
                    qmetaobject_data, qmetaobject_stringdata
                )
            )
        self.methods = []
        for i in xrange(meta_obj_data_descr.methodCount):
            self.methods.append(
                QMetaMethodDescriptor(
                    qmetaobject_data, qmetaobject_stringdata
                )
            )
        self.properties = []
        for i in xrange(meta_obj_data_descr.propertyCount):
            self.properties.append(
                QMetaPropertyDescriptor(
                    qmetaobject_data, qmetaobject_stringdata
                )
            )
        self.property_notifiactions = []
        for i in xrange(meta_obj_data_descr.propertyCount):
            self.property_notifiactions.append(
                QMetaPropertyChangedDescriptor(
                    qmetaobject_data
                )
            )
        
        enum_count = 0
        for i in xrange(meta_obj_data_descr.enumCount):
            enum_descriptor = QMetaEnumDescriptor(qmetaobject_data, qmetaobject_stringdata)
            enum_count += enum_descriptor.count
        
        for i in xrange(enum_count):
            print QMetaEnumDataDescriptor(qmetaobject_data, qmetaobject_stringdata)

    def __str__(self):
        return 

class QTFile(object):
    def __init__(self, mmapped_file):
        import pefile_mod
        self.pe = pefile_mod.PE(data=mmaped_file)
        self.classes = []
        for i, matchObject in enumerate(compiled_regexp.finditer(mmapped_file)):
            qmetaObjectVirtualAddress = struct.Struct('i').unpack(match_object.group(1))[0]
            qmetaobject_physical_address = self.pe.vtop(metaObjectVirtualAddress)
            qmetaobject_descriptor = QMetaObjectDescriptor(mmapped_file[qmetaobject_physical_address:])
            self.classes.append(QTClass(mmapped_file, qmetaobject_descriptor, self.pe))
            #info_writer(pe, matchObject, mmapped_file)
            if i > 100:
                break