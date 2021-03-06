'''
Created on Aug 5, 2012

@author: Gary
'''
from pubsub import pub
from housemonitor.lib.constants import Constants


class Common( object ):
    '''
    Common routines used through out House Monitor
    '''

    def __init__( self ):
        '''
        Constructor
        '''

    @staticmethod
    def send( value, data, listeners ):
        """
        Send takes the first listener off of the list listeners and sends the
        data to the next routine using the pubsub package.

        :param value: the value to send to the next routine
        :param data: additional data do pass along
        :param listeners: a list of subscribers that will get the data
        :Raises: ListenerSpecIncomplete Raised if there is a problem with the topic name.

        >>> from lib.common import Common
        >>> Common.send(999, {'device': 'xyz', 'port': 'abc'}, ())
        
        Note: **This is a static method**
        """
        if len( listeners ):
            # get the first item on the list
            listener = listeners.pop( 0 )
            # test to see if the first item in the list is a list
            if ( ( type( listener ) == type( "" ) ) and
                ( len( listener ) > 0 ) ):
                pub.sendMessage( listener, value=value, data=data, listeners=listeners )
            elif ( type( listener ) == type( [] ) ):
                Common.send( value, data, listener )
                Common.send( value, data, listeners )

    @staticmethod
    def getDeviceAndPort( data ):
        """
        Gets the device and port out of data dictionary.

        :param data: The data that is passed into step.
        :type data: dict
        :returns: device and port
        :rtype: string, string
        :Raises: KeyError

        >>> from lib.common import Common
        >>> Common.getDeviceAndPort({'device': 'xyz', 'port': 'abc'})
        ('xyz', 'abc')


        Note: **This is a static method**
        """
        device = ''
        port = ''
        try:
            device = data[Constants.DataPacket.device]
        except KeyError as ke:
            error = "The device is missing from the data block: {}".format( ke )
            raise KeyError( error )

        try:
            port = data[Constants.DataPacket.port]
        except KeyError as ke:
            error = "The port is missing from the data block: {}".format( ke )
            raise KeyError( error )
        return device, port

    @staticmethod
    def generateDevicePortTree( value, device, port, values ):
        """
        This function will create a values tree containing value.

        :param value: The number to add to the list of numbers.
        :type value: boolean, int or float
        :param device: the device.
        :type device: string
        :param port: the port.
        :type port: string
        :param values: a dictionary for storing the value value.
        :type values: dictionary
        :return: a boolean indicating if the entry is new
        
        >>> from lib.common import Common
        >>> dic = {}
        >>> Common.generateDevicePortTree(999, 'device', 'port', dic)
        True
        >>> print dic
        {'device': {'port': 999}}
        
        Note: **This is a static method**

        """
        new_entry = False
        if device not in values:
            values[device] = {port: value}
            new_entry = True
        if port not in values[device]:
            values[device][port] = value
            new_entry = True
        return new_entry

if __name__ == "__main__":
    import doctest
    doctest.testmod()
