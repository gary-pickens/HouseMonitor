'''
Created on Sep 12, 2012

@author: Gary
'''
import logging
import abc


class Base(object):
    '''
    classdocs
    '''
    __metaclass__ = abc.ABCMeta

    logger = None

    def __init__(self):
        '''
        Constructor
        '''
        self.logger = logging.getLogger(self.logger_name)

    @abc.abstractproperty
    def logger_name(self):
        return "call to invalid abstract property"  # pragma: no cover
