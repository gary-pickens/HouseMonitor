'''
Created on Aug 5, 2012

@author: Gary
'''
from pubsub import pub
from lib.constants import Constants


class Common(object):
    '''
    Common routines used through out House Monitor
    '''

    def __init__(self):
        '''
        Constructor
        '''

    @staticmethod
    def send(value, data, listeners):
        """
        Send takes the first listener off of the list listeners and sends the
        data to the next routine using the pubsub package.

        Args:
            value: the value to send to the next routine
            data: additional data do pass along
            listeners: a list of subscribers that will get the data

        see special section that describe the listeners list
        """
        if len(listeners):
            # get the first item on the list
            listener = listeners.pop(0)
            # test to see if the first item in the list is a list
            if ((type(listener) == type("")) and
                (len(listener) > 0)):
                pub.sendMessage(listener, value=value, data=data, listeners=listeners)
            elif (type(listener) == type([])):
                Common.send(value, data, listener)
                Common.send(value, data, listeners)

    @staticmethod
    def getDeviceAndPort(data):
        """
        Gets the device and port out of data dictionary

        :param data: The data that is passed into step.
        :type data: dict
        :returns: device and port
        :rtype: string, string
        :Raises: KeyError

        :Example:

        >>> from steps.tmp36volts2centigrade import ConvertTMP36VoltsToCentigrade
        >>> zig = ConvertTMP36VoltsToCentigrade()
        >>> zig.getDeviceAndPort({'device': 'xyz', 'port': 'abc'})
        'xyz', 'abc'
        """
        device = ''
        port = ''
        try:
            device = data[Constants.DataPacket.device]
        except KeyError as ke:
            error = "The device is missing from the data block: {}".format(ke)
            raise KeyError(error)

        try:
            port = data[Constants.DataPacket.port]
        except KeyError as ke:
            error = "The port is missing from the data block: {}".format(ke)
            raise KeyError(error)
        return device, port

    @staticmethod
    def generateDevicePortTree(value, device, port, values):
        """
        This function will create a values tree containing value.

        Args:
        :param value: The number to add to the list of numbers.
        :type value: boolean, int or float
        :param device: the device.
        :type device: string
        :param device: the port.
        :type port: string
        :param values: a dictionary for storing the value value.
        :type port: dictionary
        :return: a boolean indicating if the entry is new
        """
        new_entry = False
        if device not in values:
            values[device] = {port: value}
            new_entry = True
        if port not in values[device]:
            values[device][port] = value
            new_entry = True
        return new_entry
