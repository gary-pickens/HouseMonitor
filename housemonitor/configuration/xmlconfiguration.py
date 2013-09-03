'''

Created on Aug 6, 2012

@author: Gary

This module is for reading xml Configuration files.

'''
import abc
import os
import datetime
import re
import sys
import logging
from xml.etree.ElementTree import ElementTree
import pprint
from abc_configuration import abcConfiguration


class ConfigurationFileNotFoundError(Exception):
    '''
    This exception will be raised when the requested xml file can not be
    found.
    '''

    def __init__(self, value):
        full_path = os.path.join(os.getcwd(), value)
        self.value = \
            "Configuration file does not exist: {}".\
            format(full_path)

    def __str__(self):
        return repr(self.value)


class ConfigurationFileError(Exception):
    '''
    This exception will be raised when there is a error in the xml file. For
    example an invalid list type, or a duplicate entry in each section.
    '''

    def __init__(self, value):
        path = os.path.join(os.getcwd(), value)
        self.value = \
            "Error in configuration file {} near \"{}\"".format(path, value)

    def __str__(self):
        return repr(self.value)


class XmlConfiguration(abcConfiguration):
    '''
    This class will read an XML configuration file in the config directory
    '''

    DIRECTORIES = [os.getcwd(), "config"]
    configutation_directory = os.path.join(*DIRECTORIES)
    config = {}

    def __init__(self):
        super(XmlConfiguration, self).__init__()
        self.configure()

    def __getitem__(self, system):
        return self.config[system]

    def __setitem__(self, system, value):
        self.config[system] = value

    def file_name(self, filename=None):
        '''
        Generate a path for the xml configuration file.

        :Param filename: the name of the configuration file
        :type filename: string
        :return: the relative path to the configuation file
        :Raises: ConfigurationFileNotFoundExceptioon
        '''
        if filename == None:
            fname = self.configuration_file_name
        else:
            fname = str(filename)
        if (None == re.match(".*\.xml$", fname)):
            filename = "{}.xml".format(fname)
        else:
            filename = fname

        full_filename = os.path.join(self.configutation_directory, filename)
        if (not os.path.exists(full_filename)):
            self.logger.error("Configuration file not found: %s",
                              full_filename)
            raise ConfigurationFileNotFoundError(full_filename)
        return full_filename

    def configure(self, filename=None):
        '''
        configure is the concrete method for configuring a class.

        '''
        parsedTree = None
        self.config = {}
        parsedTree = self.parse_xml_file(filename)
        self.config = self.process_configuration(parsedTree)
        self.logger.debug('{} config = \n{}'.format(filename, pprint.pformat(self.config)))
        return self.config

    def parse_xml_file(self, filename=None):
        '''
        parse_xml_file does three things:
        1.  build the configuration filename
        2.  open the file for reading
        3.  parse the file using ElementTree

        :param name: the name of the configuration file
        :Return: a parsed element tree if the file can be successfully read and parsed.

        :Raises: ConfigurationFileNotFoundError
        '''
        xml = ElementTree()
        filename = self.file_name(filename)
        with open(filename, 'rt') as f:
            parsedTree = xml.parse(f)
            f.close()
            return parsedTree

    def process_configuration(self, parent):
        '''
        This routine will walk to xml tree and extract the information.  It
        does this by creating a dictionary entry for each node in the xml
        file.  It uses the tag as the key and text as the value.

        Args:
            parent is the node in the xml file

        Return:
            a parsed element tree if the file can be successfully read and
            parsed.

            Exceptions:
            ConfigurationFileNotFoundError
        '''
        config = {}
        if (parent.get("type", "dict") == "dict"):
            for child in parent:
                if (len(list(child)) == 0):
                    value = child.text.strip()
                    config[child.tag] = value
                elif (len(list(child)) > 0):
                    config[child.tag] = self.process_configuration(child)
            return config
        elif(parent.get("type", 'dict') == "list"):
            lst = []
            for child in parent:
                if (child.tag == "steps"):
                    l = self.process_configuration(child)
                    lst.append(l)
                else:
                    value = child.text.strip()
                    lst.append(value)
            return lst
        else:
            raise ConfigurationFileError(parent.tag)
