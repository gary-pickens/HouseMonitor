'''
Created on Sep 23, 2012

@author: Gary

'''
import pprint

from housemonitor.lib.base import Base
from xmlconfiguration import XmlConfiguration


class CosmConfiguration(XmlConfiguration, dict):
    """
    Read the COSM configuration file.
    """
    config = {}

    def __init__(self, file_name=''):
        """
        instantiation
        """
        super(CosmConfiguration, self).__init__()

    '''
    Make sure and enter the appropriate entry in the logging configuration
    file
    '''
    @property
    def logger_name(self):
        ''' Set the logger level. '''
        return 'configuration'

    def __getitem__(self, device):
        return self.config[device]

    def __setitem__(self, device, value):
        self.config[device] = value

    def process_configuration(self, parent):
        config = {}
        device = None
        port = None
        for child in parent:
            if (child.tag == "item"):
                if ("device" in child.attrib):
                    device = "{0:#8x}".format(int(child.get("device"), 16))
                if ("port" in child.attrib):
                    port = child.get("port")
                # TODO: More work on tags is needed.  Currently only one is supported.
                info = self.process_configuration(child)
                if ((device != None) and (port != None)):
                    ports = {}
                    if (device in config):
                        ports = config[device]
                    ports[port] = info
                    config[device] = ports
            elif (len(list(child)) == 0):
                config[child.tag] = child.text
        return config
