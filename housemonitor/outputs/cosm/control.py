'''
Created on Nov 6, 2012

@author: Gary
'''
from .outputthread import COSMOutputThread
from housemonitor.lib.hmqueue import HMQueue
from send import COSMSend
from housemonitor.lib.constants import Constants

from housemonitor.configuration.cosmconfiguration import CosmConfiguration
from housemonitor.lib.base import Base
from outputStep import COSMOutputStep


class COSMControl( Base ):
    '''
    COSMControl starts the COSM processing which sends data to the COSM web site
    at the following URL:

    `https://cosm.com/ <https://cosm.com/>`_.

    This consists of three parts:
    
    1. Start the COSMQueue which uses Queue, a thread safe queue for communcating between threads.
    
    2. Start the COSMOutputThread which talks to the COSM server.  This is a slow process.
    
    3. Start the COSMOutputStep object which takes massages sent to COSM on the main thread and sends it to the COSM thread.  It's topic name is:
    
        Constants.TopicNames.COSM('outputs.COSM').

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
        
        >>> from optparse import OptionParser
        >>> from outputs.cosm.control import COSMControl
        >>> c = COSMControl()                                                   # doctest: +SKIP
        >>> options = 1                                                         # doctest: +SKIP
        >>> c.startCOSM(options)                                                # doctest: +SKIP
        >>> c.cosmOutputThread.forever = False                                  # doctest: +SKIP
        >>> c = None                                                            # doctest: +SKIP
        
        .. warning:: This doctest has been disabled.  It is trying to start too much.

        '''
        self.logger.debug( 'COSM starting up' )
        self.queue = HMQueue( 'COSM' )
        self.cosmOutputThread = COSMOutputThread( self.queue, options, name='COSM' )
        self.cosmOutputThread.start()
        self.cosm = COSMOutputStep( self.queue )


if __name__ == "__main__":
    import doctest
    doctest.testmod()
