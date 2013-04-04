'''
Created on Aug 5, 2012

@author: Gary
'''
import abc
from pubsub import pub
from lib.base import Base


class iOutput(Base):
    '''
    This is an abstract class for outputting data.
    '''
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        '''
        Constructor
        '''
        super(iOutput, self).__init__()
#        pub.subscribe(self.output, self.topic_name)

    @abc.abstractproperty
    def topic_name(self):
        return 'Should never see this'

    @abc.abstractmethod
    def output(self, value, data, listeners):
        """
        This routine will be called to convert value from one unit to another
        such as Centigrade to Fahrenheit.

        Args:
            value: is the value to convert
            listeners: are the routines that this value will go through
            being processed
            data: a dictionary containing more information about the
                value. Data can be added to this as needed.  Here is a list
                of values that will be in the data dictionary:

                date_time_received: time when value was received.
                Units: units of the number
                Name: name assigned to the value
                etc.


        """
