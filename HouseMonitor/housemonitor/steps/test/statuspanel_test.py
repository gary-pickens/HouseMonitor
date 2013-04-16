'''
Created on Mar 28, 2013

@author: Gary
'''
import unittest
from datetime import datetime
from datetime import timedelta
from steps.statuspanel import StatusPanel
from steps.statuspanel import instantuate_me
from lib.common import Common
import logging.config
from lib.constants import Constants
import pprint
from mock import Mock, patch
from lib.getdatetime import GetDateTime
from configuration.formatconfiguration import FormatConfiguration
from pubsub import pub


class Test( unittest.TestCase ):
    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "house_monitor_logging.conf" )

    def tearDown( self ):
        pass

    def test_instantuate_me( self ):
        data = {}
        N = instantuate_me( data )
        self.assertIsInstance( N, StatusPanel )
        self.assertIsInstance( N.garage_door_monitor, StatusPanel.GarageDoorMonitor )

    def test_logger_name( self ):
        data = {}
        N = instantuate_me( data )
        self.assertEqual( N.logger_name, Constants.LogKeys.StatusPanel )
        self.assertEqual( N.garage_door_monitor.logger_name, Constants.LogKeys.StatusPanel )
        self.assertEqual( N.start_alarm.logger_name, Constants.LogKeys.StatusPanel )

    def test_topic_name( self ):
        data = {}
        N = instantuate_me( data )
        self.assertEqual( N.garage_door_monitor.topic_name, Constants.TopicNames.StatusPanel_GarageDoorMonitor )
        self.assertEqual( N.start_alarm.topic_name, Constants.TopicNames.StatusPanel_StartAlarm )
        self.assertEqual( N.disable_alarm_button.topic_name, Constants.TopicNames.StatusPanel_DisableAlarmButton )

    @patch( 'steps.statuspanel.StatusPanel.changeGarageDoorWarningLight' )
    @patch.object( GetDateTime, 'datetime' )
    def test_first_time_with_garage_door_closed( self, dt, light ):
        data = {}
        list = ['a', 'b']
        t = datetime( 2012, 2, 2, 2, 2, 2 )
        sp = StatusPanel()
        dt.return_value = t
        sp.garage_door_monitor.step( sp.GARAGE_DOOR_CLOSED, data, list )
        self.assertTrue( sp.garage_door )
#        self.assertEqual( sp.when_garage_door_opened, t )
        light.assert_called_once_with( sp.GARAGE_DOOR_CLOSED )
        light.reset_mock()


    @patch( 'steps.statuspanel.StatusPanel.changeGarageDoorWarningLight' )
    @patch.object( GetDateTime, 'datetime' )
    def test_first_time_with_garage_door_open( self, dt, light ):
        data = {}
        list = ['a', 'b']
        t = datetime( 2012, 2, 2, 2, 2, 2 )
        sp = StatusPanel()
        dt.return_value = t
#         sp.garage_door_monitor.step( sp.GARAGE_DOOR_OPEN, data, list )
#         self.assertFalse( sp.garage_door )
#         self.assertEqual( sp.when_garage_door_opened, t )
#         light.assert_called_once_with( sp.GARAGE_DOOR_OPEN )
#         light.reset_mock()

    @patch( 'steps.statuspanel.StatusPanel.changeGarageDoorWarningLight' )
    @patch.object( GetDateTime, 'datetime' )
    def test_first_time_with_garage_door_closed_then_open_the_garage_door( self, dt, light ):
        data = {}
        list = ['a', 'b']
        t = datetime( 2012, 2, 2, 2, 2, 2 )
        sp = StatusPanel()
        dt.return_value = t
        sp.garage_door_monitor.step( sp.GARAGE_DOOR_CLOSED, data, list )
        self.assertTrue( sp.garage_door )
#        self.assertEqual( sp.when_garage_door_opened, t )
        light.assert_called_once_with( sp.GARAGE_DOOR_CLOSED )
        light.reset_mock()

        t = datetime( 2012, 2, 2, 2, 3, 2 )
        dt.return_value = t
#        sp.garage_door_monitor.step( sp.GARAGE_DOOR_OPEN, data, list )
#        self.assertFalse( sp.garage_door )
#         self.assertEqual( sp.when_garage_door_opened, t )
#         light.assert_called_once_with( sp.GARAGE_DOOR_OPEN )
#         light.reset_mock()

