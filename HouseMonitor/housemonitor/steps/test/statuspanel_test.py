'''
Created on Mar 28, 2013

@author: Gary
'''
from configuration.formatconfiguration import FormatConfiguration
from datetime import datetime, timedelta
from lib.common import Common
from lib.constants import Constants
from lib.getdatetime import GetDateTime
from mock import Mock, patch, MagicMock
from pubsub import pub
from steps.statuspanel import StatusPanel, instantuate_me
import logging.config
import pprint
import unittest
import uuid


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
        self.assertEqual( N.process_delayed_alarm.logger_name, Constants.LogKeys.StatusPanel )

    def test_topic_name( self ):
        data = {}
        N = instantuate_me( data )
        self.assertEqual( N.garage_door_monitor.topic_name, Constants.TopicNames.StatusPanel_GarageDoorMonitor )
        self.assertEqual( N.process_delayed_alarm.topic_name, Constants.TopicNames.StatusPanel_ProcessDelayedAlarm )
        self.assertEqual( N.disable_alarm_button.topic_name, Constants.TopicNames.StatusPanel_DisableAlarmButton )

    @patch( 'steps.statuspanel.StatusPanel.changeGarageDoorWarningLight' )
    @patch.object( GetDateTime, 'datetime' )
    def test_first_time_with_garage_door_closed( self, dt, light ):
        data = {}
        list = ['a', 'b']
        t = datetime( 2012, 2, 2, 2, 2, 2 )
        sp = StatusPanel()
        dt.return_value = t
        sp.garage_door = sp.GARAGE_DOOR_OPEN
        sp.garage_door_monitor.step( sp.GARAGE_DOOR_CLOSED, data, list )
        self.assertEqual( sp.garage_door, sp.GARAGE_DOOR_CLOSED )
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
        sp.garage_door_monitor.step( sp.GARAGE_DOOR_OPEN, data, list )
        self.assertEqual( sp.garage_door, sp.GARAGE_DOOR_OPEN )
        self.assertEqual( sp.when_garage_door_opened, t )
        light.assert_called_once_with( sp.GARAGE_DOOR_OPEN )
        light.reset_mock()

    @patch( 'steps.statuspanel.StatusPanel.changeGarageDoorWarningLight' )
    @patch.object( GetDateTime, 'datetime' )
    def test_first_time_with_garage_door_closed_then_open_the_garage_door( self, dt, light ):
        data = {}
        list = ['a', 'b']
        t = datetime( 2012, 2, 2, 2, 2, 2 )
        sp = StatusPanel()
        dt.return_value = t
        sp.garage_door_monitor.step( sp.GARAGE_DOOR_CLOSED, data, list )
        self.assertEqual( sp.garage_door, sp.GARAGE_DOOR_CLOSED )
        light.assert_called_once_with( sp.GARAGE_DOOR_CLOSED )
        light.reset_mock()

        t = datetime( 2012, 2, 2, 2, 3, 2 )
        dt.return_value = t
        sp.garage_door_monitor.step( sp.GARAGE_DOOR_OPEN, data, list )
        self.assertFalse( sp.garage_door )
        self.assertEqual( sp.when_garage_door_opened, t )
        light.assert_called_once_with( sp.GARAGE_DOOR_OPEN )
        light.reset_mock()

        t1 = datetime( 2012, 2, 2, 2, 4, 2 )
        dt.return_value = t1
        sp.garage_door_monitor.step( sp.GARAGE_DOOR_OPEN, data, list )
        self.assertFalse( sp.garage_door )
        self.assertEqual( sp.when_garage_door_opened, t )
        self.assertEqual( t1 - sp.when_garage_door_opened, timedelta( 0, 60 ) )
        light.assert_called_once_with( sp.GARAGE_DOOR_OPEN )
        light.reset_mock()

        t2 = datetime( 2012, 2, 2, 2, 4, 2 )
        dt.return_value = t2
        sp.garage_door_monitor.step( sp.GARAGE_DOOR_CLOSED, data, list )
        self.assertTrue( sp.garage_door )
        self.assertIsNone( sp.when_garage_door_opened )
        light.assert_called_once_with( sp.GARAGE_DOOR_CLOSED )


#################################################
#  change Garage Door Warning Light
#################################################
    @patch( 'steps.statuspanel.Common.send' )
    def test_change_Garage_Door_light_to_open( self, send ):
        data = {}
        listeners = [Constants.TopicNames.ZigBeeOutput]
        sp = StatusPanel()
        send.reset_mock()
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
#        send.assert_called_once_with( sp.ALARM_ON , {'device': '0x13a20040902a02', 'port': 'DIO-3'}, ['step.ZigBeeOutput' ] )

#################################################
#  change alarm
#################################################
    @patch( 'steps.statuspanel.StatusPanel.changeAlarm' )
    def test_press_disarm_alarm_button( self, ca ):
        data = {}
        listeners = [Constants.TopicNames.ZigBeeOutput]
        sp = StatusPanel()
        ca.reset_mock()
        sp.disable_alarm_button.step( sp.DISABLE_ALARM_BUTTON_PRESSED, data, listeners )
        self.assertEqual( sp.disenable_alarm_button_pressed, sp.DISABLE_ALARM_BUTTON_PRESSED )
        self.assertEqual( sp.alarm, sp.ALARM_OFF )
        ca.assert_called_once_with( sp.ALARM_OFF )

