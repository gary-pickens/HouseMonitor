'''
Created on Dec 18, 2012

@author: Gary
'''
import unittest
from housemonitor.configuration.xmlconfiguration import XmlConfiguration
from housemonitor.configuration.xmlconfiguration import ConfigurationFileNotFoundError
from housemonitor.configuration.xmlconfiguration import ConfigurationFileError
import datetime
from housemonitor.lib.common import Common
import logging.config
from housemonitor.lib.constants import Constants
import pprint
from mock import Mock, patch, MagicMock
from housemonitor.lib.getdatetime import GetDateTime
from xml.etree.ElementTree import ElementTree, fromstring


class myConfiguration( XmlConfiguration ):

    @property
    def logger_name( self ):
        return 'configuration'

    @property
    def configuration_topic_name( self ):
        return 'configuration.xml'

    @property
    def configuration_file_name( self ):
        return 'unittest.xml'

#     def process_configuration( self, parsed_tree ):
#         pass


class Test( unittest.TestCase ):

    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )

    def tearDown( self ):
        pass

    @patch.object( XmlConfiguration, 'configure' )
    def test_configuration_topic_name( self, configure ):
        x = myConfiguration()
        self.assertEqual( x.configuration_file_name, "unittest.xml" )

    @patch.object( XmlConfiguration, 'configure' )
    def test_logger_name( self, configure ):
        x = myConfiguration()
        self.assertEqual( x.logger_name, 'configuration' )

    @patch.object( XmlConfiguration, 'configure' )
    def test__getitem__( self, configure ):
        x = myConfiguration()
        x.config = {'device': 'xbee'}
        self.assertEqual( x['device'], 'xbee' )

    @patch.object( XmlConfiguration, 'configure' )
    def test__setitem__( self, configure ):
        x = myConfiguration()
        x['device'] = 'xbee'
        self.assertEqual( x['device'], 'xbee' )

    @patch.object( XmlConfiguration, 'configure' )
    @patch( 'housemonitor.configuration.xmlconfiguration.os.path.exists' )
    def test_file_name_with_none_passed_in( self, exists, configure ):
        x = myConfiguration()
        x.configutation_directory = 'c:\\abc\\config'
        exists.return_value = True
        fn = x.file_name()
        exists.assert_called_once_with('c:\\abc\\config/unittest.xml')
        self.assertEqual(fn, 'c:\\abc\\config/unittest.xml')

    @patch.object( XmlConfiguration, 'configure' )
    @patch( 'housemonitor.configuration.xmlconfiguration.os.path.exists' )
    def test_file_name_with_a_filename_passed_in( self, exists, configure ):
        x = myConfiguration()
        x.configutation_directory = 'c:\\abc\\config'
        exists.return_value = True
        fn = x.file_name( 'abc.xml' )
        exists.assert_called_once_with('c:\\abc\\config/abc.xml')
        self.assertEqual(fn, 'c:\\abc\\config/abc.xml')

    @patch.object( XmlConfiguration, 'configure' )
    @patch( 'housemonitor.configuration.xmlconfiguration.os.path.exists' )
    def test_file_name_with_a_filename_passed_in_and_no_xml_sufix( self, exists, configure ):
        x = myConfiguration()
        x.configutation_directory = 'c:\\abc\\config'
        exists.return_value = True
        fn = x.file_name( 'abc' )
        exists.assert_called_once_with('c:\\abc\\config/abc.xml')
        self.assertEqual(fn, 'c:\\abc\\config/abc.xml')

    @patch.object( XmlConfiguration, 'configure' )
    @patch( 'housemonitor.configuration.xmlconfiguration.os.path.exists' )
    def test_file_name_with_a_file_that_does_not_exist( self, exists, configure ):
        x = myConfiguration()
        x.configutation_directory = 'c:\\abc\\config'
        exists.return_value = False
        with self.assertRaisesRegexp( ConfigurationFileNotFoundError,
                                     'Configuration file does not exist: .*abc.*config.*abc.xml'):
            fn = x.file_name( 'abc' )

    @patch.object( myConfiguration, 'parse_xml_file' )
    @patch.object( myConfiguration, 'process_configuration' )
    def test_configure( self, process_configuration, parse_xml_file ):
        device = {'device': {'port': 'port_name'}}
        x = myConfiguration()
        parse_xml_file.return_value = 'parseTree'
        process_configuration.return_value = device
        parse_xml_file.reset_mock()
        process_configuration.reset_mock()
        config = x.configure()
        self.assertDictEqual( config, device )
        parse_xml_file.assert_called_once_with( None )
        process_configuration.assert_called_once_with( 'parseTree' )

    @patch( 'housemonitor.configuration.xmlconfiguration.XmlConfiguration.configure' )
    @patch.object( ElementTree, 'parse' )
    @patch( '__builtin__.open' )
    def test_parse_xml_file( self, pat, parse, fn ):
        open_name = '%s.open' % __name__
        with patch( open_name, create=True ) as mock_open:
            filename = u'filename'
            mock_open.return_value = MagicMock( spec=file )
            xml = myConfiguration()

            xml.file_name = MagicMock( return_value=filename )
            xml.parse_xml_file( filename )
            xml.file_name.assert_called_once_with( filename )
            file_handle = mock_open.return_value.__enter__.return_value
