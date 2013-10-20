'''
Created on Nov 6, 2012

@author: Gary
'''
from housemonitor.outputs.sqlalchemy.sqlalchemyoutputthread import SqlAlchemyOutputThread
from housemonitor.outputs.sqlalchemy.sqlalchemyoutputstep import SqlAlchemyOutputStep
from housemonitor.lib.constants import Constants
from housemonitor.lib.hmqueue import HMQueue
from housemonitor.lib.base import Base


class SqlAlchemyOutputControl( Base ):
    '''
    Start the thread that store data in the SQL database.

    '''
    queue = None
    sqlAlchemyThread = None
    in_test_mode = False

    def __init__( self ):
        '''
        Constructor
        '''
        super( SqlAlchemyOutputControl, self ).__init__()

    @property
    def logger_name( self ):
        """ Set the logger level. This needs to be added to house_monitoring_logging.conf"""
        return Constants.LogKeys.SQL_ALCHEMY_LOG

    def startSQLAlchemy( self, in_test_mode ):
        '''
        Start the ZigBee processing.

        This consists of three parts:

        #. Start the ZigBeeQueue which used Queue, a thread safe queue for communcating
        between threads.

        #. Start the SqlAlchemyOutputThread which talks to the ZigBee server.  This is a slow process.

        #. Start the ZigBeeOutputProcessing object which takes massages sent to ZigBee on the
        main thread and sends them to the ZigBee thread.

        '''
        self.queue = HMQueue( 'sqlAlchemy' )
        self.in_test_mode = in_test_mode
        self.sqlAlchemy = SqlAlchemyOutputStep( self.queue )

        self.sqlAlchemyOutputThread = SqlAlchemyOutputThread( self.queue, self.in_test_mode )
        self.sqlAlchemyOutputThread.start()
