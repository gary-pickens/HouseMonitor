'''
Created on Aug 2, 2012

@author: Gary
'''

from abc_step import abcStep
from housemonitor.lib.constants import Constants


def instantuate_me( data ):
    return ConvertCentigradeToFahrenheit()


class ConvertCentigradeToFahrenheit( abcStep ):
    """
    Convert from Centigrade to Fahrenheit
    """
    @property
    def topic_name( self ):
        """ The topic name to which this routine subscribes."""
        return Constants.TopicNames.CentigradeToFahrenheitStep

    @property
    def logger_name( self ):
        """ Set the logger level. This needs to be added to house_monitoring_logging.conf"""
        return Constants.LogKeys.steps

    def step( self, value, data={}, listeners=[] ):
        """
        Convert from Centigrade to Fahrenheit

        :param value: The input value to be processesed
        :type value: int, float, string, etc
        :param data: a dictionary containing more information about the value.
        :param listeners: a list of the subscribed routines to send the data to
        :returns: new_value, new_data, new_listeners
        :rtype: int, dict, listeners
        :raises: None

        >>> from steps.centigrade2fahrenheit import ConvertCentigradeToFahrenheit
        >>> c2f = ConvertCentigradeToFahrenheit()
        >>> c2f.step(0, {'device': 'xyz', 'port': 'abc'}, ['a', 'b'])
        (32.0, {'device': 'xyz', 'units': 'F', 'port': 'abc'}, ['a', 'b'])
        >>> c2f.step(100, {'device': 'xyz', 'port': 'abc'}, ['a', 'b'])
        (212.0, {'device': 'xyz', 'units': 'F', 'port': 'abc'}, ['a', 'b'])
        """

        Fahrenheit = ( ( 9.0 / 5.0 ) * value ) + 32
        data['units'] = 'F'
        self.logger.debug( "Temperature = %3.1f%s", Fahrenheit, data['units'] )
        return Fahrenheit, data, listeners
