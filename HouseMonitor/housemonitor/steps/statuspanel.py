'''
Created on 2012-11-14

@author: Gary

'''
from lib.constants import Constants
from abc_step import abcStep
from lib.common import Common
from lib.base import Base
from datetime import timedelta
from lib.getdatetime import GetDateTime
from pubsub import pub
import time
import thread



def instantuate_me( data ):
    ''' This function will be called to instantiate this class. '''
    return StatusPanel()


class StatusPanel( Base ):
    '''
    The Status Panel is responsible for updating the kitchen status panel.  The status panel
    consists for a:
    
    # Green flashing LED that indicates that the system is functioning.
    # A red LED that glows when the garage door is open.
    # A alarm that will sound X minutes after the garage door has opened.
    # A disable button that will disable the alarm.
    
    A schematic is in the Fritzing directory.
    '''

    panel_address = '0x13a20040902a02'
    panel_status_led = 'DIO-0'
    panel_garage_door_led = 'DIO-1'
    panel_spare_led = 'DIO-2'
    panel_alarm = 'DIO-3'
    panel_disable = 'DIO-4'

    #  Classes
    garage_door_monitor = None
    process_delayed_alarm = None
    disable_alarm_button = None
    system_check = None
    silence_alarm = None

    #  Constants used to describe the state of various items
    GARAGE_DOOR_OPEN = False
    GARAGE_DOOR_CLOSED = True

    ALARM_OFF = False
    ALARM_ON = True

    ENABLE_ALARM = True
    DISABLE_ALARM = False

    DISABLE_ALARM_BUTTON_PRESSED = False
    DISABLE_ALARM_BUTTON_NOT_PRESSED = True

    status_panel_update_rate = 2

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
    ''' Indicates that the disable alarm has been pressed.  
    Cleared by closing the door. '''

    ''' The time from when the garage door opens to the time the alarm 
    starts sounding '''
    #  TODO: Increase this back after test
    garage_door_standoff_time = timedelta( minutes=15 )
    garage_door_initial_beep_time = timedelta( seconds=2 )
    garage_door_long_silence = 8
    garage_door_short_alarm = 2

    def __init__( self ):
        '''
        '''
        super( StatusPanel, self ).__init__()
        self.garage_door_monitor = self.GarageDoorMonitor( self )
        self.process_delayed_alarm = self.ProcessDelayedAlarm( self )
        self.disable_alarm_button = self.DisableAlarmButton( self )
        self.system_check = self.SystemCheck( self )
        self.silence_alarm = self.SilenceAlarm( self )

