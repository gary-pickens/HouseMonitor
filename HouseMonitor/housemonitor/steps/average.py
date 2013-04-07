'''
Created on 2012-10-17

@author: Gary

'''
from steps.abc_step import abcStep
from lib.constants import Constants
from configuration.formatconfiguration import FormatConfiguration
from collections import deque
from pprint import pprint
from pubsub.utils import printTreeDocs
from lib.common import Common


def instantuate_me( data ):
    ''' This function will be called to instantiate this class. '''
    return Average()


class Average( abcStep ):
    '''
    This class will take the average of the last N samples.

    Where N is the DEFAULT_SAMPLES(10) or the sample size that is defined in the file 'avg.xml'.

    The format of avg.xml is as follows::

        <?xml version="1.0" encoding="UTF-8"?>
        <average>
            <item device="0x13a200409029bf" port="adc-1">30</item>
        </average>

    The proceding file will cause samples from device *0x13a200409029bf* port *adc-1* to be average over
    30 samples.

    '''
    DEFAULT_SAMPLES = 10
    ''' The default number of samples to average. '''

    samples = {}
    ''' The repository cantaining the samples for each device. '''

    def __init__( self ):
        '''
        Instantuate the Average class and read the configuration File.

        '''
        super( Average, self ).__init__()
        self.config = FormatConfiguration().configure( 'avg.xml' )

    @property
    def topic_name( self ):
        ''' The topic name to which this routine subscribes.'''
        return Constants.TopicNames.AverageStep

    @property
    def configuration_file_name( self ):
        ''' The topic name to which this routine subscribes.'''
        return __name__

    @property
    def logger_name( self ):
        ''' Set the logger name. '''
        return Constants.LogKeys.steps

    def save_samples( self, device, port, samples ):
        """
        save the samples in the data structure self.samples

        :param device: The name of the device.
        :type device: string
        :param port: The name of the port.
        :type port: string
        :param samples: a deque containing the data that will saved to generate the average
        :type samples: dequeue
        :Raises: None

        """
        if ( device in self.samples ) and ( port in self.samples[device] ):
            self.samples[device][port] = samples
        else:
            self.samples[device] = {port: samples}

    def get_samples( self, device, port, number_of_samples ):
        '''
        get the samples from the samples dict.  If one has not been defined then create a deque for data samples.

        :param device: The name of the device.
        :type device: string
        :param port: The name of the port.
        :type port: string
        :param number_of_samples: The number of samples for generating the averaage.
        :type dequeue:
        :param samples: - the deque for storing the data samples.  Its maxlen will be set to the number of samples
        :returns: degue for storing the data

        '''
        if ( device in self.samples ) and ( port in self.samples[device] ):
            samples = self.samples[device][port]
        else:
            samples = deque( [], number_of_samples )
        return samples

    def get_number_of_samples( self, device, port ):
        '''
        get the number of samples for this port and device.

        The number of samples is stored it the xml configuration file

        :param device: The name of the device.
        :type device: string
        :param port: The name of the port.
        :type port: string
        :returns: The number of samples for this device and port.  If the file does not contain the number the use the default.

        '''
        if ( device in self.config ) and ( port in self.config[device] ):
            number_of_samples = int( self.config[device][port] )
        else:
            number_of_samples = self.DEFAULT_SAMPLES
        return number_of_samples

    def step( self, value, data={}, listeners=[] ):
        """
        This function will compute the average for each device and port.

        :param value: The input value to be processesed
        :type value: int, float, string, etc
        :param data: a dictionary containing more information about the value.
        :param listeners: a list of the subscribed routines to send the data to
        :returns: new_value, new_data, new_listeners
        :rtype: int, dict, listeners
        :raises: None

        >>> from steps.average import Average
        >>> avg = Average()
        >>> avg.step(0.0, {'device': 'xyz', 'port': 'abc'}, ['a', 'b'])
        (0, {'device': 'xyz', 'units': 'V', 'port': 'abc'}, ['a', 'b'])
        >>> avg.step(1.0, {'device': 'xyz', 'port': 'abc'}, ['a', 'b'])
        (0.5, {'device': 'xyz', 'units': 'V', 'port': 'abc'}, ['a', 'b'])

        """
        device, port = Common.getDeviceAndPort( data )

        number_of_samples = self.get_number_of_samples( device, port )

        samples = self.get_samples( device, port, number_of_samples )
        samples.append( value )
        average = sum( samples ) / len( samples )

        self.save_samples( device, port, samples )
        self.logger.debug( "average = {}".format( average ) )
        return average, data, listeners