#################################################
#  Process Delayed Alarm
#################################################
    @patch( 'steps.statuspanel.StatusPanel.changeAlarm' )
    @patch( 'steps.statuspanel.StatusPanel.ProcessDelayedAlarm.activateTimer' )
    def test_process_delayed_alarm( self, at, ca ):
        uu = uuid.uuid4()
        data = {Constants.DataPacket.scheduler_id: uu}
        listeners = []
        sp = StatusPanel()
        ca.reset_mock()
        self.assertEqual( sp.process_delayed_alarm.topic_name, Constants.TopicNames.StatusPanel_ProcessDelayedAlarm )

        sp.process_delayed_alarm.delayedAlarmState = sp.process_delayed_alarm.PreAlarm
        sp.garage_door = sp.GARAGE_DOOR_OPEN
        sp.disenable_alarm_button_pressed = sp.ENABLE_ALARM
        sp.long_scheduler_id = uu

        sp.process_delayed_alarm.step( 1, data, listeners )

        at.assert_called_once_with( 2 )
        ca.assert_called_once_with( sp.ALARM_ON )
        self.assertEqual( sp.process_delayed_alarm.delayedAlarmState, sp.process_delayed_alarm.Short_Beep )
        at.reset_mock()
        ca.reset_mock()

        # Test transition from Shout_Beep to Long_silence
        sp.garage_door = sp.GARAGE_DOOR_OPEN
        sp.disenable_alarm_button_pressed = sp.ENABLE_ALARM

        sp.process_delayed_alarm.step( 1, data, listeners )

        at.assert_called_once_with( sp.garage_door_long_silence )
        ca.assert_called_once_with( sp.ALARM_OFF )
        self.assertEqual( sp.process_delayed_alarm.delayedAlarmState, sp.process_delayed_alarm.Long_Silence )
        at.reset_mock()
        ca.reset_mock()

        # Test transition from Long_silence back to Short_Beep
        sp.garage_door = sp.GARAGE_DOOR_OPEN
        sp.disenable_alarm_button_pressed = sp.ENABLE_ALARM

        sp.process_delayed_alarm.step( 1, data, listeners )

        at.assert_called_once_with( sp.garage_door_short_alarm )
        ca.assert_called_once_with( sp.ALARM_ON )
        self.assertEqual( sp.process_delayed_alarm.delayedAlarmState, sp.process_delayed_alarm.Short_Beep )
        at.reset_mock()
        ca.reset_mock()

        # Test transition from Long_silence back to Disabled
        sp.garage_door = sp.GARAGE_DOOR_CLOSED
        sp.disenable_alarm_button_pressed = sp.ENABLE_ALARM

        sp.process_delayed_alarm.step( 1, data, listeners )

        self.assertEqual( sp.process_delayed_alarm.delayedAlarmState, sp.process_delayed_alarm.Disabled )
        at.reset_mock()
        ca.reset_mock()

    @patch.object( uuid, 'uuid4' )
    @patch.object( pub, "sendMessage" )
    def test_process_delayed_alarm_activeTimer( self, sm, u ):
        sp = StatusPanel()
        delay = 2
        value = 4
        sm.reset_mock()
        listeners = [Constants.TopicNames.StatusPanel_ProcessDelayedAlarm]
        u.return_value = value
        args = sp.panel_address, sp.panel_alarm, listeners, value
        sp.process_delayed_alarm.activateTimer( delay )
        # TODO: Fix me
#         sm.assert_called_once_with( Constants.TopicNames.SchedulerAddOneShotStep,
#                             name='garage door delayed alarm',
#                             delta=timedelta( seconds=delay ),
#                             args=args )

    @patch.object( StatusPanel, 'changeAlarm' )
    def test_process_when_disable_alarm_button_pressed( self, ca ):
        uu = uuid.uuid4()
        data = {Constants.DataPacket.scheduler_id: uu}
        listeners = [Constants.TopicNames.ZigBeeOutput]
        sp = StatusPanel()
        ca.reset_mock()
        sp.garage_door = sp.GARAGE_DOOR_OPEN
        sp.long_scheduler_id = uu
        sp.disenable_alarm_button_pressed = sp.DISABLE_ALARM_BUTTON_PRESSED
        sp.process_delayed_alarm.step( 1, data, listeners )
        self.assertEqual( sp.process_delayed_alarm.delayedAlarmState, sp.process_delayed_alarm.Disabled )
        ca.assert_called_once_with( sp.ALARM_OFF )

    @patch.object( StatusPanel, 'changeAlarm' )
    def test_process_when_disable_alarm_button_pressed_but_invalid_state( self, ca ):
        uu = uuid.uuid4()
        data = {Constants.DataPacket.scheduler_id: uu}
        invalid_state = 10
        listeners = [Constants.TopicNames.ZigBeeOutput]
        sp = StatusPanel()
        sp.long_scheduler_id = uu
        ca.reset_mock()
        sp.garage_door = sp.GARAGE_DOOR_OPEN
        sp.disenable_alarm_button_pressed = sp.DISABLE_ALARM_BUTTON_NOT_PRESSED
        sp.process_delayed_alarm.delayedAlarmState = invalid_state

        sp.process_delayed_alarm.step( 1, data, listeners )

        ca.assert_called_once_with( sp.ALARM_OFF )

################################################
# Silence Alarm
################################################
    @patch.object( StatusPanel, 'changeAlarm' )
    def test_SilenceAlarm( self, ca ):
        uu = uuid.uuid4()
        data = {Constants.DataPacket.scheduler_id: uu}
        listeners = [Constants.TopicNames.ZigBeeOutput]
        sp = StatusPanel()
        sp.short_scheduler_id = uu
        ca.reset_mock()
        value = True

        value_returned, data_returned, listeners_returned = sp.silence_alarm.step( value, data, listeners )
        ca.assert_called_once_with( sp.ALARM_OFF )

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
