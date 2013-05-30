'''
Created on Aug 2, 2012

@author: Gary
'''
import abc
from pubsub import pub
from housemonitor.lib.base import Base
from housemonitor.lib.constants import Constants


class abcInput(Base, object):
    '''
    This abstract class will input all the data and send it on
    it's way.
    '''
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        '''
        Constructor
        '''
        super(abcInput, self).__init__()
        self.logger.debug("in iInput")

    @abc.abstractproperty
    def topic_name(self):
        return 'Should never see this'  # pragma: no cover

    @abc.abstractmethod
    def input(self):
        pass  # pragma: no cover

    @abc.abstractproperty
    def logger_name(self):
        """ Set the logger level. This needs to be added to house_monitoring_logging.conf"""
        return Constants.LogKeys.inputs  # pragma: no cover
