'''
Created on Nov 6, 2012

@author: Gary
'''
from housemonitor.lib.base import Base
from outputthread import XmlRpcOutputThread
from housemonitor.lib.constants import Constants


class XMLRPCControl( Base ):
    '''
    classdocs
    '''
    OutputThread = None
    __current_values = None
    __input_queue = None
    __options = None


    def __init__( self, current_values, input_queue, options ):
        '''
        Constructor
        '''
        super( XMLRPCControl, self ).__init__()
        self.__current_values = current_values
        self.__input_queue = input_queue
        self.__options = options

    @property
    def logger_name( self ):
        """ Set the logger level. This needs to be added to house_monitoring_logging.conf"""
        return Constants.LogKeys.outputsXMLRPC

    def startXMLRPC( self, options ):
        self.OutputThread = XmlRpcOutputThread( self.__current_values, self.__input_queue )
        self.OutputThread.start()
