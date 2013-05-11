'''
Created on Nov 7, 2012

@author: Gary

'''
from threading import Lock
import copy
import pprint

from base import Base
from constants import Constants


class CurrentValues( Base ):
    '''
    This module stores and returns the most resent data received from a device and port.  It is primarily used
    for communicating the current value between threads.
    '''
    _current_values = {}
    _current_values_lock = None

    def __init__( self ):
        '''
        Initialize the lock for thread safe communications.
        '''
        super( CurrentValues, self ).__init__()
        if ( self._current_values_lock == None ):
            self._current_values_lock = Lock()
        self.logger.debug( "Current Value started" )

    def buildDataBlock( self, value, data ):
        '''
        Build a data block that is used to store the current values.  The data that is stored
        in the data block is:
        1.    arrival time
        2.    Units
        3.    name
        4.    value

        The index for each item is: Constants.DataPacket.arrival_time, Constants.DataPacket.units
        Constants.DataPacket.name, and Constants.DataPacket.current_value.

        :param value: the current value
        :type value: int, float, str
        :param data: the data that is pasted between steps
        :type dict:
        :returns: dict containing the above items
        :raises: None
        
        >>> from lib.currentvalues import CurrentValues
        >>> cv = CurrentValues()
        >>> data = {Constants.DataPacket.arrival_time: 'now', Constants.DataPacket.units: 'F', Constants.DataPacket.name: 'gary'}
        >>> cv.buildDataBlock(999, data)
        {'units': 'F', 'current_value': 999, 'at': 'now', 'name': 'gary'}
        
        
        '''
        if value != None:
            current_data = {}
            if Constants.DataPacket.arrival_time in data and data[Constants.DataPacket.arrival_time] != None:
                current_data[Constants.DataPacket.arrival_time] = data[Constants.DataPacket.arrival_time]
            if Constants.DataPacket.units in data and data[Constants.DataPacket.units] != None:
                current_data[Constants.DataPacket.units] = data[Constants.DataPacket.units]
            if Constants.DataPacket.name in data and data[Constants.DataPacket.name] != None:
                current_data[Constants.DataPacket.name] = data[Constants.DataPacket.name]
            current_data[Constants.DataPacket.current_value] = value
            return current_data
        else:
            raise ValueError()

    def store( self, value, device, port, data ):
        '''
        Store the current data in the current value dictionary.

        This module is thread safe.

        :param device: the device the data is coming from
        :type device: str
        :param port: the port the data is coming from.
        :type port: str
        :param data: the port the data is coming from.
        :type data: dict
        :raises: None
        
        >>> from lib.currentvalues import CurrentValues
        >>> cv = CurrentValues()
        >>> cv.store(999, 'device', 'port', {'a': 'A', 'b': 'B'})
        >>> print cv._current_values
        {'device': {'port': {'current_value': 999}}}

        '''
        self.logger.debug( 'store {} {} {}'.format( device, port, value ) )
        self._current_values_lock.acquire()
        try:
            if ( device in self._current_values ):
                if ( port in self._current_values[device] ):
                    self._current_values[device][port] = self.buildDataBlock( value, data )
                else:
                    self._current_values[device][port] = self.buildDataBlock( value, data )
            else:
                self._current_values[device] = {port: self.buildDataBlock( value, data )}
        except ValueError as ve:
            self.logger.exception( "Value is set to None for {} {}".format( device, port ) )
        finally:
            self._current_values_lock.release()
#        self.logger.debug('store current_values = {}'.format(pprint.pformat(self._current_values)))

    def get( self ):
        '''
        Get all the current values.

        Thread safe

        :return: the current_value data

        >>> from lib.currentvalues import CurrentValues
        >>> cv = CurrentValues()
        >>> cv.store(999, 'device', 'port', {})
        >>> cv.get()
        {'device': {'port': {'current_value': 999}}}

        '''
        self.logger.debug( 'get current value tree' )
        self._current_values_lock.acquire()
        try:
            data = copy.copy( self._current_values )
        finally:
            self._current_values_lock.release()
        return data

    def get_current_value( self, device, port ):
        '''
        Get the current value given the device and port.

        :param device: The device
        :type device: str
        :param port: The port
        :type port: str
        :return: dict containing the data for the selected item
        
        >>> from lib.currentvalues import CurrentValues
        >>> cv = CurrentValues()
        >>> cv.store(999, 'device', 'port', {})
        >>> cv.get_current_value('device', 'port')
        {'current_value': 999}
        
        '''
        self._current_values_lock.acquire()
        try:
            data = self._current_values[device][port]
        finally:
            self._current_values_lock.release()
        self.logger.debug( 'get current value {} {}'.format( device, port ) )
        return data

    @property
    def logger_name( self ):
        ''' Set the logger level. '''
        return 'lib'

if __name__ == "__main__":
    import doctest
    doctest.testmod()

