'''
Created on Sep 26, 2013

@author: gary
'''
import time
import xmlrpclib

class XBeeCommand( object ):
    '''
    classdocs
    '''

    url = ""
    connected = False

    def __init__( self, host ):
        '''
        Constructor
        '''
        super( XBeeCommand, self ).__init__()
        self.url = 'http://{}:{}'.format( host, 9002 )
        self.connect_to_house_monitor()

    def connect_to_house_monitor( self ):
        '''
        This method will attempt to connect to the housemonitor program running on the beaglebone
        server.  If it fails it will sleep for 2 minutes and try again.
        '''
        try:
            self.proxy = xmlrpclib.ServerProxy( self.url )
            self.connected = True
        except xmlrpclib.Error:
            time.sleep( 120 )
            self.connected = False

    def send_command( self, command, device, port, steps ):

        while not self.connected:
            self.connect_to_house_monitor()
        try:
            self.values = self.proxy.send_command( command, device, port, steps )
            print( "sent command {} to device {} to steps {}".format( command, device, steps ) )
        except xmlrpclib.Error as er:
            self.connected = False

    def change_dio( self, value, device, port, steps ):

        while not self.connected:
            self.connect_to_house_monitor()
        try:
            self.values = self.proxy.send_command( value, device, port, steps )
            print( "sent command {} to device {} to steps {}".format( value, device, steps ) )
        except xmlrpclib.Error as er:
            self.connected = False
