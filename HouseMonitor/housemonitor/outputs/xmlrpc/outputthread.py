'''
Created on 2012-10-20

@author: Gary

'''
from housemonitor.lib.base import Base
from housemonitor.lib.constants import Constants
from pprint import pprint
from SimpleXMLRPCServer import SimpleXMLRPCServer
import pprint
import threading
import time
import os


class XmlRpcOutputThread( Base, threading.Thread ):
    '''

    '''

    # TODO put this in a configuration file
    _select_hostname_based_on_os = {'posix': 'beaglebone',
                                   'nt': 'localhost'}
    _host = _select_hostname_based_on_os[os.name]
    _port = 9002

    def __init__( self, current_values ):
        '''
        '''
        super( XmlRpcOutputThread, self ).__init__()
        threading.Thread.__init__( self )
        self.current_values = current_values

    ''' Make sure and enter the appropriate entry in the logging configuration
    file
    '''
    @property
    def logger_name( self ):
        ''' Set the logger level. '''
        return Constants.LogKeys.outputsXMLRPC

    def get_current_value( self, device, port ):
        self.logger.debug( 'get_current_value called' )
        value = self.current_values.get( device, port )
        self.logger.debug( "{} {} = {}".format( device, port, value ) )
        return value

    def get_current_values( self ):
        self.logger.debug( 'get_current_values called' )
        cv = self.current_values.get()
#        self.logger.debug('current_value = {}'.format(pprint.pformat(cv)))
        return cv

    def run( self ):
        self.logger.warn( "Starting XMLRPC server on {} {}".format( self._host, self._port ) )
        server = SimpleXMLRPCServer( ( self._host, self._port ), logRequests=False )
        server.register_introspection_functions()
        server.register_function( self.get_current_value )
        server.register_function( self.get_current_values )
        server.serve_forever()
