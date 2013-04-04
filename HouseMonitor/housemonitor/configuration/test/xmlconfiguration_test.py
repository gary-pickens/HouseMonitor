'''
Created on Dec 18, 2012

@author: Gary
'''
import unittest
from configuration.xmlconfiguration import XmlConfiguration
from configuration.xmlconfiguration import ConfigurationFileNotFoundError
from configuration.xmlconfiguration import ConfigurationFileError
import datetime
from lib.common import Common
import logging.config
from lib.constants import Constants
import pprint
from mock import Mock, patch
from lib.getdatetime import GetDateTime
from xml.etree.ElementTree import ElementTree


class myConfiguration(XmlConfiguration):

    @property
    def logger_name(self):
        return 'configuration'

    @property
    def configuration_topic_name(self):
        return 'configuration.xml'

    @property
    def configuration_file_name(self):
        return 'unittest.xml'

    def process_configuration(self, parsed_tree):
        pass


class Test(unittest.TestCase):

    logger = logging.getLogger('UnitTest')

    def setUp(self):
        logging.config.fileConfig("house_monitor_logging.conf")

    def tearDown(self):
        pass

    @patch.object(XmlConfiguration, 'configure')
    def test_configuration_topic_name(self, configure):
        x = myConfiguration()
        self.assertEqual(x.configuration_file_name, "unittest.xml")

    @patch.object(XmlConfiguration, 'configure')
    def test_logger_name(self, configure):
        x = myConfiguration()
        self.assertEqual(x.logger_name, 'configuration')

    @patch.object(XmlConfiguration, 'configure')
    def test__getitem__(self, configure):
        x = myConfiguration()
        x.config = {'device': 'xbee'}
        self.assertEqual(x['device'], 'xbee')

    @patch.object(XmlConfiguration, 'configure')
    def test__setitem__(self, configure):
        x = myConfiguration()
        x['device'] = 'xbee'
        self.assertEqual(x['device'], 'xbee')

    @patch.object(XmlConfiguration, 'configure')
    @patch('configuration.xmlconfiguration.os.path.exists')
    def test_file_name_with_none_passed_in(self, exists, configure):
        x = myConfiguration()
        x.configutation_directory = 'c:\\abc\\config'
        exists.return_value = True
        fn = x.file_name()
        exists.assert_called_once_with('c:\\abc\\config\\unittest.xml')
        self.assertEqual(fn, 'c:\\abc\\config\\unittest.xml')

    @patch.object(XmlConfiguration, 'configure')
    @patch('configuration.xmlconfiguration.os.path.exists')
    def test_file_name_with_a_filename_passed_in(self, exists, configure):
        x = myConfiguration()
        x.configutation_directory = 'c:\\abc\\config'
        exists.return_value = True
        fn = x.file_name('abc.xml')
        exists.assert_called_once_with('c:\\abc\\config\\abc.xml')
        self.assertEqual(fn, 'c:\\abc\\config\\abc.xml')

    @patch.object(XmlConfiguration, 'configure')
    @patch('configuration.xmlconfiguration.os.path.exists')
    def test_file_name_with_a_filename_passed_in_and_no_xml_sufix(self, exists, configure):
        x = myConfiguration()
        x.configutation_directory = 'c:\\abc\\config'
        exists.return_value = True
        fn = x.file_name('abc')
        exists.assert_called_once_with('c:\\abc\\config\\abc.xml')
        self.assertEqual(fn, 'c:\\abc\\config\\abc.xml')

    @patch.object(XmlConfiguration, 'configure')
    @patch('configuration.xmlconfiguration.os.path.exists')
    def test_file_name_with_a_file_that_does_not_exist(self, exists, configure):
        x = myConfiguration()
        x.configutation_directory = 'c:\\abc\\config'
        exists.return_value = False
        with self.assertRaisesRegexp(ConfigurationFileNotFoundError,
                                     'Configuration file does not exist: c:.*abc.*config.*abc.xml'):
            fn = x.file_name('abc')

    @patch.object(myConfiguration, 'parse_xml_file')
    @patch.object(myConfiguration, 'process_configuration')
    def test_configure(self, process_configuration, parse_xml_file):
        device = {'device': {'port': 'port_name'}}
        x = myConfiguration()
        parse_xml_file.return_value = 'parseTree'
        process_configuration.return_value = device
        parse_xml_file.reset_mock()
        process_configuration.reset_mock()
        config = x.configure()
        self.assertDictEqual(config, device)
        parse_xml_file.assert_called_once_with(None)
        process_configuration.assert_called_once_with('parseTree')

# TODO Finish up sometime. Has two built in functions.
#    @patch.object(ElementTree, '__init__')
#    @patch.object(myConfiguration, 'file_name')
#    @patch('configuration.xmlconfiguration.XmlConfiguration.open')
#    @patch.object(myConfiguration, 'configure')
#    def test_parse_xml_file(self, ET, file_name, open, configure):
#        device = {'device': {'port': 'port_name'}}
#        x = myConfiguration()
#        open.return_value = 1
#        file_name.return_value = 'filename'
#        x.parse_xml_file()

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()


xml = '''<?xml version="1.0" encoding="UTF-8"?>
<xbeeInputs>
    <xbee source_address="0x13a200409029bf">
        <name>Garage Door XBee Monitor</name>
        <network_address>0xf9f2</network_address>
        <port portname="dio-0">
            <description>Monitors whether the garage door is open or closed.</description>
            <name>Garage Door Monitor</name>
            <network_address>0xf9f2</network_address>
            <steps type="list">
                <step>step.garage_door_state</step>
                <step>step.CurrentValue</step>
                <step>step.onBooleanChange</step>
                <step>outputs.COSM</step>
            </steps>
            <cosm_channel>1</cosm_channel>
        </port>
        <port portname="adc-1">
            <name>Garage Temperature</name>
            <description>The temperature above the garage door</description>
            <units>F</units>
            <steps type="list">
                <step>step.ZigbeeAnalogNumberToVolts</step>
                <step>step.TMP_36_Volts_to_Centigrade</step>
                <step>step.Centigrade_to_Fahrenheit</step>
                <step>step.Average</step>
                <step>step.FormatValue</step>
                <step>step.CurrentValue</step>
                <step>step.oneInN</step>
                <step>outputs.COSM</step>
            </steps>
            <cosm_channel>2</cosm_channel>
        </port>
    </xbee>
    <xbee source_address="0x13a200408cccc3">
        <name>Sunroom</name>
        <network_address>0xf9f2</network_address>
        <port portname="adc-0">
            <name>Indoor Temperature</name>
            <description>The temperature in the sunroom</description>
            <units>F</units>
            <steps type="list">
                <step>step.ZigbeeAnalogNumberToVolts</step>
                <step>step.TMP_36_Volts_to_Centigrade</step>
                <step>step.Centigrade_to_Fahrenheit</step>
                <step>step.Average</step>
                <step>step.FormatValue</step>
                <step>step.CurrentValue</step>
            </steps>
            <cosm_channel>3</cosm_channel>
        </port>
        <port portname="adc-1">
            <name>Outdoor Temperature</name>
            <description>The temperature at 100 West Lisa Drive Austin TX</description>
            <units>F</units>
            <steps type="list">
                <step>step.ZigbeeAnalogNumberToVolts</step>
                <step>step.TMP_36_Volts_to_Centigrade</step>
                <step>step.Centigrade_to_Fahrenheit</step>
                <step>step.Average</step>
                <step>step.FormatValue</step>
                <step>step.CurrentValue</step>
            </steps>
            <cosm_channel>3</cosm_channel>
        </port>
    </xbee>
</xbeeInputs>
'''
