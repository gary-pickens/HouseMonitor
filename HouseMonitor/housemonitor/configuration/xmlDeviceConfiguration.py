'''
Created on Sep 13, 2012

@author: Gary
'''
import glob
import os.path
import copy
import traceback
import sys
import pprint

from xmlconfiguration import XmlConfiguration
from lib.constants import Constants


class InvalidDeviceError(Exception):
    '''
    This exception will be raised when than invalid device was used.
    '''
    def __init__(self, device=None):
        self.value = "Invalid device ({})".format(device, os.linesep)

    def __str__(self):
        return repr(self.value)


class InvalidPortError(Exception):
    '''
    This exception will be raised when than invalid port is used.
    '''
    def __init__(self, port=None):
        self.value = "Invalid port ({})".format(port, os.linesep)

    def __str__(self):
        return repr(self.value)


class InvalidConfigurationOptionError(Exception):
    '''
    This exception will be raised when an invalid configuration option is raised.
    '''
    def __init__(self, device, port=None, option=None):
        if port == None:
            self.value = 'Required configuration option not present for device "{}"'.format(device)
        else:
            self.value = "Required configuration option not present ({}) for device({}) port ({})".format(option, device, port)

    def __str__(self):
        return repr(self.value)


class xmlDeviceConfiguration(XmlConfiguration, object):
    '''
    classdocs
    '''
    devices = {}

    def __init__(self):
        '''
        Constructor
        '''
        super(xmlDeviceConfiguration, self).__init__()

    @property
    def configuration_topic_name(self):
        return Constants.TopicNames.xmlDeviceConfiguration

    @property
    def configuration_file_name(self):
        return "configuration.xmlDeviceConfiguration"

    @property
    def logger_name(self):
        """ Set the logger level. This needs to be added to house_monitoring_logging.conf"""
        return 'configuration'

    def configure(self):
        self.devices = super(xmlDeviceConfiguration, self).configure()

    def process_configuration(self, parent):
        '''
        This routine will walk to xml tree and extract the information.  It
        does this by creating a dictionary entry for each node in the xml
        file.  It uses the tag as the key and text as the value.


        :param parent: the node in the xml file
        :type xml node:
        :Return: the parsed element tree if the file can be successfully read and parsed.
        :Raises: ConfigurationFileNotFoundError
        '''
        config = {}
        steps = []
        for child in parent:
            if (child.tag == 'xbee'):
                if ("source_address" in child.attrib):
                    source_address = child.get("source_address")
                config[source_address] = self.process_configuration(child)
            elif (child.tag == 'port'):
                if ('portname' in child.attrib):
                    portname = child.get('portname')
                config[portname] = self.process_configuration(child)
            elif (child.tag == 'steps'):
                steps = self.process_configuration(child)
                config['steps'] = steps['steps']
            elif (child.tag == 'step'):
                steps.append(child.text)
                config['steps'] = steps
            else:
                config[child.tag] = child.text
        return config

    def get(self, device=None, port=None, name=None):
        '''
        Get the steps (ie routines to execute) given the device and the port.

        :param device: the device ie. its source address, network address, or its name)
        :type string:
        :param port: the port name on the xbee. ie dio-0, adc-1
        :type string:
        :param name: name of the configuration item to get. ie (description, name, cosm_channel)
        :Returns: a list of the steps for this device
        :Raises: InvalidDeviceError, InvalidPortError, InvalidConfigurationOptionError
        '''
        if port == None:
            try:
                value = self.devices[device][name]
            except KeyError:
                if device not in self.devices:
                    raise InvalidDeviceError(device)
                if name not in self.devices[device]:
                    raise InvalidConfigurationOptionError(device, name)
        else:
            try:
                value = self.devices[device][port][name]
            except KeyError:
                if device not in self.devices:
                    raise InvalidDeviceError(device)
                if port not in self.devices[device]:
                    raise InvalidPortError(port)
                if name not in self.devices[device][port]:
                    raise InvalidConfigurationOptionError(device, port, name)
        return value

    def get_steps(self, device, port):
        '''
        Get the steps (ie routines to execute) given the device and the port.

        :param device: the device ie. its source address, network address, or its name)
        :type string:
        :param port: the port name on the xbee. ie dio-0, adc-1
        :type string:
        :Returns: a list of the steps for this device
        :Raises: InvalidDeviceError, InvalidPortError, InvalidConfigurationOptionError
        '''
        value = []
        value = self.get(device=device, port=port, name=Constants.XbeeConfiguration.steps)
        return value

    def get_name(self, device):
        '''
        Get the name of a device given the device.

        :param device: the device ie. its source address, network address, or its name)
        :type string:
        :param port: the port name on the xbee. ie dio-0, adc-1
        :type string:
        :Returns: a list of the steps for this device
        :Raises: InvalidDeviceError, InvalidPortError, InvalidConfigurationOptionError
        '''
        value = ''
        value = self.get(device=device, name=Constants.XbeeConfiguration.name)
        return value

    def valid_device(self, device):
        '''
        Check to see if device is in the configuration file.

        :param device: the device ie. its source address, network address, or its name)
        :type string:
        :Raises: InvalidDeviceError
        '''
        if device not in self.devices:
            raise InvalidDeviceError(device)
        return device

    def get_source_address(self, device):
        '''
        Get the source address given the device.

        :param device: the device ie. its source address, network address, or its name)
        :type string:
        :param port: the port name on the xbee. ie dio-0, adc-1
        :type string:
        :Returns: a list of the steps for this device
        :Raises: InvalidDeviceError, InvalidPortError, InvalidConfigurationOptionError
        '''
        value = ''
        value = self.get(device=device, name=Constants.XbeeConfiguration.source_address)
        return value

    def get_network_address(self, device):
        '''

        :param device: the device ie. its source address, network address, or its name)
        :type string:
        :param port: the port name on the xbee. ie dio-0, adc-1
        :type string:
        :Returns: a list of the steps for this device
        :Raises: InvalidDeviceError, InvalidPortError, InvalidConfigurationOptionError
        '''
        value = ''
        value = self.get(device=device, name=Constants.XbeeConfiguration.network_address)
        return value

    def get_port_name(self, device, port):
        '''

        :param device: the device ie. its source address, network address, or its name)
        :type string:
        :param port: the port name on the xbee. ie dio-0, adc-1
        :type string:
        :Returns: a list of the steps for this device
        :Raises: InvalidDeviceError, InvalidPortError, InvalidConfigurationOptionError
        '''
        value = ''
        value = self.get(device=device, port=port, name=Constants.XbeeConfiguration.name)
        return value

    def get_port_description(self, device, port):
        '''

        :param device: the device ie. its source address, network address, or its name)
        :type string:
        :param port: the port name on the xbee. ie dio-0, adc-1
        :type string:
        :Returns: a list of the steps for this device
        :Raises: InvalidDeviceError, InvalidPortError, InvalidConfigurationOptionError
        '''
        value = ''
        value = self.get(device=device, port=port, name=Constants.XbeeConfiguration.description)
        return value

    def get_port_units(self, device, port):
        '''

        :param device: the device ie. its source address, network address, or its name)
        :type string:
        :param port: the port name on the xbee. ie dio-0, adc-1
        :type string:
        :Returns: a list of the steps for this device
        :Raises: InvalidDeviceError, InvalidPortError, InvalidConfigurationOptionError
        '''
        value = ''
        value = self.get(device=device, port=port, name=Constants.XbeeConfiguration.units)
        return value

    def get_port_type(self, device, port):
        '''
        Get the type given the device and the port.

        :param device: the device ie. its source address, network address, or its name)
        :type string:
        :param port: the port name on the xbee. ie dio-0, adc-1
        :type string:
        :Returns: a list of the steps for this device
        :Raises: InvalidDeviceError, InvalidPortError, InvalidConfigurationOptionError
        '''
        value = ''
        value = self.get(device=device, port=port, name=Constants.XbeeConfiguration.type)
        return value
