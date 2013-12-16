'''
Created on Dec 14, 2013

@author: gary
'''
from datetime import datetime
import time


class WaitForSystemTime( object ):
    '''
    When HouseMonitor is starting at boot time, the NTP (Network
    Time Protocol) has not set the time yet.  This class delays
    the start until the system time has been set.
    '''

    HOUSEMONITOR_EPOCH_TIME = datetime( 2012, 9, 10, 0, 0, 0 )
    WAIT_FOR_SYSTEM_TIME = 15

    def __init__( self, sleep=time.sleep ):
        '''
        Initialize WaitForSystemTime.

        :param sleep: For unit test. Used for injecting a mock sleep.
        :type function

        '''
        super( WaitForSystemTime, self ).__init__()
        self.sleep = sleep

    def validSystemTime( self, now=datetime.now() ):
        '''
        Test if system time has been set.  When first booted it is
        set to the UNIX epoch which is January 1 1970.  After NTP has
        set the time it is after housemonitor epoch time(Sept 10, 2012)

        :param now: For unit test. Used for injecting a mock now.
        :type function

        '''
        if ( now < self.HOUSEMONITOR_EPOCH_TIME ):
            print( 'waiting for system time to be set: {}'.format( now ) )
            self.sleep( self.WAIT_FOR_SYSTEM_TIME )
            return False
        else:
            return True

    def wait( self ):
        '''
        Wait for system time to be set.

        '''
        valid_system_time = False
        while not valid_system_time:
            valid_system_time = self.validSystemTime( datetime.now() )
