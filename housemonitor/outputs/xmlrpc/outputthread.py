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
from housemonitor.inputs.dataenvelope import DataEnvelope


class XmlRpcOutputThread( Base, threading.Thread ):
    '''

    '''

    __host = 'localhost'
    __port = 9002
    __current_values = None
    __input_queue = None

    def __init__( self, current_values, input_queue ):
        '''
        '''
        super( XmlRpcOutputThread, self ).__init__()
        threading.Thread.__init__( self )
        self.current_values = current_values
        self.input_queue = input_queue

    ''' Make sure and enter the appropriate entry in the logging configuration
    file
    '''
    @property
    def logger_name( self ):
        ''' Set the logger level. '''
        return Constants.LogKeys.outputsXMLRPC

    def send_command( self, value, device, port, steps ):
        env = DataEnvelope( type=Constants.EnvelopeTypes.COMMAND, value=value,
                            device=device, port=port, steps=steps )
        self.input_queue.transmit( env, Constants.Queue.mid_priority )
        self.logger.debug( "send command: value = {} device = {} port = {} steps = {}".format( value, device, port, steps ) )
        return value

    def get_current_value( self, device, port ):
        value = self.__current_values.get( device, port )
        self.logger.debug( "get current value: device = {} port = {} value = {}".format( device, port, value ) )
        return value

    def get_current_values( self ):
        self.logger.debug( 'get_current_values called' )
        cv = self.__current_values.get()
        self.logger.debug( 'current_values = ', pprint.pformat( cv ) )
        return cv

    def run( self ):
        server = SimpleXMLRPCServer( ( self._host, self._port ), logRequests=True )
        server.register_introspection_functions()
        server.register_function( self.get_current_value )
        server.register_function( self.get_current_values )
        server.serve_forever()