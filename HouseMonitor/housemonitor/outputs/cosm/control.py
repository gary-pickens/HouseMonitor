'''
Created on Nov 6, 2012

@author: Gary
'''
from outputthread import COSMOutputThread
from lib.hmqueue import HMQueue
from send import COSMSend
from lib.constants import Constants

from configuration.cosmconfiguration import CosmConfiguration
from lib.base import Base
from outputStep import COSMOutputStep


class COSMControl( Base ):
    '''
    COSMControl starts the COSM processing to send data to COSM at the following
    URL:

    https://cosm.com/

    '''
    queue = None
    cosmOutputThread = None
    cosm = None

    def __init__( self ):
        '''
        Constructor
        '''
        super( COSMControl, self ).__init__()

    @property
    def logger_name( self ):
        """ Set the logger level. This needs to be added to house_monitoring_logging.conf"""
        return Constants.LogKeys.outputsCOSM

    def startCOSM( self, options ):
        '''
        Start the COSM processing.

        This consists of three parts:

        #. Start the COSMQueue which used Queue, a thread safe queue for communcating
        between threads.

        #. Start the COSMOutputThread which talks to the COSM server.  This is a slow process.

        #. Start the COSMOutputProcessing object which takes massages sent to COSM on the
        main thread and sends them to the COSM thread.

        '''
        self.logger.debug( 'COSM starting up' )
        self.queue = HMQueue( 'COSM' )
        self.cosmOutputThread = COSMOutputThread( self.queue, options, name='COSM' )
        self.cosmOutputThread.start()
        self.cosm = COSMOutputStep( self.queue )
