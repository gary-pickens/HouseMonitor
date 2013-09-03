'''
Created on Sep 12, 2012

@author: Gary
'''
import logging
import abc


class Base( object ):
    '''
    This is a ABC (Abstract Base Class) that if included in a classes inheritance tree will enable 
    using the python logger.  It is required that your class define logger_name and that the name
    be in the logger configuration file.  Most of the currently used definitions can be found in::
    
    lib/Constants.LogKeys

    Set up logging with the defined logger_name.  See the 
    `python logging <http://docs.python.org/2/library/logging.html>`_. page for information
    on using this.

    '''
    __metaclass__ = abc.ABCMeta

    logger = None

    def __init__( self ):
        '''
                
        '''
        self.logger = logging.getLogger( self.logger_name )

    @abc.abstractproperty
    def logger_name( self ):
        ''' An abstract property that must be defined in any class that inherits this property.
        See lib/Constants.LogKeys for a list of the currently used definitions.  
        
        The value assigned here must be entered in three places in the logging configuration file:
        
        # in the [Loggers] section
        # in the [Logger__XX] section where XX is the property name.  
        
        See house_monitor_logging.conf as an example.
        
        '''
        return "call to invalid abstract property"    # pragma: no cover
