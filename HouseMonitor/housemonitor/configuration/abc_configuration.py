'''
Created on Aug 5, 2012

@author: Gary
'''
import abc
from pubsub import pub
from lib.base import Base


class abcConfiguration(Base, object):
    '''
    This module will provide configuration aid
    '''
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        '''
        Constructor
        '''
#        pub.subscribe(self.configure, self.config_topic_name)
        super(abcConfiguration, self).__init__()

    @abc.abstractproperty
    def configuration_topic_name(self):
        return "call to invalid abstract property"  # pragma: no cover

    @abc.abstractproperty
    def configuration_file_name(self):
        return "call to invalid abstract property"  # pragma: no cover

    @abc.abstractmethod
    def configure(self):
        raise NotImplementedError("Missing configure routine in conversion \
            class derived from abstract conversions class")  # pragma: no cover

    def logger_name(self):
        """ Set the logger level. This needs to be added to house_monitoring_logging.conf"""
        return "configuration"  # pragma: no cover
