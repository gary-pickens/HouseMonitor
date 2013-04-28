'''
Created on Nov 6, 2012

@author: Gary
'''
from pubsub import pub
from pubsub import utils
from base import Base
from pprint import pprint
from lib.constants import Constants
from pubsub.utils import printTreeDocs


class PubSubAid( Base ):
    '''
    classdocs
    '''

    def __init__( self ):
        '''
        Constructor
        '''
        super( PubSubAid, self ).__init__()
        pub.subscribe( self.process, Constants.TopicNames.Step )
        pub.subscribe( self.outputs, "outputs" )
        pub.subscribe( self.all_topics, "ALL_TOPICS" )
        pub.subscribe( self.scheduler, Constants.TopicNames.SchedulerStep )
        pub.subscribe( self.registration, Constants.TopicNames.Registration )
        treeDoc = printTreeDocs()
        pprint( treeDoc )
        pub.setTopicUnspecifiedFatal( True )

    @property
    def logger_name( self ):
        """ Set the logger name. This needs to be added to house_monitoring_logging.conf"""
        return 'PubSubAid'

    def process( self ):
        self.logger.debug( "process topic received" )

    def outputs( self ):
        self.logger.info( 'outputs topic recieved' )

    def all_topics( self ):
        self.logger.debug( 'all topics recieved' )

    def scheduler( self ):
        self.logger.DEBUG( 'scheduler topic received' )

    def registration( self ):
        self.logger.WARN( 'registration topic received' )
