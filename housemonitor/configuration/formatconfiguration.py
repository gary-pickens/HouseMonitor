'''
Created on Oct 17, 2012

@author: Gary
'''
import pprint

from housemonitor.lib.base import Base
from xmlconfiguration import XmlConfiguration
from housemonitor.lib.constants import Constants

class FormatConfiguration( XmlConfiguration, dict ):
    """
    Read the format configuration file.
    """

    def __init__( self, file_name='' ):
        """
        instantiation
        """
        super( FormatConfiguration, self ).__init__()

    '''
    Make sure and enter the appropriate entry in the logging configuration
    file
    '''
    @property
    def logger_name( self ):
        return Constants.LogKeys.configuration

    @property
    def configuration_file_name( self ):
        return __name__

    def process_configuration( self, parent ):
        config = {}
        for item in parent.findall( 'item' ):
            format = item.text
            device = item.get( 'device' )
            port = item.get( 'port' )
            if ( device not in config ):
                ports = {}
            else:
                ports = config[device]
            ports[port] = format
            config[device] = ports
        return config
