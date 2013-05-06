'''
Created on Nov 6, 2012

@author: Gary
'''
from outputs.zigbee.zigbeeoutputthread import ZigBeeOutputThread
from lib.constants import Constants
from lib.hmqueue import HMQueue
from lib.base import Base
from outputs.zigbee.zigbeeoutputstep import ZigBeeOutputStep


class ZigBeeControl( Base ):
    '''
    ZigBeeControl starts the ZigBee processing to send data to ZigBee at the following
    URL:

    https://cosm.com/

    '''
    queue = None
    ZigBeeOutputThread = None
    cosm = None

    def __init__( self ):
        '''
        Constructor
        '''
        super( ZigBeeControl, self ).__init__()

    @property
    def logger_name( self ):
        """ Set the logger level. This needs to be added to house_monitoring_logging.conf"""
        return Constants.LogKeys.outputsZigBee

    def startZigBee( self, options ):
        '''
        Start the ZigBee processing.

        This consists of three parts:

        #. Start the ZigBeeQueue which used Queue, a thread safe queue for communcating
        between threads.

        #. Start the ZigBeeOutputThread which talks to the ZigBee server.  This is a slow process.

        #. Start the ZigBeeOutputProcessing object which takes massages sent to ZigBee on the
        main thread and sends them to the ZigBee thread.

        '''
        self.queue = HMQueue( 'ZigBeeInput' )
        self.zig = ZigBeeOutputStep( self.queue )

        self.ZigBeeOutputThread = ZigBeeOutputThread( self.queue )
        self.ZigBeeOutputThread.start()
