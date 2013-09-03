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
    _current_values = None

    def __init__( self, global_data ):
        '''
        Constructor
        '''
        super( XMLRPCControl, self ).__init__()
        self._current_values = global_data['current values']

    @property
    def logger_name( self ):
        """ Set the logger level. This needs to be added to house_monitoring_logging.conf"""
        return Constants.LogKeys.outputsXMLRPC

    def startXMLRPC( self, options ):
        self.OutputThread = XmlRpcOutputThread( self._current_values )
        self.OutputThread.start()
