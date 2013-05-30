'''
Created on Jul 30, 2012

@author: Gary
'''
from abc_step import abcStep
from housemonitor.lib.constants import Constants


def instantuate_me( data ):
    return ConvertTMP36VoltsToCentigrade()


class  ConvertTMP36VoltsToCentigrade( abcStep ):
    """
    Convert from TMP36 volts to Centigrade
    """

    @property
    def topic_name( self ):
        """ The topic name to which this routine subscribes."""
        return Constants.TopicNames.TMP36Volts2CentigradeStep

    @property
    def logger_name( self ):
        """ Set the logger name. This needs to be added to house_monitoring_logging.conf"""
        return Constants.LogKeys.steps

    def step( self, value, data={}, listeners=[] ):
        """
        Convert from TMP36 volts to Centigrade
        The formula can be found at:

        http://learn.adafruit.com/tmp36-temperature-sensor

        :param value: The number to convert from volts to centigrade.
        :type value: int, float
        :param data: a dictionary containing more information about the value.
        :param listeners: a list of the subscribed routines to send the data to
        :returns: centigrade, data, listeners
        :rtype: float, dict, listeners

        >>> from steps.tmp36volts2centigrade import ConvertTMP36VoltsToCentigrade
        >>> zig = ConvertTMP36VoltsToCentigrade()
        >>> zig.step(0.8, {'device': 'xyz', 'port': 'abc'}, ['a', 'b'])
        (30.0, {'device': 'xyz', 'units': 'C', 'port': 'abc'}, ['a', 'b'])
        """
        centigrade = ( ( value * 1000.0 ) - 500 ) / 10
        data['units'] = 'C'
        self.logger.debug( "Temperature = %2.1f%s", centigrade, data['units'] )
        return centigrade, data, listeners

if __name__ == "__main__":
    import doctest    # pragma: no cover
    doctest.testmod()    # pragma: no cover
