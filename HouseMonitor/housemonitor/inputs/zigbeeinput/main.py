'''
Created on Sep 13, 2012

@author: Gary
'''

from lib.base import Base
from inputs.zigbeeinput.xbeeinputthread import XBeeInputThread
from inputs.inputqueue import InputQueue
from lib.constants import Constants


def instantuate_me():
    return Main()


class Main(Base):

    @property
    def logger_name(self):
        return Constants.LogKeys.inputsZigBee

    def __init__(self):
        super(Main, self).__init__()
        self.logger.debug('Start Input Queue')
        input_queue = InputQueue()
        self.logger.debug('instantuate XBeeInputThread')
        xbee_thread = XBeeInputThread(input_queue)
        self.logger.debug('Start Thread')
        xbee_thread.start()