#         listeners = [ Constants.TopicNames.StatusPanel_SystemCheck, Constants.TopicNames.ZigBeeOutput]
#         args = self.panel_address, self.panel_status_led, listeners
#         pub.sendMessage( Constants.TopicNames.SchedulerAddIntervalStep,
#                             name='status panel status',
#                             seconds=self.status_panel_update_rate,
#                             args=args )


    @property
    def logger_name( self ):
        ''' Set the logger level. '''
        return Constants.LogKeys.StatusPanel

    def changeGarageDoorWarningLight( self, value ):
        ''' Turn on or off the LED that indicates that the garage door is open. 
        
        :param value: determines if the light will be on or off.
        :type value: Boolean
        :returns: none
        
        '''
        steps = [Constants.TopicNames.ZigBeeOutput]
        data = {}
        data[Constants.DataPacket.device] = self.panel_address
        data[Constants.DataPacket.port] = self.panel_garage_door_led
        light = not value
        self.logger.debug( "changeGarageDoorWarningLight with {} {} {}".format( value, data, steps ) )
        Common.send( light, data, steps )

    def changeAlarm( self, value ):
        ''' Turn on or off the alarm that indicates that the garage door is open.         

        :param value: determines if the alarm will be on or off.
        :type value: Boolean
        :returns: none

        '''
        steps = [Constants.TopicNames.ZigBeeOutput]
        data = {}
        data[Constants.DataPacket.device] = self.panel_address
        data[Constants.DataPacket.port] = self.panel_alarm
        self.logger.debug( "changeAlarm with {} {} {}".format( value, data, steps ) )
        Common.send( value, data, steps )

    class GarageDoorMonitor( abcStep ):
        ''' GarageDoorMonitor is a class that receives the message about 
        the garage door.
        '''

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
            '''
            This will start a timer when the garage door opens.  When the 
            timer expire a message will be sent to ProcessDelayedAlarm.step() which will 
            start the alarm. 
            '''
            listeners = [Constants.TopicNames.StatusPanel_ProcessDelayedAlarm]
            args = self.status_panel.panel_address, self.status_panel.panel_alarm, listeners
            pub.sendMessage( Constants.TopicNames.SchedulerAddOneShotStep,
                            name='garage door delayed alarm',
                            delta=self.status_panel.garage_door_standoff_time,
                            args=args )
            self.logger.debug( 'Activate garage door timer' )

        def turnOffAlarmAfterInterval( self ):
            '''
            This will start a timer when the garage door opens.  When the 
            timer expire a message will be sent to ProcessDelayedAlarm.step() which will 
            start the alarm. 
            '''
            listeners = [Constants.TopicNames.StatusPanel_SilenceAlarm]
            args = self.status_panel.panel_address, self.status_panel.panel_alarm, listeners
            pub.sendMessage( Constants.TopicNames.SchedulerAddOneShotStep,
                            name='turn off garage door alarm',
                            delta=self.status_panel.garage_door_initial_beep_time,
                            args=args )
            self.logger.debug( 'Turn off alarm after {}'.format( self.status_panel.garage_door_initial_beep_time ) )

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
            :param data: a dictionary containing more information about the value.
            :param listeners: a list of the subscribed routines to send the data to
            :returns: value, data, listeners
            :rtype: Boolean, dict, listeners
    
            """
            self.logger.debug( 'Garage door is  {}'.format( "closed" if value else "open" ) )
            if self.status_panel.garage_door == self.status_panel.GARAGE_DOOR_CLOSED and value == self.status_panel.GARAGE_DOOR_OPEN:

                self.status_panel.when_garage_door_opened = GetDateTime().datetime()
                self.status_panel.enable_alarm_button_pressed = self.status_panel.DISABLE_ALARM
                self.status_panel.changeAlarm( self.status_panel.ALARM_ON )
                self.turnOffAlarmAfterInterval()
                self.setTimerToActivateAlarmAfterInterval()
                self.status_panel.process_delayed_alarm.delayedAlarmState = self.status_panel.process_delayed_alarm.PreAlarm

            if value == self.status_panel.GARAGE_DOOR_CLOSED:
                self.status_panel.when_garage_door_opened = None
                self.status_panel.enable_alarm_button_pressed = self.status_panel.DISABLE_ALARM
                self.logger.debug( 'GarageDoorMonitor. closed thread_id = {}'.format( thread.get_ident() ) )

            self.status_panel.garage_door = value
            self.status_panel.changeGarageDoorWarningLight( value )
            self.logger.debug( 'GarageDoorMonitor.step called. garage_door [{}] button_pressed [{}]'.
                format( "closed" if self.status_panel.garage_door else 'open',
                        "pressed" if self.status_panel.enable_alarm_button_pressed else "not pressed" ) )
            self.logger.debug( 'GarageDoorMonitor. delayedAlarmState = {}'.format( self.status_panel.process_delayed_alarm.delayedAlarmState ) )
            return value, data, listeners

    class SilenceAlarm( abcStep ):
        '''
        When the garage door first opens a alarm will sound for about two seconds.  This class 
        will turn the alarm off.  This class will be activated by calling sendMessage specifing the 
        amount af time for the alarm to sound.  This is done in the turnOffAlarmAfterInterval 
        call above.
        '''

        def __init__( self, status_panel ):
            '''
            '''
            super( StatusPanel.SilenceAlarm, self ).__init__()
            self.status_panel = status_panel

        @property
        def logger_name( self ):
            ''' Set the logger level. '''
            return Constants.LogKeys.StatusPanel

        @property
        def topic_name( self ):
            ''' The topic name to which this routine subscribes.'''
            return Constants.TopicNames.StatusPanel_SilenceAlarm

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
    
            """
            self.logger.debug( 'Silence alarm. value = {} thread_id = {}'.format( value, thread.get_ident() ) )
            self.status_panel.changeAlarm( self.status_panel.ALARM_OFF )
            return value, data, listeners

    class DisableAlarmButton( abcStep ):
        '''
        DisableAlarmButton will be waiting for the disable alarm button to
        be pressed.  When it is pressed it will disable the alarm until
        the garage door is closed.
        '''

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
    
            """
            self.logger.debug( 'Disable alarm. value = {}'.format( value ) )
            # TODO: fixme
#             if ( value == self.status_panel.DISABLE_ALARM_BUTTON_PRESSED ):
#                 self.status_panel.enable_alarm_button_pressed = self.status_panel.DISABLE_ALARM
#                 self.status_panel.changeAlarm( self.status_panel.ALARM_OFF )
#                 self.status_panel.alarm = self.status_panel.ALARM_OFF
#                 self.logger.warn( 'Disable alarm. {} {}'.format( self.status_panel.enable_alarm_button_pressed, self.status_panel.alarm ) )
            return value, data, listeners

    class ProcessDelayedAlarm( abcStep ):
        '''
        If the door has been open for an extended period, ProcessDelayedAlarm will start the alarm.  It will sound until the garage door
        is closed or the disable alarm button is pressed.
        '''
        def __init__( self, status_panel ):
            '''
            '''
            super( StatusPanel.ProcessDelayedAlarm, self ).__init__()
            self.status_panel = status_panel

        @property
        def logger_name( self ):
            ''' Set the logger level. '''
            return Constants.LogKeys.StatusPanel

        @property
        def topic_name( self ):
            ''' The topic name to which this routine subscribes.'''
            return Constants.TopicNames.StatusPanel_ProcessDelayedAlarm

        ''' Delayed alarm states '''
        Disabled = 0
        PreAlarm = 1
        Short_Beep = 2
        Long_Silence = 3
        delayedAlarmState = Disabled;

        def activateTimer( self, seconds ):
            '''
            This will start a timer when the garage door opens.  When the 
            timer expire a message will be sent to ProcessDelayedAlarm.step() which will 
            start the alarm. 
            '''
            listeners = [Constants.TopicNames.StatusPanel_ProcessDelayedAlarm]
            args = self.status_panel.panel_address, self.status_panel.panel_alarm, listeners
            pub.sendMessage( Constants.TopicNames.SchedulerAddOneShotStep,
                            name='garage door delayed alarm',
                            delta=timedelta( seconds=seconds ),
                            args=args )
            self.logger.debug( 'Activate garage door timer' )

        def step( self, value, data={}, listeners=[] ):
            """
            This routine will receive a message X minutes after the door has been opened.  If the garage door is 
            still open and the alarm has not been disabled, it will start the alarm:
            
            | 1. set disable alarm to disabled
            | 2. turn off the alarm
                        
            :param value: Not used
            :type value: Boolean
            :param data: a dictionary containing more information about the value. 
            :param listeners: a list of the subscribed routines to send the data to
            :returns: value, data, listeners
            :rtype: Boolean, dict, listeners
    
            """
            self.logger.debug( 'ProcessDelayedAlarm.step called. garage_door [{}] button_pressed [{}]'.
                format( "closed" if self.status_panel.garage_door else 'open',
                        "pressed" if self.status_panel.enable_alarm_button_pressed else "not pressed" ) )
            #  Test to see if the alarm needs to be activated:
            #  1. Is the garage door open
            #  2. Has the disable button been pressed
            if ( self.status_panel.garage_door == self.status_panel.GARAGE_DOOR_OPEN ):
                # TODO: Fixme
#                  and
#                  self.status_panel.enable_alarm_button_pressed == self.status_panel.ENABLE_ALARM ):

                self.logger.debug( 'delayedAlarmState = {}'.format( self.delayedAlarmState ) )

                if ( self.delayedAlarmState == self.PreAlarm ):
                    # Long wait for when the door opens until the alarm goes off
                    self.delayedAlarmState = self.Short_Beep
                    self.status_panel.changeAlarm( self.status_panel.ALARM_ON )
                    self.status_panel.alarm = self.status_panel.ALARM_ON
                    self.activateTimer( self.status_panel.garage_door_short_alarm )
                    self.logger.debug( 'transitioning to = {}'.format( self.delayedAlarmState ) )
                elif ( self.delayedAlarmState == self.Short_Beep ):
                    # Short 2 second blast
                    self.delayedAlarmState = self.Long_Silence
                    self.status_panel.changeAlarm( self.status_panel.ALARM_OFF )
                    self.status_panel.alarm = self.status_panel.ALARM_OFF
                    self.activateTimer( self.status_panel.garage_door_long_silence )
                    self.logger.debug( 'transitioning to = {}'.format( self.delayedAlarmState ) )
                elif ( self.delayedAlarmState == self.Long_Silence ):
                    # Long pause between blasts
                    self.delayedAlarmState = self.Short_Beep
                    self.status_panel.changeAlarm( self.status_panel.ALARM_ON )
                    self.status_panel.alarm = self.status_panel.ALARM_ON
                    self.activateTimer( self.status_panel.garage_door_short_alarm )
                    self.logger.debug( 'transitioning to = {}'.format( self.delayedAlarmState ) )
                else:
                    self.logger.debug( 'invalid state = {}'.format( self.delayedAlarmState ) )
            else:
                self.delayedAlarmState = self.Disabled
            self.logger.debug( 'ProcessDelayedAlarm. {}'.format( self.delayedAlarmState ) )
            return value, data, listeners

    class SystemCheck( abcStep ):

        toggle = True

        def __init__( self, status_panel ):
            '''
            SystemCheck will toggle on and off the green status LED indicating that 
            the system is running.
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
    
            """
            value = self.toggle = not self.toggle
            self.logger.debug( 'System Check called. {}'.format( self.toggle ) )
            return value, data, listeners
