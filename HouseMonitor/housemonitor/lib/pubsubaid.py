'''
Created on Nov 6, 2012

@author: Gary
'''
from pubsub import pub
from pubsub import utils
from base import Base
from pprint import pprint, pformat
from housemonitor.lib.constants import Constants
from pubsub.utils import printTreeDocs


class PubSubAid( Base ):
    '''
    PubSubAid provides subscriptions for some lingering topics and sets setTopicUnspecifiedFatal
    to true.  This will prevent using topics that do not have someplace to go.
    '''
    @property
    def logger_name( self ):
        """ Set the logger name. This needs to be added to house_monitoring_logging.conf"""
        return 'PubSubAid'

    def __init__( self ):
        '''
        Constructor
        '''
        super( PubSubAid, self ).__init__()
        try:
            self.logger.debug( "PubSubAid starting" )
            pub.subscribe( self.step, Constants.TopicNames.Step )
            pub.subscribe( self.outputs, Constants.TopicNames.Outputs )
            pub.subscribe( self.all_topics, Constants.TopicNames.ALL_TOPICS )
            printTreeDocs( extra='LaDA' )
            print()
            pub.setTopicUnspecifiedFatal( True )
            self.logger.debug( "PubSubAid ending" )
        except Exception as ex:
            self.logger.exception( 'exception in BupSupAid {}'.format( ex ) )

    def step( self ):
        ''' 
        A catch all for topic step.
        '''
        self.logger.debug( "process topic step" )

    def outputs( self ):
        '''
        A catch all for topic outputs.
        '''
        self.logger.debug( "'outputs' topic received" )

    def all_topics( self ):
        '''
        A catch all for all topics.
        '''
        self.logger.debug( 'all topics received' )

