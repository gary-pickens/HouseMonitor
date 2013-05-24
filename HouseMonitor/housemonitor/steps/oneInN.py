'''
Created on 2012-11-14

@author: Gary

'''
from housemonitor.lib.constants import Constants
from housemonitor.configuration.formatconfiguration import FormatConfiguration
from abc_step import abcStep
from housemonitor.lib.common import Common


def instantuate_me( data ):
    ''' This function will be called to instantiate this class. '''
    return OneInN()


class OneInN( abcStep ):
    '''
    This class will pass along one in N samples.  This could be used
    to slow the rate that samples will be sent to some remote site.  ie. COSM

    The N is stored in an xml file named oneInN.xml.  It looks as follows:

    ::

        <?xml version="1.0" encoding="UTF-8"?>
        <OneInN>
            <item device="0x13a200409029bf" port="adc-1">10</item>
        </OneInN>

    '''

    count = None
    ''' Montains a count for each input device port combination. '''

    config = None
    ''' Configuration data. '''

    def __init__( self ):
        '''
        Construct the object OneInN and read the configuration file.
        '''
        super( OneInN, self ).__init__()
        self.config = FormatConfiguration().configure( 'oneInN.xml' )
        self.count = {}

    @property
    def topic_name( self ):
        ''' The topic name to which this routine subscribes.'''
        return Constants.TopicNames.OneInNStep

    def configuration_file_name( self ):
        ''' The topic name to which this routine subscribes.'''
        return __name__

    @property
    def logger_name( self ):
        ''' Set the logger level. '''
        return Constants.LogKeys.steps

    def step( self, value, data={}, listeners=[] ):
        """
        This function will take one sample out of limit samples.

        :param value: The input value to be processesed
        :type value: int, float, string, etc
        :param data: a dictionary containing more information about the value.
        :param listeners: a list of the subscribed routines to send the data to
        :returns: new_value, new_data, new_listeners
        :rtype: int, dict, listeners
        :raises: KeyError

        >>> from steps.oneInN import oneInN
        >>> oneInN = oneInN()
        >>> c2f.step(0, {'device': 'test', 'port': 'test'}, ['a', 'b'])
        (32.0, {'device': 'test', 'units': 'F', 'port': 'test'}, [])
        >>> c2f.step(100, {'device': 'test', 'port': 'test'}, ['a', 'b'])
        (212.0, {'device': 'test', 'units': 'F', 'port': 'test'}, ['a', 'b'])

        """
        device, port = Common.getDeviceAndPort( data )
        limit = int( self.config[device][port] )

        Common.generateDevicePortTree( 0, device, port, self.count )
        if ( self.count[device][port] % limit ) != 0:
            listeners = []
            self.logger.debug( "count is {}: don't send data".format( self.count[device][port] ) )
        else:
            self.logger.debug( "count is {}: send data".format( self.count[device][port] ) )
        self.count[device][port] += 1
        return value, data, listeners
