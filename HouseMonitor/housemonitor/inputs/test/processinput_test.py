'''
Created on Dec 18, 2012

@author: Gary
'''
from housemonitor.inputs.processinput import ProcessInput
from housemonitor.inputs.processinput import ProcessXBeeInput
from housemonitor.inputs.processinput import ProcessStatusRequests
from housemonitor.inputs.dataenvelope import DataEnvelope
from housemonitor.lib.hmqueue import HMQueue
from housemonitor.configuration.xmlDeviceConfiguration import xmlDeviceConfiguration
from housemonitor.configuration.xmlDeviceConfiguration import InvalidDeviceError
from housemonitor.configuration.xmlDeviceConfiguration import InvalidPortError
from housemonitor.configuration.xmlDeviceConfiguration import InvalidConfigurationOptionError

import unittest
import datetime
from housemonitor.lib.common import Common
import logging.config
from housemonitor.lib.constants import Constants
import pprint
from mock import Mock, MagicMock, patch
from housemonitor.lib.getdatetime import GetDateTime


class Test( unittest.TestCase ):
    logger = logging.getLogger( 'UnitTest' )

    valid_devices_configuration = {'0x13a200408cccc3': {'adc-0': {'cosm_channel': '3',
                                   'description': 'The temperature in the sunroom',
                                   'name': 'Indoor Temperature',
                                   'steps': ['step.ZigbeeAnalogNumberToVolts',
                                             'step.TMP_36_Volts_to_Centigrade',
                                             'step.Centigrade_to_Fahrenheit',
                                             'step.Average',
                                             'step.FormatValue',
                                             'step.CurrentValue'],
                                   'units': 'F'},
                         'adc-1': {'cosm_channel': '3',
                                   'description': 'The temperature at 100 West Lisa Drive Austin TX',
                                   'name': 'Outdoor Temperature',
                                   'steps': ['step.ZigbeeAnalogNumberToVolts',
                                             'step.TMP_36_Volts_to_Centigrade',
                                             'step.Centigrade_to_Fahrenheit',
                                             'step.Average',
                                             'step.FormatValue',
                                             'step.CurrentValue'],
                                   'units': 'F'},
                         'name': 'Sunroom',
                         'network_address': '0xf9f2'},
    '0x13a200409029bf': {'adc-1': {'cosm_channel': '2',
                                   'description': 'The temperature above the garage door',
                                   'name': 'Garage Temperature',
                                   'steps': ['step.ZigbeeAnalogNumberToVolts',
                                             'step.TMP_36_Volts_to_Centigrade',
                                             'step.Centigrade_to_Fahrenheit',
                                             'step.Average',
                                             'step.FormatValue',
                                             'step.CurrentValue',
                                             'step.oneInN',
                                             'outputs.COSM'],
                                   'units': 'F'},
                         'dio-0': {'cosm_channel': '1',
                                   'description': 'Monitors whether the garage door is open or closed.',
                                   'name': 'Garage Door Monitor',
                                   'network_address': '0xf9f2',
                                   'steps': ['step.garage_door_state',
                                             'step.CurrentValue',
                                             'step.onBooleanChange',
                                             'outputs.COSM']},
                         'name': 'Garage Door XBee Monitor',
                         'network_address': '0xf9f2'}}

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )

    def tearDown( self ):
        pass

