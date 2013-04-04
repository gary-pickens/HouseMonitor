'''
Created on Oct 10, 2012

@author: Gary
'''
from serial import Serial

from inputs.zigbeeinput.xbeecommunications import XBeeCommunications
from configuration.xmlconfiguration import XmlConfiguration
from lib.constants import Constants


class WindowsXbeeCommunications(XBeeCommunications, XmlConfiguration, object):
    """
    Connect to the XBee connected to the windows PC
    """
    #====================================================
    #  Configuration for the windows computer
    #====================================================

    def __init__(self):
        super(WindowsXbeeCommunications, self).__init__()

    def setup(self):
        port = self.config[Constants.XbeeConfiguration.xbee_windows_port]
        baudrate = int(self.config[Constants.XbeeConfiguration.xbee_windows_baud])
        return Serial(port, baudrate)

    def close(self):
        Serial.close()

    @property
    def configuration_topic_name(self):
        return __name__

    @property
    def configuration_file_name(self):
        return __name__
