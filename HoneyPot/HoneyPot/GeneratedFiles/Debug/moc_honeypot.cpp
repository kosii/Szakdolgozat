/****************************************************************************
** Meta object code from reading C++ file 'honeypot.h'
**
** Created: Sat Nov 19 22:57:41 2011
**      by: The Qt Meta Object Compiler version 62 (Qt 4.7.4)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../../honeypot.h"
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'honeypot.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 62
#error "This file was generated using the moc from 4.7.4. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
static const uint qt_meta_data_honeypot[] = {

 // content:
       5,       // revision
       0,       // classname
       2,   14, // classinfo
       3,   18, // methods
       1,   33, // properties
       3,   37, // enums/sets
       0,    0, // constructors
       0,       // flags
       2,       // signalCount

 // classinfo: key, value
      32,    9,
      71,   39,

 // signals: signature, parameters, type, tag, flags
      76,   75,   75,   75, 0x05,
     104,  102,   75,   75, 0x05,

 // slots: signature, parameters, type, tag, flags
     120,  102,  116,   75, 0x0a,

 // properties: name, type, flags
     140,  131, 0x0049510b,

 // properties: notify_signal_id
       0,

 // enums: name, flags, count, data
     131, 0x0,    4,   49,
     149, 0x1,    6,   57,
     156, 0x1,    6,   69,

 // enum data: key, value
     164, uint(honeypot::High),
     169, uint(honeypot::Low),
     173, uint(honeypot::VeryHigh),
     182, uint(honeypot::VeryLow),
     190, uint(honeypot::OptionA),
     198, uint(honeypot::OptionB),
     206, uint(honeypot::OptionC),
     214, uint(honeypot::OptionD),
     222, uint(honeypot::OptionE),
     222, uint(honeypot::OptionE),
     190, uint(honeypot::OptionA),
     198, uint(honeypot::OptionB),
     206, uint(honeypot::OptionC),
     214, uint(honeypot::OptionD),
     222, uint(honeypot::OptionE),
     222, uint(honeypot::OptionE),

       0        // eod
};

static const char qt_meta_stringdata_honeypot[] = {
    "honeypot\0Sabrina Schweinsteiger\0author\0"
    "http://doc.moosesoft.co.uk/1.0/\0url\0"
    "\0priorityChanged(Priority)\0v\0Signal(int)\0"
    "int\0Slot1(int)\0Priority\0priority\0"
    "Option\0Options\0High\0Low\0VeryHigh\0"
    "VeryLow\0OptionA\0OptionB\0OptionC\0OptionD\0"
    "OptionE\0"
};

const QMetaObject honeypot::staticMetaObject = {
    { &QObject::staticMetaObject, qt_meta_stringdata_honeypot,
      qt_meta_data_honeypot, 0 }
};

#ifdef Q_NO_DATA_RELOCATION
const QMetaObject &honeypot::getStaticMetaObject() { return staticMetaObject; }
#endif //Q_NO_DATA_RELOCATION

const QMetaObject *honeypot::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->metaObject : &staticMetaObject;
}

void *honeypot::qt_metacast(const char *_clname)
{
    if (!_clname) return 0;
    if (!strcmp(_clname, qt_meta_stringdata_honeypot))
        return static_cast<void*>(const_cast< honeypot*>(this));
    return QObject::qt_metacast(_clname);
}

int honeypot::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        switch (_id) {
        case 0: priorityChanged((*reinterpret_cast< Priority(*)>(_a[1]))); break;
        case 1: Signal((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 2: { int _r = Slot1((*reinterpret_cast< int(*)>(_a[1])));
            if (_a[0]) *reinterpret_cast< int*>(_a[0]) = _r; }  break;
        default: ;
        }
        _id -= 3;
    }
#ifndef QT_NO_PROPERTIES
      else if (_c == QMetaObject::ReadProperty) {
        void *_v = _a[0];
        switch (_id) {
        case 0: *reinterpret_cast< Priority*>(_v) = priority(); break;
        }
        _id -= 1;
    } else if (_c == QMetaObject::WriteProperty) {
        void *_v = _a[0];
        switch (_id) {
        case 0: setPriority(*reinterpret_cast< Priority*>(_v)); break;
        }
        _id -= 1;
    } else if (_c == QMetaObject::ResetProperty) {
        _id -= 1;
    } else if (_c == QMetaObject::QueryPropertyDesignable) {
        _id -= 1;
    } else if (_c == QMetaObject::QueryPropertyScriptable) {
        _id -= 1;
    } else if (_c == QMetaObject::QueryPropertyStored) {
        _id -= 1;
    } else if (_c == QMetaObject::QueryPropertyEditable) {
        _id -= 1;
    } else if (_c == QMetaObject::QueryPropertyUser) {
        _id -= 1;
    }
#endif // QT_NO_PROPERTIES
    return _id;
}

// SIGNAL 0
void honeypot::priorityChanged(Priority _t1)
{
    void *_a[] = { 0, const_cast<void*>(reinterpret_cast<const void*>(&_t1)) };
    QMetaObject::activate(this, &staticMetaObject, 0, _a);
}

// SIGNAL 1
void honeypot::Signal(int _t1)
{
    void *_a[] = { 0, const_cast<void*>(reinterpret_cast<const void*>(&_t1)) };
    QMetaObject::activate(this, &staticMetaObject, 1, _a);
}
QT_END_MOC_NAMESPACE