#            parse.assert_called_once_with( file_handle )

    @patch( 'housemonitor.configuration.xmlconfiguration.os.getcwd' )
    def test_ConfigurationFileError( self, getcwd ):
        value = 'xxx'
        getcwd.return_value = 'abc/'
        c = ConfigurationFileError( value )
        self.assertEqual( c.__str__(), '\'Error in configuration file abc/xxx near "xxx"\'' )

    @patch.object( XmlConfiguration, 'configure' )
    def test_process_configuration_with_type_is_list( self, getcwd ):
        xml = '''<steps type="list">
                <step>step.garage_door_state</step>
            </steps>'''
        c = myConfiguration()
        et = ElementTree()
        parent = fromstring( xml )
        steps = c.process_configuration( parent )
        self.assertListEqual( steps, ['step.garage_door_state'] )

    @patch.object( XmlConfiguration, 'configure' )
    def test_process_configuration_with_type_is_list_with_sublist( self, getcwd ):
        xml = '''<steps type="list">
                    <step>a</step>
                    <steps type="list">
                        <step>b</step>
                    </steps>
                </steps>'''
        c = myConfiguration()
        et = ElementTree()
        parent = fromstring( xml )
        steps = c.process_configuration( parent )
        self.assertListEqual( steps, ['a', ['b']] )

    @patch.object( XmlConfiguration, 'configure' )
    def test_process_configuration_with_type_is_dict( self, getcwd ):
        xml = '''<port>
            <a>aaa</a>
            <b>bbb</b>
            <c>ccc</c>
        </port>'''
        c = myConfiguration()
        et = ElementTree()
        parent = fromstring( xml )
        d = c.process_configuration( parent )
        self.assertDictEqual( d, {'a': 'aaa', 'b': 'bbb', 'c': 'ccc'} )

    @patch.object( XmlConfiguration, 'configure' )
    def test_process_configuration_with_type_is_dict_with_subdict( self, getcwd ):
        xml = '''<port>
            <a>aaa</a>
            <part>
                <b>bbb</b>
                <c>ccc</c>
            </part>
        </port>'''
        c = myConfiguration()
        et = ElementTree()
        parent = fromstring( xml )
        d = c.process_configuration( parent )
        self.assertDictEqual( d, {'a': 'aaa', 'part': {'b': 'bbb', 'c': 'ccc'}} )

    @patch.object( XmlConfiguration, 'configure' )
    def test_process_configuration_with_configuration_file_error( self, getcwd ):
        xml = '''<steps type="xxx">
                    <step>a</step>
                    <steps type="list">
                        <step>b</step>
                    </steps>
                </steps>'''
        c = myConfiguration()
        et = ElementTree()
        parent = fromstring( xml )
        with self.assertRaisesRegexp( ConfigurationFileError, "Error in configuration file.*" ):
            c.process_configuration( parent )

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
