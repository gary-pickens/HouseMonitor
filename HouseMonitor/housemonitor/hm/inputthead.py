'''
Created on Jun 21, 2012

@author: Gary
'''
import threading
import time
from struct import *
import xmlrpclib


class InputThread( threading.Thread ):
    '''
    Send fake messages though the system and see how it performs.
    '''
    host = 'beaglebone'
    port = 9002
    proxy = None
    _sleep_time = 10

    def __init__( self, current_values ):
        '''
        Constructor
        args:

        '''
        threading.Thread.__init__( self )
        url = 'http://{}:{}'.format( self.host, self.port )
        print( url )
        self.proxy = xmlrpclib.ServerProxy( url )
        self.current_values = current_values

    def run( self ):
        value = {}

        while True:
            self.current_values = self.proxy.get_current_values()
            print( self.current_values )
            time.sleep( self._sleep_time )
