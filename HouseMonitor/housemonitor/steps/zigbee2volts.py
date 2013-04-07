'''
Created on Jul 30, 2012

@author: Gary
'''

from abc_step import abcStep
from lib.constants import Constants


class  ZigbeeCountToVolts( abcStep ):
    """
    Convert Zigbee count to Volts
    """

    VOLTS_PER_COUNT = 1.2 / 1024

    @property
    def topic_name( self ):
        """ The topic name to which this routine subscribes."""
        return Constants.TopicNames.ZigbeeAnalogNumberToVoltsStep

    @property
    def logger_name( self ):
        """ Set the logger name. This needs to be added to house_monitoring_logging.conf"""
        return Constants.LogKeys.steps

    def step( self, value, data={}, listeners=[] ):
        """
        Convert the Zigbee analog count(value) to volts


        :math: V = ( 1.2 * count ) / 1024

        The formula can be found at:

        .. seealso::  http://learn.adafruit.com/tmp36-temperature-sensor

        :param value: Not used
        :type value: Boolean
        :param data: a dictionary containing more information about the value. 
        :param listeners: a list of the subscribed routines to send the data to
        :returns: value, data, listeners
        :rtype: Boolean, dict, listeners

        >>> from steps.zigbee2volts import ZigbeeCountToVolts
        >>> zig = ZigbeeCountToVolts()
        >>> zig.step(700, {'device': 'xyz', 'port': 'abc'}, ['a', 'b'])
        (0.8203125, {'device': 'xyz', 'units': 'V', 'port': 'abc'}, ['a', 'b'])

        """
        volts = value * self.VOLTS_PER_COUNT
        data['units'] = 'V'
        self.logger.debug( "Volts = %4.1f%s", volts, data['units'] )
        return volts, data, listeners


def instantuate_me( data ):
    '''
    This function is used to instantuate this modules class

    instantuate_me(data)
    returns ZigbeeCountToVolts object
    :param data: a dictionary containing several options needed by some steps: (options and args passed in from the command line)
    :returns: ZigbeeCountToVolts object

    '''
    return ZigbeeCountToVolts()


if __name__ == "__main__":
    import doctest    # pragma: no cover
    doctest.testmod()    # pragma: no cover
