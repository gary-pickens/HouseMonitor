'''
Created on 2012-11-14

@author: Gary

'''
from lib.constants import Constants
from configuration.formatconfiguration import FormatConfiguration
from abc_step import abcStep
from lib.common import Common
from lib.base import Base
from datetime import datetime
from datetime import timedelta
from lib.getdatetime import GetDateTime
from pubsub import pub


def instantuate_me( data ):
    ''' This function will be called to instantiate this class. '''
    return StatusPanel()


class StatusPanel( Base ):
    '''
    This panel is responsible for updating the status panel whose schematic is in the Fritzing directory.
    '''

    panel_address = '0x13a20040902a02'
    panel_status_led = 'DIO-0'
    panel_garage_door_led = 'DIO-1'
    panel_spare_led = 'DIO-2'
    panel_alarm = 'DIO-3'
    panel_disable = 'DIO-5'

    #  Classes
    garage_door_monitor = None
    start_alarm = None
    disable_alarm_button = None
    system_check = None

    #  Constants used to describe the state of various items
    GARAGE_DOOR_OPEN = False
    GARAGE_DOOR_CLOSED = True

    ALARM_OFF = True
    ALARM_ON = False

    ENABLE_ALARM = True
    DISABLE_ALARM = False

    #  items that are tracked
    alarm = ALARM_OFF
    ''' Weather the alarm is sounding or not '''

    garage_door = GARAGE_DOOR_CLOSED
    ''' The state of the garage door. '''

    when_garage_door_opened = None
    ''' The time when the garage door was opened '''

    garage_door_timer = None
    ''' Contains the time that the garage door was opened '''

    enable_alarm_button_pressed = False
    ''' Indicates that the disable alarm has been pressed.  Cleared by closing the door. '''

    ''' The time from when the garage door opens to the time the alarm starts sounding '''
    #  TODO: Increase this back after test
    garage_door_standoff_time = timedelta( minutes=1 )

    def __init__( self ):
        '''
        '''
        super( StatusPanel, self ).__init__()
        self.garage_door_monitor = self.GarageDoorMonitor( self )
        self.start_alarm = self.StartAlarm( self )
        self.disable_alarm_button = self.DisableAlarmButton( self )
        self.system_check = self.SystemCheck( self )

    @property
    def logger_name( self ):
        ''' Set the logger level. '''
        return Constants.LogKeys.StatusPanel

    def changeGarageDoorWarningLight( self, value ):
        ''' Turn on or off the LED that indicates that the garage door is open. '''
        steps = [Constants.TopicNames.ZigBeeOutput]
        data = {}
        data[Constants.DataPacket.device] = self.panel_address
        data[Constants.DataPacket.port] = self.panel_garage_door_led
        light = not value
        self.logger.debug( "changeGarageDoorWarningLight with {} {} {}".format( value, data, steps ) )
        Common.send( light, data, steps )

    def changeAlarm( self, value ):
        ''' Turn on or off the alarm that indicates that the garage door is open. '''
        steps = [Constants.TopicNames.ZigBeeOutput]
        data = {}
        data[Constants.DataPacket.device] = self.panel_address
        data[Constants.DataPacket.port] = self.panel_alarm
        self.logger.debug( "changeAlarm with {} {} {}".format( value, data, steps ) )
        Common.send( value, data, steps )

    class GarageDoorMonitor( abcStep ):

        def __init__( self, status_panel ):
            '''
            '''
            super( StatusPanel.GarageDoorMonitor, self ).__init__()
            self.status_panel = status_panel

        @property
        def logger_name( self ):
            ''' Set the logger level. '''
            return Constants.LogKeys.StatusPanel

        @property
        def topic_name( self ):
            ''' The topic name to which this routine subscribes.'''
            return Constants.TopicNames.StatusPanel_GarageDoorMonitor

        def setTimerToActivateAlarmAfterInterval( self ):
            listeners = [Constants.TopicNames.StatusPanel_StartAlarm]
            args = self.status_panel.panel_address, self.status_panel.panel_status_led, listeners
            pub.sendMessage( Constants.TopicNames.SchedulerAddOneShotStep,
                            name='garage door alarm',
                            delta=self.status_panel.garage_door_standoff_time,
                            args=args )
            self.logger.debug( 'Activate garage door timer' )

        def step( self, value, data={}, listeners=[] ):
            """
            Will detect if the garage door has been opened.  If it has it will:
                | 1. Set the time when the door was opened
                | 2. disable the alarm
                | 3. Turn off the alarm
            
            It will always do the following:
                | 1. Set the garage door to the value that was passed in
                | 2. Start a timer that will send a message in X minutes telling the system
                | to recheck the garage door and if it is still open start the alarm.
                
            :param value: The state of the garage door
            :type value: Boolean
            :param data: a dictionary containing more information about the
                    value. Data can be added to this as needed.  Here is a list
                    of values that will be in the data dictionary:
    
                   | 1. **date:** time received: time when value was received.
                   | 2. **units:** units of the number
                   | 3. **name:** name assigned to the value
                   | 4. etc.
            :param listeners: a list of the subscribed routines to send the data to
            :returns: value, data, listeners
            :rtype: Boolean, dict, listeners
            Raises:
                None
    
            """
            self.logger.debug( 'GarageDoorMonitor. {} {}'.format( self.status_panel.garage_door, value ) )
            if self.status_panel.garage_door == self.status_panel.GARAGE_DOOR_CLOSED and value == self.status_panel.GARAGE_DOOR_OPEN:
                self.status_panel.when_garage_door_opened = GetDateTime().datetime()
                self.status_panel.enable_alarm_button_pressed = self.status_panel.DISABLE_ALARM
                self.status_panel.changeAlarm( self.status_panel.ALARM_OFF )
                self.setTimerToActivateAlarmAfterInterval()
            self.status_panel.garage_door = value
            self.status_panel.changeGarageDoorWarningLight( value )
            self.logger.debug( 'After GarageDoorMonitor.step {} {}'.format( self.status_panel.when_garage_door_opened, self.status_panel.enable_alarm_button_pressed ) )
            return value, data, listeners

    class DisableAlarmButton( abcStep ):

        def __init__( self, status_panel ):
            '''
            '''
            super( StatusPanel.DisableAlarmButton, self ).__init__()
            self.status_panel = status_panel

        @property
        def logger_name( self ):
            ''' Set the logger level. '''
            return Constants.LogKeys.StatusPanel

        @property
        def topic_name( self ):
            ''' The topic name to which this routine subscribes.'''
            return Constants.TopicNames.StatusPanel_DisableAlarmButton

        def step( self, value, data={}, listeners=[] ):
            """
            Will detect if the garage door disable button has been pressed.  If it has it will:
                | 1. set disable alarm to disabled
                | 2. turn off the alarm
                        
            :param value: The state of the garage door
            :type value: Boolean
            :param data: a dictionary containing more information about the
                    value. Data can be added to this as needed.  Here is a list
                    of values that will be in the data dictionary:
    
                   | 1. **date:** time received: time when value was received.
                   | 2. **units:** units of the number
                   | 3. **name:** name assigned to the value
                   | 4. etc.
            :param listeners: a list of the subscribed routines to send the data to
            :returns: value, data, listeners
            :rtype: Boolean, dict, listeners
            Raises:
                None
    
            """
            #  set when_garage_door_opened the first time the door is detected open
            self.status_panel.enable_alarm_button_pressed = self.status_panel.DISABLE_ALARM
            self.status_panel.changeAlarm( self.status_panel.ALARM_OFF )
            self.status_panel.alarm = self.status_panel.ALARM_OFF
            self.logger.debug( 'Disable alarm. {} {}'.format( self.status_panel.enable_alarm_button_pressed, self.status_panel.alarm ) )
            return value, data, listeners

    class StartAlarm( abcStep ):

        def __init__( self, status_panel ):
            '''
            '''
            super( StatusPanel.StartAlarm, self ).__init__()
            self.status_panel = status_panel

        @property
        def logger_name( self ):
            ''' Set the logger level. '''
            return Constants.LogKeys.StatusPanel

        @property
        def topic_name( self ):
            ''' The topic name to which this routine subscribes.'''
            return Constants.TopicNames.StatusPanel_StartAlarm

        def step( self, value, data={}, listeners=[] ):
            """
            This routine will receive a message X minutes after the door has been opened.  If the garage door is 
            still open and the alarm has not been disabled, it will start the alarm:
                | 1. set disable alarm to disabled
                | 2. turn off the alarm
                        
            :param value: Not used
            :type value: Boolean
            :param data: a dictionary containing more information about the
                    value. Data can be added to this as needed.  Here is a list
                    of values that will be in the data dictionary:
    
                   | 1. **date:** time received: time when value was received.
                   | 2. **units:** units of the number
                   | 3. **name:** name assigned to the value
                   | 4. etc.
            :param listeners: a list of the subscribed routines to send the data to
            :returns: value, data, listeners
            :rtype: Boolean, dict, listeners
            Raises:
                None
    
            """
            self.logger.debug( 'Start alarm called. {} {}'.format( self.status_panel.garage_door, self.status_panel.enable_alarm_button_pressed ) )
            #  Test to see if the alarm needs to be activated:
            #  1. Is the garage door open
            #  2. Has the disable button been pressed
            if ( self.status_panel.garage_door == self.status_panel.GARAGE_DOOR_OPEN and
                 self.status_panel.enable_alarm_button_pressed == self.status_panel.ENABLE_ALARM ):
                self.status_panel.changeAlarm( self.status_panel.ALARM_ON )
                self.status_panel.alarm = self.status_panel.ALARM_ON
                self.logger.debug( 'Start alarm. {}'.format( self.status_panel.alarm ) )
            return value, data, listeners

    class SystemCheck( abcStep ):

        toggle = True

        def __init__( self, status_panel ):
            '''
            '''
            super( StatusPanel.SystemCheck, self ).__init__()
            self.status_panel = status_panel

        @property
        def logger_name( self ):
            ''' Set the logger level. '''
            return Constants.LogKeys.StatusPanel

        @property
        def topic_name( self ):
            ''' The topic name to which this routine subscribes.'''
            return Constants.TopicNames.StatusPanel_SystemCheck

        def step( self, value, data={}, listeners=[] ):
            """
             This routine will monitor the status of the HouseMonitor program and if everything appears ok
             will toggle the Status LED.
             
            :param value: Not used
            :type value: Boolean
            :param data: a dictionary containing more information about the
                    value. Data can be added to this as needed.  Here is a list
                    of values that will be in the data dictionary:
    
                   | 1. **date:** time received: time when value was received.
                   | 2. **units:** units of the number
                   | 3. **name:** name assigned to the value
                   | 4. etc.
            :param listeners: a list of the subscribed routines to send the data to
            :returns: value, data, listeners
            :rtype: Boolean, dict, listeners
            Raises:
                None
    
            """
            value = self.toggle = not self.toggle
            self.logger.debug( 'System Check called. {}'.format( self.toggle ) )
            return value, data, listeners
