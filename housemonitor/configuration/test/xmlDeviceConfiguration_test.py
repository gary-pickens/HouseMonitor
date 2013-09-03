'''
Created on Dec 20, 2012

@author: Gary
'''
import unittest
from housemonitor.configuration.xmlDeviceConfiguration import xmlDeviceConfiguration
from housemonitor.configuration.xmlDeviceConfiguration import InvalidDeviceError
from housemonitor.configuration.xmlDeviceConfiguration import InvalidPortError
from housemonitor.configuration.xmlDeviceConfiguration import InvalidConfigurationOptionError
import datetime
from housemonitor.lib.common import Common
import logging.config
from housemonitor.lib.constants import Constants
import pprint
from mock import Mock, patch
from housemonitor.lib.getdatetime import GetDateTime
import xml.etree.ElementTree as ET


class Test( unittest.TestCase ):

    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )

    def tearDown( self ):
        pass

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_configuration_topic_name( self, configure ):
        x = xmlDeviceConfiguration()
        self.assertEqual( x.configuration_topic_name, Constants.TopicNames.xmlDeviceConfiguration )

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_configuration_file_name( self, configure ):
        x = xmlDeviceConfiguration()
        self.assertEqual( x.configuration_file_name, 'configuration.xmlDeviceConfiguration' )

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_logger_name( self, configure ):
        x = xmlDeviceConfiguration()
        self.assertEqual( x.logger_name, "configuration" )

# process_configuration

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_process_configuration( self, configure ):
        expected_config = {'0x13a200409029bf': {'dio-0': {'cosm_channel': '1',
             'description': 'Monitors whether the garage door is open or closed.',
             'name': 'Garage Door Monitor',
             'network_address': '0xf9f2',
             'steps': ['step.garage_door_state',
             'step.CurrentValue',
             'step.onBooleanChange',
             'outputs.COSM']},
             'name': 'Garage Door XBee Monitor',
             'network_address': '0xf9f2'}}
        self.maxDiff = None
        xdc = xmlDeviceConfiguration()
        root = ET.fromstring( xml )
        config = xdc.process_configuration( root )
        self.assertEqual( config, expected_config )

# Test get_steps

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_get_steps( self, configure ):
        steps = [i for i in range( 10 )]
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {'port':
                                    {Constants.XbeeConfiguration.name: 'test',
                                    Constants.XbeeConfiguration.steps: steps}}}
        self.assertSequenceEqual( xdc.get_steps( 'device', 'port' ), steps )

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_get_steps_with_invalid_device( self, configure ):
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {Constants.XbeeConfiguration.name: 'test'}}
        with self.assertRaisesRegexp( InvalidDeviceError, 'Invalid device (.*)' ):
            xdc.get_steps( 'device-1', 'port' )

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_get_steps_with_invalid_port( self, configure ):
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {'port': {Constants.XbeeConfiguration.name: 'test'}}}
        with self.assertRaisesRegexp( InvalidPortError, 'Invalid port \(port-1\)' ):
            xdc.get_steps( 'device', 'port-1' )

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_get_steps_with_invalid_option( self, configure ):
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {'port': {Constants.XbeeConfiguration.description: 'test'}}}
        with self.assertRaisesRegexp( InvalidConfigurationOptionError, 'Required configuration option not present (.*) for device(.*) port (.*)' ):
            xdc.get_steps( 'device', 'port' )

# Test get_name

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_get_name( self, configure ):
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {Constants.XbeeConfiguration.name: 'test'}}
        self.assertEqual( xdc.get_name( 'device' ), 'test' )

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_get_name_with_invalid_device( self, configure ):
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {Constants.XbeeConfiguration.name: 'test'}}
        with self.assertRaisesRegexp( InvalidDeviceError, 'Invalid device (.*)' ):
            xdc.get_name( 'device-1' )

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_get_name_with_no_name_device( self, configure ):
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {Constants.XbeeConfiguration.description: 'test'}}
        with self.assertRaisesRegexp( InvalidConfigurationOptionError, 'Required configuration option not present (.*) for device(.*) port (.*)' ):
            xdc.get_name( device='device' )

# get_source_address

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_get_source_address( self, configure ):
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {Constants.XbeeConfiguration.name: 'test',
                                  Constants.XbeeConfiguration.source_address: 'address'}}
        self.assertEqual( xdc.get_source_address( 'device' ), 'address' )

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_get_source_address_with_invalid_device( self, configure ):
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {Constants.XbeeConfiguration.name: 'test',
                                  Constants.XbeeConfiguration.source_address: 'address'}}
        with self.assertRaisesRegexp( InvalidDeviceError, 'Invalid device (.*)' ):
            xdc.get_source_address( 'device-1' )

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_get_source_address_with_invalid_option( self, configure ):
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {Constants.XbeeConfiguration.name: 'test'}}
        with self.assertRaisesRegexp( InvalidConfigurationOptionError, 'Required configuration option not present (.*) for device(.*) port (.*)' ):
            xdc.get_source_address( device='device' )

# get_network_address

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_get_network_address( self, configure ):
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {Constants.XbeeConfiguration.network_address: 'test'}}
        self.assertEqual( xdc.get_network_address( 'device' ), 'test' )

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_get_network_address_with_invalid_device( self, configure ):
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {Constants.XbeeConfiguration.name: 'test'}}
        with self.assertRaisesRegexp( InvalidDeviceError, 'Invalid device (.*)' ):
            xdc.get_network_address( 'device-1' )

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_get_network_address_with_no_name_device( self, configure ):
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {Constants.XbeeConfiguration.description: 'test'}}
        with self.assertRaisesRegexp( InvalidConfigurationOptionError, 'Required configuration option not present (.*) for device(.*) port (.*)' ):
            xdc.get_network_address( device='device' )

