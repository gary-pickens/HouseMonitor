'''
Created on Nov 30, 2012

@author: Gary
'''
import unittest
from lib.currentvalues import CurrentValues
from lib.constants import Constants


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_buildDataBlock(self):
        arg = 555
        name = 'xbee'
        units = 'C'
        time = '12/12/2012 12:12:12'
        data = {Constants.DataPacket.arrival_time: time, \
                Constants.DataPacket.units: units, \
                Constants.DataPacket.name: name}
        val = CurrentValues()
        currentvalue = val.buildDataBlock(arg, data)
        self.assertEqual(currentvalue[Constants.DataPacket.name], name)
        self.assertEqual(currentvalue[Constants.DataPacket.arrival_time], time)
        self.assertEqual(currentvalue[Constants.DataPacket.units], units)
        self.assertEqual(currentvalue[Constants.DataPacket.current_value], arg)

    def check_current_values(self, device, port, arg, name, time, val):
        self.assertIn(device, val._current_values)
        self.assertIn(port, val._current_values[device])
        self.assertIn(Constants.DataPacket.name, val._current_values[device][port])
        self.assertEqual(val._current_values[device][port][Constants.DataPacket.name], name)
        self.assertIn(Constants.DataPacket.current_value, val._current_values[device][port])
        self.assertEqual(val._current_values[device][port][Constants.DataPacket.current_value], arg)
        self.assertIn(Constants.DataPacket.arrival_time, val._current_values[device][port])
        self.assertEqual(val._current_values[device][port][Constants.DataPacket.arrival_time], time)

    def test_store_with_valid_values(self):
        device = 'device'
        port = 'port'
        arg = 555
        name = 'xbee'
        units = 'C'
        time = '12/12/2012 12:12:12'
        data = {Constants.DataPacket.arrival_time: time, \
                Constants.DataPacket.units: units, \
                Constants.DataPacket.name: name}
        val = CurrentValues()
        val.store(arg, device, port, data)
        self.check_current_values(device, port, arg, name, time, val)

    def test_store_two_devices_with_valid_values(self):
        device = ['device0', 'device1']
        port = ['port0', 'port1']
        arg = [555, 666]
        name = ['xbee', 'xyz']
        units = ['C', 'F']
        time = ['12/12/2012 12:12:12', '12/12/2012 12:12:13']
        data = [{Constants.DataPacket.arrival_time: time[0], \
                Constants.DataPacket.units: units[0], \
                Constants.DataPacket.name: name[0]},
                {Constants.DataPacket.arrival_time: time[1], \
                Constants.DataPacket.units: units[1], \
                Constants.DataPacket.name: name[1]}]

        val = CurrentValues()
        val.store(arg[0], device[0], port[0], data[0])
        val.store(arg[1], device[1], port[1], data[1])
        self.check_current_values(device[0], port[0], arg[0], name[0], time[0], val)
        self.check_current_values(device[1], port[1], arg[1], name[1], time[1], val)

    def test_store_one_device_and_two_ports_with_valid_values(self):
        device = ['device0', 'device1']
        port = ['port0', 'port1']
        arg = [555, 666]
        name = ['xbee', 'xyz']
        units = ['C', 'F']
        time = ['12/12/2012 12:12:12', '12/12/2012 12:12:13']
        data = [{Constants.DataPacket.arrival_time: time[0], \
                Constants.DataPacket.units: units[0], \
                Constants.DataPacket.name: name[0]},
                {Constants.DataPacket.arrival_time: time[1], \
                Constants.DataPacket.units: units[1], \
                Constants.DataPacket.name: name[1]}]

        val = CurrentValues()
        val.store(arg[0], device[0], port[0], data[0])
        val.store(arg[1], device[0], port[1], data[1])
        self.check_current_values(device[0], port[0], arg[0], name[0], time[0], val)
        self.check_current_values(device[0], port[1], arg[1], name[1], time[1], val)

    def check_dict(self, device, port, arg, name, time, dict):
        self.assertIn(device, dict)
        self.assertIn(port, dict[device])
        self.assertIn(Constants.DataPacket.name, dict[device][port])
        self.assertEqual(dict[device][port][Constants.DataPacket.name], name)
        self.assertIn(Constants.DataPacket.current_value, dict[device][port])
        self.assertEqual(dict[device][port][Constants.DataPacket.current_value], arg)
        self.assertIn(Constants.DataPacket.arrival_time, dict[device][port])
        self.assertEqual(dict[device][port][Constants.DataPacket.arrival_time], time)

    def test_get_values(self):
        device = ['device0', 'device1']
        port = ['port0', 'port1']
        arg = [555, 666]
        name = ['xbee', 'xyz']
        units = ['C', 'F']
        time = ['12/12/2012 12:12:12', '12/12/2012 12:12:13']
        data = [{Constants.DataPacket.arrival_time: time[0], \
                Constants.DataPacket.units: units[0], \
                Constants.DataPacket.name: name[0]},
                {Constants.DataPacket.arrival_time: time[1], \
                Constants.DataPacket.units: units[1], \
                Constants.DataPacket.name: name[1]}]

        val = CurrentValues()
        val.store(arg[0], device[0], port[0], data[0])
        val.store(arg[1], device[0], port[1], data[1])
        val.store(arg[1], device[1], port[0], data[1])

        dict = val.get()
        self.check_dict(device[0], port[0], arg[0], name[0], time[0], dict)
        self.check_dict(device[0], port[1], arg[1], name[1], time[1], dict)

    def test_get_current_value(self):
        device = ['device0', 'device1']
        port = ['port0', 'port1']
        arg = [555, 666]
        name = ['xbee', 'xyz']
        units = ['C', 'F']
        time = ['12/12/2012 12:12:12', '12/12/2012 12:12:13']
        data = [{Constants.DataPacket.arrival_time: time[0], \
                Constants.DataPacket.units: units[0], \
                Constants.DataPacket.name: name[0]},
                {Constants.DataPacket.arrival_time: time[1], \
                Constants.DataPacket.units: units[1], \
                Constants.DataPacket.name: name[1]}]

        val = CurrentValues()
        val.store(arg[0], device[0], port[0], data[0])
        val.store(arg[1], device[0], port[1], data[1])
        val.store(arg[1], device[1], port[0], data[1])
        val.store(arg[0], device[1], port[1], data[0])
        dict = val.get_current_value(device[0], port[0])
        self.assertEqual(dict[Constants.DataPacket.current_value], arg[0])
        dict = val.get_current_value(device[1], port[1])
        self.assertEqual(dict[Constants.DataPacket.current_value], arg[0])


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