#         t1 = datetime( 2012, 2, 2, 2, 4, 2 )
#         dt.return_value = t1
#         sp.garage_door_monitor.step( sp.GARAGE_DOOR_OPEN, data, list )
#         self.assertFalse( sp.garage_door )
#         self.assertEqual( sp.when_garage_door_opened, t )
#         self.assertEqual( t1 - sp.when_garage_door_opened, timedelta( 0, 60 ) )
#         light.assert_called_once_with( sp.GARAGE_DOOR_OPEN )
#         light.reset_mock()
#
#         t2 = datetime( 2012, 2, 2, 2, 4, 2 )
#         dt.return_value = t2
#         sp.garage_door_monitor.step( sp.GARAGE_DOOR_CLOSED, data, list )
#         self.assertTrue( sp.garage_door )
#         self.assertIsNone( sp.when_garage_door_opened )
#         light.assert_called_once_with( sp.GARAGE_DOOR_CLOSED )

#################################################
#  Disable Alarm Button
#################################################

    @patch( 'steps.statuspanel.StatusPanel.changeAlarm' )
    def test_start_alarm_with_door_open_and_not_disabled( self, change ):
        data = {}
        list = ['a', 'b']
        sp = StatusPanel()
        sp.garage_door = sp.GARAGE_DOOR_OPEN
        sp.enable_alarm_button_pressed = sp.ENABLE_ALARM
        sp.start_alarm.step( sp.ALARM_ON, data, list )
        self.assertEqual( sp.alarm, sp.ALARM_ON )
        change.assert_called_once_with( sp.ALARM_ON )
        change.reset_mock()

    @patch( 'steps.statuspanel.StatusPanel.changeAlarm' )
    def test_start_alarm_with_door_open_and_disabled( self, change ):
        data = {}
        list = ['a', 'b']
        sp = StatusPanel()
        sp.garage_door = sp.GARAGE_DOOR_OPEN
        sp.alarm_disabled = sp.DISABLE_ALARM
        sp.start_alarm.step( sp.ALARM_ON, data, list )
        self.assertEqual( sp.alarm, sp.ALARM_OFF )

    @patch( 'steps.statuspanel.StatusPanel.changeAlarm' )
    def test_start_alarm_with_door_closed_and_disabled( self, change ):
        data = {}
        list = ['a', 'b']
        sp = StatusPanel()
        sp.garage_door = sp.GARAGE_DOOR_CLOSED
        sp.alarm_disabled = sp.DISABLE_ALARM
        sp.start_alarm.step( sp.ALARM_ON, data, list )
        self.assertEqual( sp.alarm, sp.ALARM_OFF )

#################################################
#  change Garage Door Warning Light
#################################################
    @patch( 'steps.statuspanel.Common.send' )
    def test_change_Garage_Door_light_to_open( self, send ):
        data = {}
        listeners = [Constants.TopicNames.ZigBeeOutput]
        sp = StatusPanel()
        sp.changeGarageDoorWarningLight( sp.GARAGE_DOOR_OPEN )
        send.assert_called_once_with( not sp.GARAGE_DOOR_OPEN , {'device': '0x13a20040902a02', 'port': 'DIO-1'}, ['step.ZigBeeOutput'] )

#################################################
#  change alarm
#################################################
    @patch( 'steps.statuspanel.Common.send' )
    def test_change_alarm_to_on( self, send ):
        data = {}
        listeners = [Constants.TopicNames.ZigBeeOutput]
        sp = StatusPanel()
        sp.changeAlarm( sp.ALARM_ON )
        send.assert_called_once_with( sp.ALARM_ON , {'device': '0x13a20040902a02', 'port': 'DIO-3'}, ['step.ZigBeeOutput' ] )

#################################################
#  change alarm
#################################################
    @patch( 'steps.statuspanel.StatusPanel.changeAlarm' )
    def test_press_disarm_alarm_button( self, ca ):
        data = {}
        listeners = [Constants.TopicNames.ZigBeeOutput]
        sp = StatusPanel()
        sp.disable_alarm_button.step( True, data, listeners )
        self.assertEqual( sp.enable_alarm_button_pressed, sp.DISABLE_ALARM )
        self.assertEqual( sp.alarm, sp.ALARM_OFF )
# TODO: Fix ME
#        ca.assert_called_once_with( sp.ALARM_OFF )

#################################################
#  System Check
#################################################

    def test_SystemCheck( self ):
        data = {}
        listeners = [Constants.TopicNames.ZigBeeOutput]
        sp = StatusPanel()
        value = True
        self.assertEqual( sp.system_check.logger_name, Constants.LogKeys.StatusPanel )
        self.assertEqual( sp.system_check.topic_name, Constants.TopicNames.StatusPanel_SystemCheck )
        sp.system_check.toggle = False

        value_returned, data_returned, listeners_returned = sp.system_check.step( value, data, listeners )
        self.assertTrue( value_returned )
        self.assertDictEqual( data, data_returned )
        self.assertListEqual( listeners, listeners_returned )

        value_returned, data_returned, listeners_returned = sp.system_check.step( value, data, listeners )
        self.assertFalse( value_returned )
        self.assertDictEqual( data, data_returned )
        self.assertListEqual( listeners, listeners_returned )




if __name__ == "__main__":
    #  import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