# get_port_name

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_get_port_name( self, configure ):
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {'port': {Constants.XbeeConfiguration.name: 'test'}}}
        self.assertSequenceEqual( xdc.get_port_name( 'device', 'port' ), 'test' )

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_get_port_name_with_invalid_device( self, configure ):
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {Constants.XbeeConfiguration.name: 'test'}}
        with self.assertRaisesRegexp( InvalidDeviceError, 'Invalid device (.*)' ):
            xdc.get_port_name( 'device-1', 'port' )

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_get_port_name_with_invalid_port( self, configure ):
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {'port': {Constants.XbeeConfiguration.name: 'test'}}}
        with self.assertRaisesRegexp( InvalidPortError, 'Invalid port .port-1.' ):
            xdc.get_port_name( 'device', 'port-1' )

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_get_port_name_with_invalid_option( self, configure ):
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {'port': {Constants.XbeeConfiguration.description: 'test'}}}
        with self.assertRaisesRegexp( InvalidConfigurationOptionError, 'Required configuration option not present (.*) for device(.*) port (.*)' ):
            xdc.get_port_name( 'device', 'port' )

# get_port_description

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_get_port_description( self, configure ):
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {'port': {Constants.XbeeConfiguration.description: 'description'}}}
        self.assertEqual( xdc.get_port_description( 'device', 'port' ), 'description' )

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_get_port_description_with_invalid_device( self, configure ):
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {Constants.XbeeConfiguration.description: 'test'}}
        with self.assertRaisesRegexp( InvalidDeviceError, 'Invalid device (.*)' ):
            xdc.get_port_description( 'device-1', 'port' )

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_get_port_description_with_invalid_port( self, configure ):
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {'port': {Constants.XbeeConfiguration.name: 'test'}}}
        with self.assertRaisesRegexp( InvalidPortError, 'Invalid port \(port-1\)' ):
            xdc.get_port_description( 'device', 'port-1' )

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_get_port_description_with_invalid_option( self, configure ):
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {'port': {Constants.XbeeConfiguration.name: 'test'}}}
        with self.assertRaisesRegexp( InvalidConfigurationOptionError, 'Required configuration option not present (.*) for device(.*) port (.*)' ):
            xdc.get_port_description( 'device', 'port' )

# get_port_units

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_get_port_units( self, configure ):
        units = 'C'
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {'port':
                                    {Constants.XbeeConfiguration.name: 'test',
                                    Constants.XbeeConfiguration.units: units}}}
        self.assertEqual( xdc.get_port_units( 'device', 'port' ), units )

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_get_port_units_with_invalid_device( self, configure ):
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {'port': {Constants.XbeeConfiguration.units: 'test'}}}
        with self.assertRaisesRegexp( InvalidDeviceError, 'Invalid device \(.*\)' ):
            xdc.get_port_units( 'device-1', 'port' )

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_get_port_units_with_invalid_port( self, configure ):
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {'port': {Constants.XbeeConfiguration.name: 'test'}}}
        with self.assertRaisesRegexp( InvalidPortError, 'Invalid port \(port-1\)' ):
            xdc.get_port_units( 'device', 'port-1' )

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_get_port_units_with_invalid_option( self, configure ):
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {'port': {Constants.XbeeConfiguration.description: 'test'}}}
        with self.assertRaisesRegexp( InvalidConfigurationOptionError, 'Required configuration option not present (.*) for device(.*) port (.*)' ):
            xdc.get_port_units( 'device', 'port' )

# get_port_type

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_get_port_type( self, configure ):
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {'port': {Constants.XbeeConfiguration.type: 'type'}}}
        self.assertEqual( xdc.get_port_type( 'device', 'port' ), 'type' )

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_get_port_type_with_invalid_device( self, configure ):
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {Constants.XbeeConfiguration.type: 'type'}}
        with self.assertRaisesRegexp( InvalidDeviceError, 'Invalid device (.*)' ):
            xdc.get_port_type( 'device-1', 'port' )

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_get_port_type_with_invalid_port( self, configure ):
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {'port': {Constants.XbeeConfiguration.type: 'type'}}}
        with self.assertRaisesRegexp( InvalidPortError, 'Invalid port \(port-1\)' ):
            xdc.get_port_type( 'device', 'port-1' )

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_get_port_type_with_invalid_option( self, configure ):
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {'port': {Constants.XbeeConfiguration.description: 'test'}}}
        with self.assertRaisesRegexp( InvalidConfigurationOptionError, 'Required configuration option not present (.*) for device(.*) port (.*)' ):
            xdc.get_port_type( 'device', 'port' )

    def test_InvalidConfigurationOptionError( self ):
        device = 'device name'
        e = InvalidConfigurationOptionError( device )
        self.assertRegexpMatches( e.value, 'Required configuration option not present for device "device name"' )

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_valid_device( self, c ):
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {'port': 'a'}, 'device 1': {'port 1': 'b'}}
        device = xdc.valid_device( 'device' )
        self.assertEqual( device, 'device' )

    @patch.object( xmlDeviceConfiguration, 'configure' )
    def test_in_valid_device( self, c ):
        xdc = xmlDeviceConfiguration()
        xdc.devices = {'device': {'port': 'a'}, 'device 1': {'port 1': 'b'}}
        with self.assertRaisesRegexp( InvalidDeviceError, 'device a' ):
            xdc.valid_device( 'device a' )


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()    # pragma: no cover


xml = '''<xbeeInputs>
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
    </xbee>
</xbeeInputs>
'''