# ProcessXBeeInput

    def test_ProcessXBeeInput_logger_name( self ):
        devices = {'device': {'port': {}}}
        pxi = ProcessXBeeInput( devices )
        self.assertEqual( pxi.logger_name, Constants.LogKeys.inputsZigBee )

    @patch( 'housemonitor.inputs.processinput.Common.send' )
    @patch( 'housemonitor.inputs.processinput.xmlDeviceConfiguration.configure' )
    def test_XBeeInput_process_invalid_device_error( self, config, send ):
        env = DataEnvelope()
        env.packet = {'source_addr_long': '\x00\x13\xa2\x00@\x90)\xbf',
                       'source_addr': '\xf9\xf2',
                        'id': 'rx_io_data_long_addr',
                         'samples': [{'adc-1': 622}],
                       'options': '\x01'}

        xd = xmlDeviceConfiguration()
        xd.devices = {'0x13a200408cccc3': {'adc-0': {'cosm_channel': '3',
                                   'description': 'The temperature in the sunroom',
                                   'name': 'Indoor Temperature',
                                   'steps': ['step.ZigbeeAnalogNumberToVolts',
                                             'step.TMP_36_Volts_to_Centigrade',
                                             'step.Centigrade_to_Fahrenheit',
                                             'step.Average',
                                             'step.FormatValue',
                                             'step.CurrentValue'],
                                   'units': 'F'},
                         'adc-1': {'cosm_channel': '3',
                                   'description': 'The temperature at 100 West Lisa Drive Austin TX',
                                   'name': 'Outdoor Temperature',
                                   'steps': ['step.ZigbeeAnalogNumberToVolts',
                                             'step.TMP_36_Volts_to_Centigrade',
                                             'step.Centigrade_to_Fahrenheit',
                                             'step.Average',
                                             'step.FormatValue',
                                             'step.CurrentValue'],
                                   'units': 'F'},
                         'name': 'Sunroom',
                         'network_address': '0xf9f2'}}

        xp = ProcessXBeeInput( xd )
        xp.logger.exception = MagicMock()
        value = xp.process( env )
        xp.logger.exception.assert_called_with( "'Invalid device (0x13a200409029bf)'" )
        self.assertEqual( send.call_count, 0 )

    @patch( 'housemonitor.inputs.processinput.Common.send' )
    @patch( 'housemonitor.inputs.processinput.xmlDeviceConfiguration.configure' )
    def test_XBeeInput_process_invalid_port_error( self, config, send ):
        env = DataEnvelope()
        env.packet = {'source_addr_long': '\x00\x13\xa2\x00@\x90)\xbf',
                       'source_addr': '\xf9\xf2',
                        'id': 'rx_io_data_long_addr',
                         'samples': [{'adc-3': 622}],
                       'options': '\x01'}

        xd = xmlDeviceConfiguration()
        xd.devices = {'0x13a200409029bf': {'adc-0': {'cosm_channel': '3',
                                   'description': 'The temperature in the sunroom',
                                   'name': 'Indoor Temperature',
                                   'steps': ['step.ZigbeeAnalogNumberToVolts',
                                             'step.TMP_36_Volts_to_Centigrade',
                                             'step.Centigrade_to_Fahrenheit',
                                             'step.Average',
                                             'step.FormatValue',
                                             'step.CurrentValue'],
                                   'units': 'F'},
                         'adc-1': {'cosm_channel': '3',
                                   'description': 'The temperature at 100 West Lisa Drive Austin TX',
                                   'name': 'Outdoor Temperature',
                                   'steps': ['step.ZigbeeAnalogNumberToVolts',
                                             'step.TMP_36_Volts_to_Centigrade',
                                             'step.Centigrade_to_Fahrenheit',
                                             'step.Average',
                                             'step.FormatValue',
                                             'step.CurrentValue'],
                                   'units': 'F'},
                         'name': 'Sunroom',
                         'network_address': '0xf9f2'}}

        xp = ProcessXBeeInput( xd )
        xp.logger.exception = MagicMock()
        value = xp.process( env )
        xp.logger.exception.assert_called_with( "'Invalid port (adc-3)'" )
        self.assertEqual( send.call_count, 0 )

    @patch( 'housemonitor.inputs.processinput.Common.send' )
    @patch( 'housemonitor.inputs.processinput.xmlDeviceConfiguration.configure' )
    def test_XBeeInput_process_invalid_configuration_options_error( self, config, send ):
        env = DataEnvelope()
        env.packet = {'source_addr_long': '\x00\x13\xa2\x00@\x90)\xbf',
                       'source_addr': '\xf9\xf2',
                        'id': 'rx_io_data_long_addr',
                         'samples': [{'adc-0': 622}],
                       'options': '\x01'}

        xd = xmlDeviceConfiguration()
        xd.devices = {'0x13a200409029bf': {'adc-0': {'cosm_channel': '3',
                                   'description': 'The temperature in the sunroom',
                                   'name': 'Indoor Temperature',
                                   'steps': ['step.ZigbeeAnalogNumberToVolts',
                                             'step.TMP_36_Volts_to_Centigrade',
                                             'step.Centigrade_to_Fahrenheit',
                                             'step.Average',
                                             'step.FormatValue',
                                             'step.CurrentValue']},
                         'adc-1': {'cosm_channel': '3',
                                   'description': 'The temperature at 100 West Lisa Drive Austin TX',
                                   'name': 'Outdoor Temperature',
                                   'steps': ['step.ZigbeeAnalogNumberToVolts',
                                             'step.TMP_36_Volts_to_Centigrade',
                                             'step.Centigrade_to_Fahrenheit',
                                             'step.Average',
                                             'step.FormatValue',
                                             'step.CurrentValue'],
                                   'units': 'F'},
                         'name': 'Sunroom',
                         'network_address': '0xf9f2'}}

        xp = ProcessXBeeInput( xd )
        xp.logger.exception = MagicMock()
        value = xp.process( env )
        xp.logger.exception.assert_called_with( "'Required configuration option not present (units) for device(0x13a200409029bf) port (adc-0)'" )
        self.assertEqual( send.call_count, 0 )

    @patch( 'housemonitor.inputs.processinput.datetime' )
    @patch( 'housemonitor.inputs.processinput.Common.send' )
    @patch( 'housemonitor.inputs.processinput.xmlDeviceConfiguration.configure' )
    def test_XBeeInput_process_with_valid_data( self, config, send, dt ):
        env = DataEnvelope()
        test_time = datetime.datetime( 2012, 1, 2, 3, 4, 5 )
        env.packet = {'source_addr_long': '\x00\x13\xa2\x00@\x90)\xbf',
                       'source_addr': '\xf9\xf2',
                        'id': 'rx_io_data_long_addr',
                         'samples': [{'adc-1': 622}],
                       'options': '\x01'}

        xd = xmlDeviceConfiguration()
        xd.devices = self.valid_devices_configuration
        xp = ProcessXBeeInput( xd )
        dt.utcnow.return_value = 123
        xp.process( env )
        send.assert_called_once_with( 622, {'name': 'Garage Temperature', 'units': 'F', 'steps': ['step.ZigbeeAnalogNumberToVolts', 'step.TMP_36_Volts_to_Centigrade', 'step.Centigrade_to_Fahrenheit', 'step.Average', 'step.FormatValue', 'step.CurrentValue', 'step.oneInN', 'outputs.COSM'], 'at': 123, 'device': '0x13a200409029bf', 'port': 'adc-1'}, ['step.ZigbeeAnalogNumberToVolts', 'step.TMP_36_Volts_to_Centigrade', 'step.Centigrade_to_Fahrenheit', 'step.Average', 'step.FormatValue', 'step.CurrentValue', 'step.oneInN', 'outputs.COSM'] )

