import unittest, contextlib, mmap

import mock

import context_managers
import pefile_mod
import qt_meta, workers, conf, arguments
import os


class TestPefileMod(unittest.TestCase):
	def setUp(self):
		self.pe = pefile_mod.PE('Honeypot/Honeypot.exe')

	def testGetSectionnameOrdinal(self):
		self.assertEqual(self.pe.GetSectionnameOrdinal('.text'), 0)
		self.assertEqual(self.pe.GetSectionnameOrdinal('.rdata'), 1)
		self.assertRaises(ValueError, self.pe.GetSectionnameOrdinal, '.doesnotexists')

	def testGetSectionnameSection(self):
		self.assertEqual(self.pe.GetSectionnameSection('.text'), self.pe.sections[0])
		self.assertRaises(ValueError, self.pe.GetSectionnameSection, '.doesnotexists')

	def testGetSectionnameContent(self):
		self.assertEqual(self.pe.GetSectionnameContent('.text'), self.pe.sections[0].get_data())
		self.assertRaises(ValueError, self.pe.GetSectionnameContent, '.doesnotexists')

	def testGetPhysicalAddressSectionOrdinal(self):
		self.assertEqual(self.pe.GetPhysicalAddressSectionOrdinal(0x14f0), 1)
		self.assertRaises(ValueError, self.pe.GetPhysicalAddressSectionOrdinal, 0)

	def testGetPhysicalAddressSectionName(self):
		self.assertEqual(self.pe.GetPhysicalAddressSectionName(0x14f0), '.rdata'.ljust(8, '\0'))
		self.assertRaises(ValueError, self.pe.GetPhysicalAddressSectionName, 0)

	def testGetVirtualAddressSectionOrdinal(self):
		self.assertEqual(self.pe.GetVirtualAddressSectionOrdinal(0x4020f0), 1)
		self.assertRaises(ValueError, self.pe.GetVirtualAddressSectionOrdinal, 0)

	def testGetVirtualAddressSectionName(self):
		self.assertEqual(self.pe.GetVirtualAddressSectionName(0x4020f0), '.rdata'.ljust(8, '\0'))
		self.assertRaises(ValueError, self.pe.GetVirtualAddressSectionName, 0)

	def test_vtop(self):
		self.assertEqual(self.pe.vtop(0x4020f0), 0x14f0)
		self.assertEqual(self.pe.vtop(0), 0)
		self.assertRaises(ValueError, self.pe.vtop, 0x4200f0)

	def test_ptov(self):
		self.assertEqual(self.pe.ptov(0x14f0), 0x4020f0)
		self.assertEqual(self.pe.ptov(0), 0)
		self.assertRaises(ValueError, self.pe.ptov, 0x1)

class TestContextManagers(unittest.TestCase):

	def test_restore_cwd(self):
		cwd = os.getcwd()
		with context_managers.restore_cwd():
			os.chdir('injector')
		self.assertEqual(os.getcwd(), cwd)

class TestQtMeta(unittest.TestCase):

	def setUp(self):
		self.string_data = "honeypot\0Sabrina Schweinsteiger\0author\0"\
		    "http://doc.moosesoft.co.uk/1.0/\0url\0"\
		    "\0v\0Signal(int)\0Signal2(int)\0p\0"\
		    "priorityChanged(Priority)\0int\0Slot1(int)\0"\
		    "Priority\0priority\0Option\0Options\0High\0"\
		    "Low\0VeryHigh\0VeryLow\0OptionA\0OptionB\0"\
		    "OptionC\0OptionD\0OptionE\0OptionF\0"

	def test_string_reader(self):
		self.assertEqual(qt_meta.string_reader('abcd\0asd'), 'abcd')

	def test_take(self):
		self.assertEqual(qt_meta._take(4, xrange(10)), '0123')

	def test_class_creation_failure(self):
		self.assertRaises(RuntimeError, qt_meta.DescriptorMetaclass('noStructClass', (qt_meta.Descriptor,), {}), '' )
		self.assertRaises(RuntimeError, qt_meta.DescriptorMetaclass('noStructClass', (qt_meta.Descriptor,), {'struct': ''}), '')
		self.assertRaises(RuntimeError, qt_meta.DescriptorMetaclass('noStructClass', (qt_meta.Descriptor,), {'fields': ''}), '')
		qt_meta.DescriptorMetaclass('noStructClass', (qt_meta.Descriptor,), {'fields': '', 'struct': ''})('')
		self.assertRaises(RuntimeError, qt_meta.DescriptorMetaclass('noStructClass', (qt_meta.Descriptor,), {'struct': '', 'fields': '', 'strings': set(('a', ))}), '')

	def test_class_instantiation(self):
		classinfo = qt_meta.QMetaClassInfoDescriptor('\x20\0\0\0\x09\0\0\0', string_metadata=self.string_data)
		self.assertEqual(classinfo.key, "author")
		self.assertEqual(classinfo.value, "Sabrina Schweinsteiger")

		method = qt_meta.QMetaMethodDescriptor('\x87\0\0\0\x4c\0\0\0\x83\0\0\0\x4b\0\0\0\x0a\0\0\0', string_metadata=self.string_data)
		self.assertEqual(method.signature, "Slot1(int)")
		self.assertEqual(method.parameters, "v")
		self.assertEqual(method.type, "int")
		self.assertEqual(method.tag, "")
		self.assertEqual(method.flags, 0x0a)

		prop = qt_meta.QMetaPropertyDescriptor('\x9b\0\0\0\x92\0\0\0\x0b\x51\x49\0', string_metadata=self.string_data)
		self.assertEqual(prop.name, "priority")
		self.assertEqual(prop.type, "Priority")
		self.assertEqual(prop.flags, 0x0049510b)

	def test_QTFile(self):
		with context_managers.filedescriptor('Honeypot/Honeypot.exe', os.O_RDONLY) as fd:
			with contextlib.closing(mmap.mmap(fd, length=0, access=mmap.ACCESS_READ)) as mmapped_file:
				qt_file = qt_meta.QTFile(mmapped_file)
		    	self.assertEqual(len(qt_file.classes), 2)
		    	self.assertEqual([klass.name for klass in qt_file.classes], ['honeypot', 'no_signals'])
		    	self.assertEqual([klass.safe_name for klass in qt_file.classes], ['honeypot', 'no_signals'])
		    	self.assertEqual([klass.metacall_address_name for klass in qt_file.classes], ['honeypot_metacall_address', 'no_signals_metacall_address'])
		    	self.assertEqual([klass.metacall_hook_name for klass in qt_file.classes], ['honeypot_metacall_address_hook', 'no_signals_metacall_address_hook'])
		    	self.assertEqual([klass.metaobject_function for klass in qt_file.classes], [0x401130, 0x401300])

class testWorkers(unittest.TestCase):
	@mock.patch('subprocess.call')
	def test_launcher(self, call_mock):
		workers.launcher('cmd')
		self.assertTrue(call_mock.called)

	@mock.patch('zmq.Socket')
	@mock.patch('workers.Receiver')
	def test_Receiver(self, Receiver_mock, recv_mock):
		recv_mock.recv.return_value = "Hello"
		Receiver_mock.daemon = False
		receiver_thread = Receiver_mock.return_value
		receiver_thread.start()
		self.assertTrue(recv_mock.called)
		del receiver_thread