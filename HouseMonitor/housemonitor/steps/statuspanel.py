'''
Created on 2012-05-13

@author: Gary

'''
from abc_step import abcStep
from datetime import timedelta
from lib.base import Base
from lib.common import Common
from lib.constants import Constants
from lib.getdatetime import GetDateTime
from pubsub import pub
import sys
import traceback
import uuid



def instantuate_me( data ):
    ''' This function will be called to instantiate this class. '''
    return StatusPanel()


class StatusPanel( Base ):
    '''
    The Status Panel is responsible for updating the kitchen status panel.  The status panel
    consists for a:
    
    # Green flashing LED that indicates that the system is functioning.
    # A red LED that glows when the garage door is open.
    # A second LED that glows when the disable alarm has been pressed and will extungish when 
    the garage door has been closed.
    # A alarm that will sound 15 minutes after the garage door has opened.
    # A disable button that will disable the alarm.
    
    A schematic is in the Fritzing directory.
    
    There are four classes that will be notified on certain events:
    # *GarageDoorMonitor* which will be notified when the garage door has been opened or closed.
    # *SilenceAlarm* will be notified 2 seconds after the garage door has been opened.
    # *DisableAlarmButton* will be notified when the Disable Alarm Button has been pressed.
    # *ProcessDelayedAlarm* Will be notified when to change the alarm setting.
    # *SystemCheck* will monitor the health of the system and cause the greeen LED to flash if 
    everything is okay.
    
    
    '''

    panel_address = '0x13a20040902a02'
    panel_status_led = 'DIO-0'
    panel_garage_door_led = 'DIO-1'
    panel_disable_button_led = 'DIO-2'
    panel_alarm = 'DIO-3'
    panel_disable = 'DIO-4'

    scheduler_delayed_sound_alarm = 'garage door start delayed alarm'
    scheduler_turn_off_initial_alarm = 'garage door turn off initial alarm'

    #  Classes
    garage_door_monitor = None
    process_delayed_alarm = None
    disable_alarm_button = None
    system_check = None
    silence_alarm = None

    LED_ON = True
    LED_OFF = False

    ENABLE_ALARM = True
    DISABLE_ALARM = False

    # How fast the status light flashes
    status_panel_update_rate = 2

    # The most recent scheduler request
    long_scheduler_id = None
    short_scheduler_id = None

    #  items that are tracked
    ALARM_OFF = False
    ALARM_ON = True
    alarm = ALARM_OFF
    ''' Weather the alarm is sounding or not '''

    GARAGE_DOOR_OPEN = False
    GARAGE_DOOR_CLOSED = True
    garage_door = GARAGE_DOOR_CLOSED
    ''' The state of the garage door. '''

    when_garage_door_opened = None
    ''' The time when the garage door was opened '''

    garage_door_timer = None
    ''' Contains the time that the garage door was opened '''

    DISABLE_ALARM_BUTTON_PRESSED = False
    DISABLE_ALARM_BUTTON_NOT_PRESSED = True
    disenable_alarm_button_pressed = DISABLE_ALARM_BUTTON_NOT_PRESSED
    ''' Indicates that the disable alarm has been pressed.  
    Cleared by closing the door. '''

    ''' The time from when the garage door opens to the time the alarm 
    starts sounding '''
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
        # Turn the alarm off when starting.
        self.changeAlarm( self.ALARM_OFF )

    @property
    def logger_name( self ):
        ''' Set the logger level. '''
        return Constants.LogKeys.StatusPanel

    def changeGarageDoorWarningLight( self, value ):
        ''' Turn on or off the LED that indicates that the disable alarm has been pressed. 
        
        :param value: determines if the light will be on or off.
        :type value: Boolean
        :returns: none
        
        '''
        steps = [Constants.TopicNames.ZigBeeOutput]
        data = {}
        data[Constants.DataPacket.device] = self.panel_address
        data[Constants.DataPacket.port] = self.panel_garage_door_led
        light = not value
        try:
            Common.send( light, data, steps )
        except Exception as ex:
            self.logger.exception( 'Common.send error {}'.format( ex ) )

    def changeDisableButtonWarningLight( self, value ):
        ''' Turn on or off the LED that indicates that the garage door is open. 
        
        :param value: determines if the light will be on or off.
        :type value: Boolean
        :returns: none
        
        '''
        steps = [Constants.TopicNames.ZigBeeOutput]
        data = {}
        data[Constants.DataPacket.device] = self.panel_address
        data[Constants.DataPacket.port] = self.panel_disable_button_led
        try:
            Common.send( value, data, steps )
        except Exception as ex:
            self.logger.exception( 'Common.send error {}'.format( ex ) )


    def changeAlarm( self, value ):
        ''' Turn on or off the alarm that indicates that the garage door is open.         

        :param value: determines if the alarm will be on or off.
        :type value: Boolean
        :returns: none

        '''
        self.alarm = value
        steps = [Constants.TopicNames.ZigBeeOutput]
        data = {}
        data[Constants.DataPacket.device] = self.panel_address
        data[Constants.DataPacket.port] = self.panel_alarm
        self.logger.debug( "changeAlarm with {} {} {}".format( value, data, steps ) )
        try:
            Common.send( value, data, steps )
        except Exception as ex:
            self.logger.exception( 'Common.send error {}'.format( ex ) )

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
            self.status_panel.long_scheduler_id = str( uuid.uuid4() )
            # Delete all the previously scheduled slow alarm events
            try:
                pub.sendMessage( Constants.TopicNames.SchedulerDeleteJob,
                            name=self.status_panel.scheduler_delayed_sound_alarm )
            except Exception as ex:
                self.logger.exception( 'Common.send error {}'.format( ex ) )

            # Then turn the correct one for this event on
            args = self.status_panel.scheduler_delayed_sound_alarm, \
                    self.status_panel.panel_address, \
                    self.status_panel.panel_alarm, \
                    listeners, \
                    self.status_panel.long_scheduler_id

            try:
                pub.sendMessage( Constants.TopicNames.SchedulerAddOneShotStep,
                                delta=self.status_panel.garage_door_standoff_time,
                                args=args )
            except Exception as ex:
                self.logger.exception( 'Common.send error {}'.format( ex ) )

            self.logger.debug( 'Activate garage door timer' )

        def turnOffAlarmAfterInterval( self ):
            '''
            This will start a timer when the garage door opens.  When the 
            timer expire a message will be sent to ProcessDelayedAlarm.step() which will 
            start the alarm. 
            '''
            listeners = [Constants.TopicNames.StatusPanel_SilenceAlarm]
            self.status_panel.short_scheduler_id = str( uuid.uuid4() )

            # Delete all the previously scheduled alarms.
            try:
                pub.sendMessage( Constants.TopicNames.SchedulerDeleteJob,
                                name=self.status_panel.scheduler_turn_off_initial_alarm )
            except Exception as ex:
                self.logger.exception( 'Common.send error {}'.format( ex ) )

            args = ( self.status_panel.scheduler_turn_off_initial_alarm, \
                    self.status_panel.panel_address, \
                    self.status_panel.panel_alarm, \
                    listeners, \
                    self.status_panel.short_scheduler_id )
            try:
                pub.sendMessage( Constants.TopicNames.SchedulerAddOneShotStep,
                                delta=self.status_panel.garage_door_initial_beep_time,
                                args=args )
            except Exception as ex:
                self.logger.exception( 'Common.send error {}'.format( ex ) )
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

            # Garage Door transitioning from Open to Closed
            if self.status_panel.garage_door == self.status_panel.GARAGE_DOOR_OPEN and \
                    value == self.status_panel.GARAGE_DOOR_CLOSED:
                self.status_panel.changeDisableButtonWarningLight( self.status_panel.LED_OFF )
                self.status_panel.changeAlarm( self.status_panel.ALARM_OFF )
                self.status_panel.process_delayed_alarm.delayedAlarmState = self.status_panel.process_delayed_alarm.Disabled
                try:
                    pub.sendMessage( Constants.TopicNames.SchedulerDeleteJob,
                                name=self.status_panel.scheduler_turn_off_initial_alarm )
                except Exception as ex:
                    self.logger.exception( 'Common.send error {}'.format( ex ) )
                try:
                    pub.sendMessage( Constants.TopicNames.SchedulerDeleteJob,
                                name=self.status_panel.scheduler_delayed_sound_alarm )
                except Exception as ex:
                    self.logger.exception( 'Common.send error {}'.format( ex ) )

                self.logger.info( 'Garage door closed' )

            # Garage Door transitioning from Closed to Open
            if self.status_panel.garage_door == self.status_panel.GARAGE_DOOR_CLOSED and \
                    value == self.status_panel.GARAGE_DOOR_OPEN:
                self.status_panel.changeAlarm( self.status_panel.ALARM_ON )
                self.status_panel.changeDisableButtonWarningLight( self.status_panel.LED_OFF )
                self.status_panel.when_garage_door_opened = GetDateTime().datetime()
                self.status_panel.disenable_alarm_button_pressed = self.status_panel.DISABLE_ALARM_BUTTON_NOT_PRESSED
                self.turnOffAlarmAfterInterval()
                self.setTimerToActivateAlarmAfterInterval()
                self.status_panel.process_delayed_alarm.delayedAlarmState = self.status_panel.process_delayed_alarm.PreAlarm
                self.logger.info( 'Garage door opening' )

            # Garage Door is Closed
            if value == self.status_panel.GARAGE_DOOR_CLOSED:
                self.status_panel.when_garage_door_opened = None
                self.status_panel.process_delayed_alarm.delayedAlarmState = self.status_panel.process_delayed_alarm.Disabled
                self.status_panel.disenable_alarm_button_pressed = self.status_panel.DISABLE_ALARM_BUTTON_NOT_PRESSED
                self.status_panel.changeDisableButtonWarningLight( self.status_panel.LED_OFF )


            self.status_panel.garage_door = value
            self.status_panel.changeGarageDoorWarningLight( value )
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
            self.logger.debug( 'Silence alarm.' )
            if data[Constants.DataPacket.scheduler_id] == self.status_panel.short_scheduler_id:
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
            if value == self.status_panel.DISABLE_ALARM_BUTTON_PRESSED:
                self.logger.info( 'Disable alarm button pressed' )
                self.status_panel.disenable_alarm_button_pressed = self.status_panel.DISABLE_ALARM_BUTTON_PRESSED
                self.status_panel.changeAlarm( self.status_panel.ALARM_OFF )
                self.status_panel.changeDisableButtonWarningLight( self.status_panel.LED_ON )
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
            self.status_panel.long_scheduler_id == str( uuid.uuid4() )
            try:
                pub.sendMessage( Constants.TopicNames.SchedulerDeleteJob,
                                 self.status_panel.scheduler_turn_off_initial_alarm )
            except Exception as ex:
                self.logger.exception( 'Common.send error {}'.format( ex ) )

            args = self.status_panel.scheduler_turn_off_initial_alarm, \
                    self.status_panel.panel_address, \
                    self.status_panel.panel_alarm, \
                    listeners, \
                    self.status_panel.long_scheduler_id
            try:
                pub.sendMessage( Constants.TopicNames.SchedulerAddOneShotStep,
                                delta=timedelta( seconds=seconds ),
                                args=args )
            except Exception as ex:
                self.logger.exception( 'Common.send error {}'.format( ex ) )
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
            # Test if the correct packet
            if data[Constants.DataPacket.scheduler_id] == self.status_panel.long_scheduler_id:
                if self.status_panel.garage_door == self.status_panel.GARAGE_DOOR_OPEN:
                    if self.status_panel.disenable_alarm_button_pressed == self.status_panel.DISABLE_ALARM_BUTTON_PRESSED :
                        self.delayedAlarmState = self.Disabled
                        self.status_panel.changeAlarm( self.status_panel.ALARM_OFF )
                        self.logger.debug( 'Disable alarm pressed. exit' )
                    else:
                        if ( self.delayedAlarmState == self.PreAlarm ):
                            self.status_panel.changeAlarm( self.status_panel.ALARM_ON )
                            self.activateTimer( self.status_panel.garage_door_short_alarm )
                            self.delayedAlarmState = self.Short_Beep
                            self.logger.debug( 'short beep' )
                        elif ( self.delayedAlarmState == self.Short_Beep ):
                            self.status_panel.changeAlarm( self.status_panel.ALARM_OFF )
                            self.activateTimer( self.status_panel.garage_door_long_silence )
                            self.delayedAlarmState = self.Long_Silence
                            self.logger.debug( 'long silence' )
                        elif ( self.delayedAlarmState == self.Long_Silence ):
                            self.status_panel.changeAlarm( self.status_panel.ALARM_ON )
                            self.activateTimer( self.status_panel.garage_door_short_alarm )
                            self.delayedAlarmState = self.Short_Beep
                            self.logger.debug( 'Short Beep' )
                        elif ( self.delayedAlarmState == self.Disabled ):
                            self.logger.debug( 'Disabled state' )
                            self.status_panel.changeAlarm( self.status_panel.ALARM_OFF )
                        else:
                            self.status_panel.changeAlarm( self.status_panel.ALARM_OFF )
                            self.logger.warn( 'invalid state = {}'.format( self.delayedAlarmState ) )
                else:
                    self.delayedAlarmState = self.Disabled
                    self.status_panel.changeAlarm( self.status_panel.ALARM_OFF )
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
            # disable the following line. It prints aboue every two seconds.
#            self.logger.info( 'System Check called. {}'.format( self.toggle ) )
            return value, data, listeners
