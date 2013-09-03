'''
Created on Aug 5, 2012

@author: Gary
'''
import abc
from pubsub import pub
from housemonitor.lib.base import Base


class iOutput( Base ):
    '''
    This is an abstract class for outputting data.
    '''
    __metaclass__ = abc.ABCMeta

    def __init__( self ):
        '''
        Constructor
        '''
        super( iOutput, self ).__init__()
#        pub.subscribe(self.output, self.topic_name)

    @abc.abstractproperty
    def topic_name( self ):
        return 'Should never see this'

    @abc.abstractmethod
    def output( self, value, data, listeners ):
        """
        This routine will be called to convert value from one unit to another
        such as Centigrade to Fahrenheit.

        :param value: Not used
        :type value: Boolean
        :param data: a dictionary containing more information about the value. 
        :param listeners: a list of the subscribed routines to send the data to
        :returns: value, data, listeners
        :rtype: Boolean, dict, listeners


        """