# ProcessStatusRequests

    def test_ProcessStatusRequests_logger_name( self ):
        devices = {'device': {'port': {}}}
        psr = ProcessStatusRequests( devices )
        self.assertEqual( psr.logger_name, Constants.LogKeys.inputs )

    @patch( 'housemonitor.inputs.processinput.Common.send' )
    def test_ProcessStatusRequests_process( self, send ):
        devices = {'device': {'port': {}}}
        env = DataEnvelope()
        env.data = {}
        env.data[Constants.DataPacket.listeners] = ['a', 'b', 'c']
        psr = ProcessStatusRequests( devices )
        psr.process( env )
        send.assert_called_once_with( 1, env.data, env.data[Constants.DataPacket.listeners] )

# ProcessInput

    @patch( 'housemonitor.inputs.processinput.xmlDeviceConfiguration.configure' )
    def testProcessInput_topic_name( self, config ):
        devices = {'device': {'port': {}}}
        pi = ProcessInput( devices )
        self.assertEqual( pi.topic_name, Constants.TopicNames.ProcessInputs )

    @patch( 'housemonitor.inputs.processinput.xmlDeviceConfiguration.configure' )
    def testProcessInput_configuration_file_name( self, config ):
        devices = {'device': {'port': {}}}
        pi = ProcessInput( devices )
        self.assertEqual( pi.configuration_file_name, 'housemonitor.inputs.processinput' )

    @patch( 'housemonitor.inputs.processinput.xmlDeviceConfiguration.configure' )
    def test_ProcessInput_logger_name( self, config ):
        devices = {'device': {'port': {}}}
        pi = ProcessInput( devices )
        self.assertEqual( pi.logger_name, Constants.LogKeys.inputs )

    @patch.object( ProcessXBeeInput, 'process' )
    @patch( 'housemonitor.inputs.processinput.xmlDeviceConfiguration.configure' )
    @patch.object( HMQueue, 'receive' )
    def test_ProcessInput_work_xbee_input( self, process, config, receive ):
        envelope = DataEnvelope( type='xbee' )
        que = HMQueue()
        pi = ProcessInput( que )
        que.receive.return_value = envelope
        pi.work()
        que.receive.assert_called_oncy_with()
        pi.commands[envelope.type].process.assert_called_once_with( envelope )

    @patch.object( ProcessStatusRequests, 'process' )
    @patch( 'housemonitor.inputs.processinput.xmlDeviceConfiguration.configure' )
    @patch.object( HMQueue, 'receive' )
    def test_ProcessInput_work_status_request( self, process, config, receive ):
        envelope = DataEnvelope( type=Constants.EnvelopeTypes.status )
        que = HMQueue()
        pi = ProcessInput( que )
        que.receive.return_value = envelope
        pi.work()
        que.receive.assert_called_oncy_with()
        pi.commands[envelope.type].process.assert_called_once_with( envelope )

    def side_effect( self ):
        self.pi.forever = False

    @patch.object( HMQueue, 'receive' )
    @patch.object( ProcessInput, 'work' )
    @patch( 'housemonitor.inputs.processinput.xmlDeviceConfiguration.configure' )
    def test_input( self, receive, work, config ):
        que = HMQueue()
        self.pi = ProcessInput( que )
        work.side_effect = self.side_effect
        self.pi.input()
        self.pi.work.assert_called_once_with()

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()    # pragma: no cover
